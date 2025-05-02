# Copyright (C) 2025 Reveal AI
#
# Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

from enum import Enum
from os import path as osp
from unittest import TestCase
from unittest.mock import patch

from django.conf import settings

from genflow.apps.ai.base.entities.shared import ModelType
from genflow.apps.ai.tests.utils import (
    DummyAIProvider,
    DummyModelCollection,
    create_dummy_model_config,
    remove_dummy_model_config,
)


class AIProviderTest(TestCase):
    @classmethod
    def setUpClass(cls):
        create_dummy_model_config()
        cls.dummy_provider = DummyAIProvider()
        cls.dummy_provider.config_path = osp.join(
            settings.MODEL_CONFIG_ROOT, DummyAIProvider.PROVIDER_FOLDER
        )
        cls.model_type = "llm"

    @classmethod
    def tearDownClass(cls):
        remove_dummy_model_config()

    def test_get_schema(self):
        schema = self.dummy_provider.get_schema()
        self.assertIsNotNone(schema)

    def test_get_schema_no_config_folder(self):
        dummy_provider = DummyAIProvider()
        dummy_provider.config_path = osp.join(settings.MODEL_CONFIG_ROOT, "no_folder")
        with self.assertRaises(Exception):
            dummy_provider.get_schema()

    def test_get_schema_no_config_file(self):
        dummy_provider = DummyAIProvider()
        dummy_provider.config_path = osp.join(settings.MODEL_CONFIG_ROOT, "no_config")
        with self.assertRaises(Exception):
            dummy_provider.get_schema()

    def test_get_schema_invalid_config(self):
        dummy_provider = DummyAIProvider()
        dummy_provider.config_path = osp.join(settings.MODEL_CONFIG_ROOT, "invalid")
        with self.assertRaises(Exception):
            dummy_provider.get_schema()

    def test_add_model_collection_instance(self):
        provider_name = self.dummy_provider.config_path.split("/")[-1]
        config_path = osp.join(self.dummy_provider.config_path, self.model_type)
        self.dummy_provider.add_model_collection_instance(config_path, DummyModelCollection)
        self.assertIn(
            f"{provider_name}.{self.model_type}", self.dummy_provider.model_collections_map
        )

    def test_add_model_collection_instance_invalid_subclass(self):
        config_path = osp.join(self.dummy_provider.config_path, self.model_type)
        with self.assertRaises(Exception):
            self.dummy_provider.add_model_collection_instance(config_path, DummyAIProvider)

    def test_add_model_collection_instance_invalid_model_type(self):
        config_path = osp.join(self.dummy_provider.config_path, "invalid")
        with self.assertRaises(Exception):
            self.dummy_provider.add_model_collection_instance(config_path, DummyModelCollection)

    def test_get_model_collection_instance(self):
        config_path = osp.join(self.dummy_provider.config_path, self.model_type)
        self.dummy_provider.add_model_collection_instance(config_path, DummyModelCollection)
        model_collection = self.dummy_provider.get_model_collection_instance(self.model_type)
        self.assertIsNotNone(model_collection)

    def test_get_model_collection_instance_invalid_model_type(self):
        config_path = osp.join(self.dummy_provider.config_path, self.model_type)
        self.dummy_provider.add_model_collection_instance(config_path, DummyModelCollection)
        with self.assertRaises(Exception):
            self.dummy_provider.get_model_collection_instance("invalid")

    def test_get_models(self):
        config_path = osp.join(self.dummy_provider.config_path, self.model_type)
        self.dummy_provider.add_model_collection_instance(config_path, DummyModelCollection)
        models = self.dummy_provider.get_models(self.model_type)
        self.assertIsNotNone(models)

    def test_get_models_invalid_model_type(self):
        config_path = osp.join(self.dummy_provider.config_path, self.model_type)
        self.dummy_provider.add_model_collection_instance(config_path, DummyModelCollection)
        with self.assertRaises(Exception):
            self.dummy_provider.get_models("invalid")

    def test_get_models_invalid_model_type2(self):
        config_path = osp.join(self.dummy_provider.config_path, self.model_type)
        self.dummy_provider.add_model_collection_instance(config_path, DummyModelCollection)
        with patch(
            "genflow.apps.ai.base.ai_provider.ModelType",
            new=Enum(
                "ModelType",
                {
                    **{name: name for name in ModelType._member_names_},
                    "NEW_MODEL_TYPE": "new_model_type",
                },
            ),
        ):
            models = self.dummy_provider.get_models("new_model_type")
            self.assertEqual(models, [])
