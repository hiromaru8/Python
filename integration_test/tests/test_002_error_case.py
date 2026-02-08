import unittest
import logging
from tests.base_test import BaseIntegrationTest


class TestErrorCase(BaseIntegrationTest):

    TEST_ID = "IT-002"

    def test_invalid_input(self):
        self.log_start()
        value = None
        self.assertIsNone(value)
        self.log_end()
