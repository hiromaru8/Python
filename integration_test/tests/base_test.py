# base_test.py
import unittest
import logging
import time

class TestLoggerAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        return f"[{self.extra['test_id']}] {msg}", kwargs


class BaseIntegrationTest(unittest.TestCase):
    """ Base class for integration tests.

    """

    TEST_ID = ""

    # メソッドごとにセットアップ
    def setUp(self):
        
        # 開始時間を記録
        self._start_time = time.perf_counter()

        # ロガーの設定
        base_logger = logging.getLogger(self.__class__.__module__)
        self.logger = TestLoggerAdapter(
            base_logger,
            {"test_id": self.TEST_ID}
        )

        # 
        self.logger.info("START")


    # メソッドごとにティアダウン（後処理）
    def tearDown(self):
        # 経過時間を計算
        duration = time.perf_counter() - self._start_time
        self.logger.info("END (%.3f sec)", duration)
       