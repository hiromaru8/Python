import unittest
import logging


class TestErrorCase(unittest.TestCase):

    TEST_ID = "IT-002"

    def test_invalid_input(self):
        logging.info("Executing %s", self.TEST_ID)

        value = None
        self.assertIsNone(value)
