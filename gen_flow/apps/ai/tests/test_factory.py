# Copyright (C) 2025 Reveal AI
#
# SPDX-License-Identifier: MIT

from unittest import TestCase

from gen_flow.apps.ai.base.entities.provider import AIProviderEntity
from gen_flow.apps.ai.ai_provider_factory import AIProviderFactory


class RegisteredAIProviderTest(TestCase):
    @classmethod
    def setUpClass(cls):
        import gen_flow.apps.ai.tests.register_providers # noqa
        cls.ai_provider_factory = AIProviderFactory()

    def test_get_ai_provider_schemas(self):
        ai_provider_schemas = self.ai_provider_factory.get_ai_provider_schemas()
        self.assertIsNotNone(ai_provider_schemas)
        self.assertEqual(len(ai_provider_schemas), 1)
        self.assertEqual(len(ai_provider_schemas[0].models), 2)

    def test_get_ai_provider_instance(self):
        ai_provider_instance = self.ai_provider_factory.get_ai_provider_instance('dummy')
        self.assertIsNotNone(ai_provider_instance)

    def test_get_ai_provider_instance_invalid(self):
        with self.assertRaises(Exception):
            self.ai_provider_factory.get_ai_provider_instance('invalid_provider')

    def test_validate_credentials(self):
        ai_provider_schemas = self.ai_provider_factory.get_ai_provider_schemas()
        for ai_provider_schema in ai_provider_schemas:
            if not ai_provider_schema.credential_form:
                with self.assertRaises(ValueError):
                    self.ai_provider_factory.validate_credentials(ai_provider_schema.id, {})
            else:
                self.validate_credentials_valid(ai_provider_schema)
                self.validate_credentials_invalid(ai_provider_schema)
                self.validate_credentials_invalid_type(ai_provider_schema)

    def validate_credentials_valid(self, ai_provider_schema: AIProviderEntity):
        credentials = {}
        for configuration_input in ai_provider_schema.credential_form:
            if configuration_input.required:
                credentials[configuration_input.name] = 'test'
        filtered_credentials = self.ai_provider_factory.validate_credentials(ai_provider_schema.id, credentials)
        self.assertEqual(len(filtered_credentials), len(credentials))

    def validate_credentials_invalid(self, ai_provider_schema: AIProviderEntity):
        with self.assertRaises(ValueError):
            self.ai_provider_factory.validate_credentials(ai_provider_schema.id, {})

    def validate_credentials_invalid_type(self, ai_provider_schema: AIProviderEntity):
        credentials = {}
        for configuration_input in ai_provider_schema.credential_form:
            if configuration_input.required:
                credentials[configuration_input.name] = 10
        with self.assertRaises(ValueError):
            self.ai_provider_factory.validate_credentials(ai_provider_schema.id, credentials)
