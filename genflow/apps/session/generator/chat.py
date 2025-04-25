# Copyright (C) 2025 Reveal AI
#
# SPDX-License-Identifier: MIT

from django.db.models.query import QuerySet

from genflow.apps.ai.llm.entities import Result
from genflow.apps.core.config.llm_model_bundle import LLMModelBundle
from genflow.apps.core.config.provider_service import AIProviderConfigurationService
from genflow.apps.core.models import Provider
from genflow.apps.prompt.models import PromptType, Prompt
from genflow.apps.assistant.models import AssistantContextSource, Assistant
from genflow.apps.session.generator.base import BaseGenerator
from genflow.apps.session.generator.entities import GenerateEntity, GenerateRequest
from genflow.apps.session.models import Session, SessionMode, SessionType
from genflow.apps.session.transform.base import PromptTemplateEntity


class ChatGenerator(BaseGenerator):
    """
    Responsible for generating chat responses using a specified
    LLM model including chat history depending on session mode. It integrates with a database session and supports streaming responses.
    """

    def __init__(
        self, queryset: QuerySet[Provider], db_session: Session, stream: bool = True
    ) -> None:
        """
        Initializes the ChatGenerator with the given queryset, database session, and
            optional streaming configuration.
        """
        related_model = db_session.related_model
        if db_session.session_type == SessionType.PROMPT.value:
            related_model = db_session.related_prompt.related_model
        if db_session.session_type == SessionType.ASSISTANT.value:
            related_model = db_session.related_assistant.related_model

        model_collection_bundle = AIProviderConfigurationService.get_model_collection_bundle(
            related_model.provider_name,
            queryset=queryset,
        )
        llm_model_bundle = LLMModelBundle(
            configuration=model_collection_bundle.configuration,
            ai_provider_instance=model_collection_bundle.ai_provider_instance,
            model_collection_instance=model_collection_bundle.model_collection_instance,
            model_schema=model_collection_bundle.model_collection_instance.get_model_schema(
                model_name=related_model.model_name
            ),
            parameters=related_model.parameters,
            credentials=model_collection_bundle.configuration.user_configuration.provider.credentials,
        )
        super().__init__(db_session=db_session, llm_model_bundle=llm_model_bundle)

        prompt_entity = None
        if db_session.session_type == SessionType.PROMPT.value:
            prompt: Prompt = db_session.related_prompt
            prompt_entity = PromptTemplateEntity(
                prompt_type=prompt.prompt_type,
                simple_prompt_template=prompt.pre_prompt,
            )
        if db_session.session_type == SessionType.ASSISTANT.value:
            assistant: Assistant = db_session.related_assistant
            prompt_entity = PromptTemplateEntity(
                prompt_type=PromptType.SIMPLE.value,
                simple_prompt_template=assistant.pre_prompt,
            )

        self.generate_entity = GenerateEntity(
            db_session=db_session,
            llm_model_bundle=llm_model_bundle,
            prompt_entity=prompt_entity,
            stream=stream,
        )

    def generate(self, generate_request: GenerateRequest) -> Result:
        """
        Generates a response based on the provided request, which includes the query,
            optional files, and parameters.
        """

        query = generate_request.query
        files = generate_request.files
        stream = (
            generate_request.stream
            if generate_request.stream is not None
            else self.generate_entity.stream
        )
        use_memory = True if self.db_session.session_mode == SessionMode.CHAT.value else False

        # load files content
        if files is not None and len(files) > 0:
            files = self.db_session.load_user_files(files)

        # Include: prompt template, query(optional), files(optional)
        # Not Include: memory
        self.get_precalculate_rest_tokens(
            prompt_template_entity=self.generate_entity.prompt_entity,
            files=files,
            query=query,
        )

        input_messages, stop = self.organize_input_messages(
            prompt_template_entity=self.generate_entity.prompt_entity,
            files=files,
            query=query,
            memory=use_memory,
        )

        # set session name if this is the first message
        # and session name is not set
        if (
            query
            and self.db_session.sessionmessage_set.count() == 0
            and self.db_session.name == "New Chat"
        ):
            self.db_session.name = f"{query[:17]}..." if len(query) > 20 else query
            self.db_session.save()

        # get context
        context = None
        if self.db_session.session_type == SessionType.ASSISTANT.value:
            assistant: Assistant = self.db_session.related_assistant
            if assistant.context_source == AssistantContextSource.FILES.value:
                context = assistant.get_files_context()
            elif assistant.context_source == AssistantContextSource.COLLECTIONS.value:
                context = ''

        input_messages, stop = self.organize_input_messages(
            prompt_template_entity=self.generate_entity.prompt_entity,
            files=files,
            query=query,
            context=context,
            memory=use_memory,
        )

        # Re-calculate the max tokens if sum(prompt_token +  max_tokens) over model token limit
        self.recalculate_max_tokens(input_messages=input_messages)

        # call model
        response = self.llm_model_bundle.call(
            messages=input_messages,
            parameters=(
                self.generate_entity.llm_model_bundle.parameters
                if generate_request.parameters is None
                else generate_request.parameters
            ),
            stop=stop,
            stream=stream,
            user=generate_request.user_id,
        )

        # handle response
        result = self._handle_model_response(
            response=response,
            callback=generate_request.callback,
            stream=stream,
        )

        return result
