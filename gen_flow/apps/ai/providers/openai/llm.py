# Copyright (C) 2025 Reveal AI
#
# SPDX-License-Identifier: MIT

from typing import Optional, Union, Generator, cast

import tiktoken
from openai import Stream
from openai.types import Completion
from openai.types.chat import ChatCompletion, ChatCompletionChunk

from gen_flow.apps.ai.base.entities.shared import ModelType
from gen_flow.apps.ai.llm.messages import Message, UserMessage, AssistantMessage, SystemMessage, MessageContentType
from gen_flow.apps.ai.llm.entities import Result, ResultChunk, ResultChunkDelta
from gen_flow.apps.ai.llm.llm_model_collection import LLMMode, LLMModelCollection
from gen_flow.apps.ai.providers.registry import register_model_collection
from gen_flow.apps.ai.providers.openai.client import OpenAIClient


@register_model_collection(ai_provider='openai', model_type=ModelType.LLM.value)
class OpenAILargeLanguageModel(LLMModelCollection):
    '''
    Defines the interface for a collection of language models (LLMs) provided by OpenAI.
    '''


    def validate_credentials(self, model: str, credentials: dict) -> None:
        '''
        Validates model credentials
        '''
        try:
            client = OpenAIClient(credentials=credentials)

            # get model mode
            model_mode = self.get_model_mode(model=model)

            if model_mode == LLMMode.CHAT:
                # chat model
                client.chat.completions.create(
                    messages=[{'role': 'user', 'content': 'ping'}],
                    model=model,
                    temperature=0,
                    max_tokens=20,
                    stream=False,
                )
            else:
                # text completion model
                client.completions.create(
                    prompt='ping',
                    model=model,
                    temperature=0,
                    max_tokens=20,
                    stream=False,
                )
        except Exception as ex:
            # TODO: log -> 'Error validating credentials for model {model}: {ex}'
            raise ex

    def get_tokens_count(
        self,
        model: str,
        messages: list[Message],
    ) -> int:
        '''
        Gets the token counts for a given model and messages.
        '''

        # get model mode
        model_mode = self.get_model_mode(model)

        if model_mode == LLMMode.CHAT:
            # chat model
            return self._get_tokens_count_from_messages(model=model, messages=messages)
        else:
            # text completion model
            if len(messages) == 0:
                return 0
            return self._get_tokens_count_from_string(model, messages[0].content)

    def _get_tokens_count_from_messages(
        self,
        model: str,
        messages: list[Message]
    ) -> int:
        '''
        Return the number of tokens used by a list of messages.
        Official documentation: https://github.com/openai/openai-cookbook/blob/main/examples/How_to_format_inputs_to_ChatGPT_models.ipynb
        Information on how messages are converted to tokens: https://platform.openai.com/docs/advanced-usage/managing-tokens
        '''

        # Use gpt4o to calculate chatgpt-4o-latest's token.
        if model == 'chatgpt-4o-latest' or model.startswith('o1'):
            model = 'gpt-4o'

        try:
            encoding = tiktoken.encoding_for_model(model)
        except KeyError:
            # TODO: log -> 'Warning: model not found. Using cl100k_base encoding.'
            model = 'cl100k_base'
            encoding = tiktoken.get_encoding(model)

        if model.startswith('gpt-3.5-turbo-0301'):
            tokens_per_message = 4 # every message follows <im_start>{role/name}\n{content}<im_end>\n
            tokens_per_name = -1 # if there's a name, the role is omitted
        elif model.startswith('gpt-3.5-turbo') or model.startswith('gpt-4') or model.startswith('o1'):
            tokens_per_message = 3
            tokens_per_name = 1
        else:
            raise NotImplementedError(
                f'_get_tokens_count_from_messages() is not implemented for model {model}.'
            )

        num_tokens = 0
        messages_dict = [message.to_dict() for message in messages]
        for message in messages_dict:
            num_tokens += tokens_per_message
            for key, value in message.items():
                # 'content' my be a list
                if isinstance(value, list):
                    text = ''
                    for item in value:
                        if isinstance(item, dict) and item['type'] == 'text':
                            text += item['text']

                    value = text

                num_tokens += len(encoding.encode(str(value)))
                if key == 'name':
                    num_tokens += tokens_per_name

        num_tokens += 3 # every reply is primed with <|start|>assistant<|message|>

        return num_tokens

    def _get_tokens_count_from_string(
            self,
            model: str,
            text: str,
        ) -> int:
        '''
        Return the number of tokens used by a text.
        '''

        try:
            encoding = tiktoken.encoding_for_model(model)
        except KeyError:
            # TODO: log -> 'Warning: model not found. Using cl100k_base encoding.'
            encoding = tiktoken.get_encoding('cl100k_base')

        num_tokens = len(encoding.encode(text))
        return num_tokens

    def _call(
        self,
        model: str,
        credentials: dict,
        messages: list[Message],
        parameters: dict,
        stop: Optional[list[str]] = None,
        stream: bool = True,
        user: Optional[str] = None,
    ) -> Union[Result, Generator]:
        '''
        Calls the model with the given parameters and messages.
        '''

        # init model client
        client = OpenAIClient(credentials=credentials)

        extra_model_kwargs = {}
        if stop:
            extra_model_kwargs['stop'] = stop

        if user:
            extra_model_kwargs['user'] = user

        if stream:
            extra_model_kwargs['stream_options'] = {'include_usage': True}
        # get model mode
        model_mode = self.get_model_mode(model, credentials)

        if model_mode == LLMMode.CHAT:
            # chat model
            return self._chat_completions(
                model=model,
                client=client,
                messages=messages,
                parameters=parameters,
                extra_model_kwargs=extra_model_kwargs,
                stop=stop,
                stream=stream,
            )
        else:
            # text completion model
            return self._completions(
                model=model,
                credentials=credentials,
                messages=messages,
                parameters=parameters,
                stop=stop,
                stream=stream,
                user=user,
            )

    def _chat_completions(
        self,
        model: str,
        client: OpenAIClient,
        messages: list[Message],
        parameters: dict,
        extra_model_kwargs: dict,
        stop: Optional[list[str]] = None,
        stream: bool = True,
    ) -> Union[Result, Generator]:
        '''
        Calls llm chat model
        '''

        # clear illegal prompt messages
        messages = self._fix_messages(model, messages)

        block_as_stream = False
        if model.startswith('o1'):
            if stream:
                block_as_stream = True
                stream = False

                if 'stream_options' in extra_model_kwargs:
                    del extra_model_kwargs['stream_options']

            if 'stop' in extra_model_kwargs:
                del extra_model_kwargs['stop']

        # chat model
        response = client.chat.completions.create(
            messages=[message.to_dict() for message in messages],
            model=model,
            stream=stream,
            **parameters,
            **extra_model_kwargs,
        )

        if stream:
            return self._process_chat_completions_stream_response(model, response, messages)

        block_result = self._process_chat_completions_response(model, response, messages)

        if block_as_stream:
            return self._process_chat_completions_block_as_stream_response(block_result, messages, stop)

        return block_result

    def _fix_messages(
            self,
            model: str,
            messages: list[Message]
        ) -> list[Message]:
        '''
        Fix messages for OpenAI API based on the model
        '''

        if model in ['gpt-4-turbo', 'gpt-4-turbo-2024-04-09']:
            # user messages content should be str
            # and not a list of MessageContent
            for message in messages:
                if isinstance(message, UserMessage):
                    if isinstance(message.content, list):
                        message.content = '\n'.join(
                            [
                                item.data
                                if item.type == MessageContentType.TEXT
                                else ''
                                for item in message.content
                            ]
                        )

        if model.startswith('o1'):
            # system messages content should be converted to user messages

            count = len(
                filter(
                    lambda x: isinstance(x, SystemMessage),
                    messages
                )
            )
            if count == 0:
                return messages

            # convert system messages to user messages
            new_messages = []
            for message in messages:
                if isinstance(message, SystemMessage):
                    message = UserMessage(
                        content=message.content,
                        name=message.name,
                    )

                new_messages.append(message)

        return new_messages

    def _process_chat_completions_stream_response(
        self,
        model: str,
        response: Stream[ChatCompletionChunk],
        messages: list[Message],
    ) -> Generator:
        '''
        Processes llm chat stream response
        '''

        final_chunk = ResultChunk(
            model=model,
            messages=messages,
            delta=ResultChunkDelta(
                index=0,
                message=AssistantMessage(content=''),
            ),
        )

        full_assistant_content = ''
        input_tokens = 0
        output_tokens = 0
        for chunk in response:
            if len(chunk.choices) == 0:
                if chunk.usage:
                    # get input and output tokens from usage
                    input_tokens = chunk.usage.prompt_tokens
                    output_tokens = chunk.usage.completion_tokens
                continue

            delta = chunk.choices[0]
            has_finish_reason = delta.finish_reason is not None

            if (
                not has_finish_reason
                and (delta.delta.content is None or delta.delta.content == '')
            ):
                continue

            # transform assistant message to message
            assistant_message = AssistantMessage(content=delta.delta.content or '')

            full_assistant_content += delta.delta.content or ''

            if has_finish_reason:
                final_chunk = ResultChunk(
                    model=chunk.model,
                    messages=messages,
                    system_fingerprint=chunk.system_fingerprint,
                    delta=ResultChunkDelta(
                        index=delta.index,
                        message=assistant_message,
                        finish_reason=delta.finish_reason,
                    ),
                )
            else:
                yield ResultChunk(
                    model=chunk.model,
                    messages=messages,
                    system_fingerprint=chunk.system_fingerprint,
                    delta=ResultChunkDelta(
                        index=delta.index,
                        message=assistant_message,
                    ),
                )

        # calculate input tokens
        if not input_tokens:
            input_tokens = self._get_tokens_count_from_messages(model, messages)

        # calculate output tokens
        if not output_tokens:
            full_assistant_message = AssistantMessage(
                content=full_assistant_content
            )
            output_tokens = self._get_tokens_count_from_messages(model, [full_assistant_message])

        # build usage entity
        usage = self._calculate_usage(model=model, input_tokens=input_tokens, output_tokens=output_tokens)
        final_chunk.delta.usage = usage

        yield final_chunk

    def _process_chat_completions_response(
        self,
        model: str,
        response: ChatCompletion,
        messages: list[Message],
    ) -> Result:
        '''
        Processes llm chat response
        '''

        assistant_message = response.choices[0].message

        # transform assistant message to prompt message
        assistant_message = AssistantMessage(content=assistant_message.content)

        # calculate tokens count
        if response.usage:
            # get input and output tokens from usage
            input_tokens = response.usage.prompt_tokens
            output_tokens = response.usage.completion_tokens
        else:
            # calculate input and output tokens
            input_tokens = self._get_tokens_count_from_messages(model, messages)
            output_tokens = self._get_tokens_count_from_messages(model, [assistant_message])

        # build usage entity
        usage = self._calculate_usage(model, input_tokens=input_tokens, output_tokens=output_tokens)

        # build result entity
        response = Result(
            model=response.model,
            messages=messages,
            message=assistant_message,
            usage=usage,
            system_fingerprint=response.system_fingerprint,
        )

        return response

    def _process_chat_completions_block_as_stream_response(
        self,
        block_result: Result,
        messages: list[Message],
        stop: Optional[list[str]] = None,
    ) -> Generator[ResultChunk, None, None]:
        '''
        Processes llm chat block_as_stream response
        '''

        text = block_result.message.content
        text = cast(str, text)

        if stop:
            text = self.truncate_at_stop_tokens(text=text, stop=stop)

        yield ResultChunk(
            model=block_result.model,
            messages=messages,
            system_fingerprint=block_result.system_fingerprint,
            delta=ResultChunkDelta(
                index=0,
                message=AssistantMessage(content=text),
                finish_reason="stop",
                usage=block_result.usage,
            ),
        )

    def _completions(
        self,
        model: str,
        client: OpenAIClient,
        messages: list[Message],
        parameters: dict,
        extra_model_kwargs: dict,
        stream: bool = True,
    ) -> Union[Result, Generator]:
        '''
        Calls llm completion model
        '''

        # text completion model
        response = client.completions.create(
            prompt=messages[0].content, model=model, stream=stream, **parameters, **extra_model_kwargs
        )

        if stream:
            return self._process_completions_stream_response(model, response, messages)

        return self._process_completions_response(model, response, messages)

    def _process_completions_stream_response(
        self,
        model: str,
        response: Stream[Completion],
        messages: list[Message]
    ) -> Generator:
        '''
        Processes llm completion stream response
        '''

        final_chunk = ResultChunk(
            model=model,
            messages=messages,
            delta=ResultChunkDelta(
                index=0,
                message=AssistantMessage(content=''),
            ),
        )

        full_text = ''
        input_tokens = 0
        output_tokens = 0
        for chunk in response:
            if len(chunk.choices) == 0:
                if chunk.usage:
                    # get input and output tokens from usage
                    input_tokens = chunk.usage.prompt_tokens
                    output_tokens = chunk.usage.completion_tokens
                continue

            delta = chunk.choices[0]

            if delta.finish_reason is None and (delta.text is None or delta.text == ''):
                continue

            # transform assistant message to message
            text = delta.text or ''
            assistant_message = AssistantMessage(content=text)

            full_text += text

            if delta.finish_reason is not None:
                final_chunk = ResultChunk(
                    model=chunk.model,
                    messages=messages,
                    system_fingerprint=chunk.system_fingerprint,
                    delta=ResultChunkDelta(
                        index=delta.index,
                        message=assistant_message,
                        finish_reason=delta.finish_reason,
                    ),
                )
            else:
                yield ResultChunk(
                    model=chunk.model,
                    messages=messages,
                    system_fingerprint=chunk.system_fingerprint,
                    delta=ResultChunkDelta(
                        index=delta.index,
                        message=assistant_message,
                    ),
                )

        # calculate input tokens
        if not input_tokens:
            input_tokens = self._get_tokens_count_from_string(model=model, text=messages[0].content)

        # calculate output tokens
        if not output_tokens:
            output_tokens = self._get_tokens_count_from_string(model=model, text=full_text)

        # build usage entity
        usage = self._calculate_usage(model=model, input_tokens=input_tokens, output_tokens=output_tokens)
        final_chunk.delta.usage = usage

        yield final_chunk

    def _process_completions_response(
        self, model: str,
        response: Completion,
        messages: list[Message]
    ) -> Result:
        '''
        Processes llm completion response
        '''

        assistant_text = response.choices[0].text

        # transform assistant message to message
        assistant_message = AssistantMessage(content=assistant_text)

        # calculate tokens count
        if response.usage:
            # get input and output tokens from usage
            input_tokens = response.usage.prompt_tokens
            output_tokens = response.usage.completion_tokens
        else:
            # calculate num tokens
            input_tokens = self._get_tokens_count_from_string(model=model, text=messages[0].content)
            output_tokens = self._get_tokens_count_from_string(model=model, text=assistant_text)

        # build usage entity
        usage = self._calculate_usage(model=model, input_tokens=input_tokens, output_tokens=output_tokens)

        # build result entity
        result = Result(
            model=response.model,
            messages=messages,
            message=assistant_message,
            usage=usage,
            system_fingerprint=response.system_fingerprint,
        )

        return result
