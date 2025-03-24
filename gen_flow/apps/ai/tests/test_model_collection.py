# Copyright (C) 2025 Reveal AI
#
# SPDX-License-Identifier: MIT

from os import path as osp
import decimal
from unittest import TestCase

from django.conf import settings

from gen_flow.apps.ai.tests.utils import DummyAIProvider, DummyModelCollection, create_dummy_model_config, remove_dummy_model_config
from gen_flow.apps.ai.base.entities.model import PricingType


class ModelCollectionTest(TestCase):
    @classmethod
    def setUpClass(cls):
        create_dummy_model_config()
        cls.model_type = 'llm'
        cls.config_path = osp.join(
            settings.MODEL_CONFIG_ROOT,
            DummyAIProvider.PROVIDER_FOLDER,
            cls.model_type
        )

    @classmethod
    def tearDownClass(cls):
        remove_dummy_model_config()

    def test_get_models(self):
        model_collection = DummyModelCollection()
        model_collection.config_path = self.config_path
        models = model_collection.get_models()
        listing = model_collection._get_listing()

        self.assertIsNotNone(models)
        self.assertEqual(len(models), len(listing))
        for key, value in listing.items():
            self.assertEqual(models[value].id, key)

    def test_get_model_schema(self):
        model_collection = DummyModelCollection()
        model_collection.config_path = self.config_path
        models = model_collection.get_models()
        for model in models:
            schema = model_collection.get_model_schema(model.id)
            self.assertIsNotNone(schema)
            self.assertEqual(schema.id, model.id)

    def test_get_price(self):
        model_collection = DummyModelCollection()
        model_collection.config_path = self.config_path
        models = model_collection.get_models()
        for model in models:
            if model.pricing is None:
                price = model_collection.get_price(model.id, PricingType.INPUT, 10)
                self.assertEqual(price.total_amount, 0)
            else:
                tokens = 10
                price = model_collection.get_price(model.id, PricingType.INPUT, tokens)
                self.assertIsNotNone(price)
                self.assertEqual(price.unit_price, model.pricing.input)
                total = tokens * model.pricing.unit * model.pricing.input
                total = total.quantize(decimal.Decimal('0.0000001'), rounding=decimal.ROUND_HALF_UP)
                self.assertEqual(price.total_amount, total)
                self.assertEqual(price.unit, model.pricing.unit)
