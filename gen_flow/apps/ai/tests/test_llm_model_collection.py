# Copyright (C) 2025 Reveal AI
#
# SPDX-License-Identifier: MIT

from os import path as osp
from unittest import TestCase

from django.conf import settings

from gen_flow.apps.ai.llm.messages import UserMessage, AssistantMessage, SystemMessage, TextMessageContent
from gen_flow.apps.ai.tests.utils import DummyAIProvider, DummyLLMModelCollection, create_dummy_model_config

class MessageTest(TestCase):
    '''
    Test class for the Message class.
    '''

    def test_user_message_to_dict(self):
        '''
        Test the UserMessage class.
        '''

        user_message = UserMessage(content='hello')
        self.assertEqual(user_message.to_dict(), {'content': 'hello', 'role': 'user'})

        message_content1 = TextMessageContent(data='hello')
        message_content2 = TextMessageContent(data='world')
        user_message = UserMessage(content=[message_content1, message_content2])
        self.assertEqual(
            user_message.to_dict(),
            {'content': [{'type': 'text', 'text': 'hello'}, {'type': 'text', 'text': 'world'}], 'role': 'user'}
        )

    def test_assistant_message_to_dict(self):
        '''
        Test the AssistantMessage class.
        '''

        assistant_message = AssistantMessage(content='hello')
        self.assertEqual(assistant_message.to_dict(), {'content': 'hello', 'role': 'assistant'})

        assistant_message = AssistantMessage(content='hello', name='assistant')
        self.assertEqual(assistant_message.to_dict(), {'content': 'hello', 'role': 'assistant', 'name': 'assistant'})


    def test_system_message_to_dict(self):
        '''
        Test the SystemMessage class.
        '''

        system_message = SystemMessage(content='hello')
        self.assertEqual(system_message.to_dict(), {'content': 'hello', 'role': 'system'})

        message_content1 = TextMessageContent(data='hello')
        message_content2 = TextMessageContent(data='world')
        system_message = SystemMessage(content=[message_content1, message_content2])
        self.assertEqual(
            system_message.to_dict(),
            {'content': [message_content1.model_dump(), message_content2.model_dump()], 'role': 'system'}
        )

class LLMModelCollectionTest(TestCase):
    @classmethod
    def setUpClass(cls):
        create_dummy_model_config()
        cls.model_type = 'llm'
        cls.llm_model_collection = DummyLLMModelCollection()
        cls.llm_model_collection.config_path = osp.join(
            settings.MODEL_CONFIG_ROOT,
            DummyAIProvider.PROVIDER_FOLDER,
            cls.model_type
        )

    def test_get_parameter_configs(self):
        models = self.llm_model_collection.get_models()
        for model in models:
            parameter_configs = self.llm_model_collection.get_parameter_configs(model.id)
            if model.parameter_configs:
                self.assertEqual(len(parameter_configs), len(model.parameter_configs))
                for parameter_config in parameter_configs:
                    self.assertTrue(parameter_config in model.parameter_configs)

    def test_process_model_parameters(self):
        models = self.llm_model_collection.get_models()
        for model in models:
            model_parameters = {}
            for parameter_config in model.parameter_configs:
                model_parameters[parameter_config.name] = parameter_config.default
            processed_parameters = self.llm_model_collection._process_model_parameters(model.id, model_parameters)
            self.assertEqual(len(processed_parameters), len(model_parameters))
            for parameter_name in processed_parameters:
                self.assertTrue(parameter_name in model_parameters)

    def test_process_model_parameters_use_template(self):
        models = self.llm_model_collection.get_models()
        for model in models:
            model_parameters = {}
            if model.parameter_configs:
                # use the first parameter as a template for the second parameter
                model.parameter_configs[0].use_template = model.parameter_configs[1].name
                model_parameters[model.parameter_configs[1].name] = model.parameter_configs[1].default
                # model.parameter_configs = [{'name': 'temperature', 'use_template': 'top_p'}, {'name': 'top_p', 'use_template': 'top_p'}]
                # model_parameters = {'top_p': 0.9} => processed_parameters = {'temperature': 0.9, 'top_p': 0.9}
                processed_parameters = self.llm_model_collection._process_model_parameters(model.id, model_parameters)
                # parameter with use_template should be processed
                self.assertEqual(len(processed_parameters), len(model.parameter_configs))
                # the second parameter should have the same value as the first parameter
                self.assertEqual(processed_parameters[model.parameter_configs[0].name], model.parameter_configs[1].default)

    def test_process_model_parameters_validation_error(self):
        models = self.llm_model_collection.get_models()
        for model in models:
            model_parameters = {}
            for parameter_config in model.parameter_configs:
                model_parameters[parameter_config.name] = parameter_config.max + 1
            if model.parameter_configs:
                with self.assertRaises(ValueError):
                    self.llm_model_collection._process_model_parameters(model.id, model_parameters)
            else:
                self.assertEqual(len(self.llm_model_collection._process_model_parameters(model.id, model_parameters)), 0)

    def test_call(self):
        models = self.llm_model_collection.get_models()
        for model in models:
            messages = [
                UserMessage(content='hello'),
                AssistantMessage(content='world'),
            ]
            input = self.llm_model_collection.get_tokens_count(model.id, {}, messages)
            output = self.llm_model_collection.get_tokens_count(model.id, {}, [self.llm_model_collection.RESPONSE])
            result = self.llm_model_collection.call(model.id, {}, messages, {})
            self.assertIsNotNone(result)
            self.assertIsNotNone(result.usage)
            self.assertEqual(result.model, model.id)
            self.assertEqual(result.messages, messages)
            self.assertEqual(result.message, self.llm_model_collection.RESPONSE)
            if model.pricing is None:
                self.assertEqual(result.usage.total_price, 0)
            else:
                self.assertEqual(result.usage.total_tokens, input+output)
                total = input * model.pricing.unit * model.pricing.input + output * model.pricing.unit * model.pricing.output
                self.assertEqual(result.usage.total_price, total)
