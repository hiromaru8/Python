import unittest
import logging


class TestLoggerAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        return f"[{self.extra['test_id']}] {msg}", kwargs


class BaseIntegrationTest(unittest.TestCase):
    """ Base class for integration tests.

    """

    TEST_ID = ""

    # メソッドごとにセットアップ
    def setUp(self):
        base_logger = logging.getLogger(self.__class__.__module__)
        self.logger = TestLoggerAdapter(
            base_logger,
            {"test_id": self.TEST_ID}
        )
        self.logger.info("START")

    # メソッドごとにティアダウン（後処理）
    def tearDown(self):
        self.logger.info("END")
