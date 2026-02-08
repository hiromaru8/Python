import unittest
import logging
import time
from tests.result_collector import ResultCollector

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

        # 成功/失敗/エラー判定
        status = "SUCCESS"
        if hasattr(self, "_outcome"):
            result = self._outcome.result
            errors = result.errors
            failures = result.failures

            # エラー・失敗の確認
            # エラーの確認
            for test, _ in errors:
                if test is self:
                    status = "ERROR"
            # 失敗の確認
            for test, _ in failures:
                if test is self:
                    status = "FAIL"

        self.logger.info("END (%.3f sec) -> %s", duration, status)
        
        ResultCollector.add_result({
            "test_id"       : self.TEST_ID,
            "class"         : self.__class__.__name__,
            "method"        : self._testMethodName,
            "status"        : status,
            "duration_sec"  : round(duration, 3)
        })