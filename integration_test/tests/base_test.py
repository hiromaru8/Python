import unittest
import logging
import time
import re
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
        error_message = None    
        traceback_text = None
        exception_type = None
        
        # 結果の解析
        if hasattr(self, "_outcome"):
            result      = self._outcome.result

            # エラー・失敗の確認
            # エラーの確認
            for test, tb in result.errors:
                if test is self:
                    status = "ERROR"
                    traceback_text = tb
                    exception_type, error_message = self._parse_traceback(tb)
                    
            # 失敗の確認
            for test, tb in result.failures:
                if test is self:
                    status = "FAIL"
                    traceback_text = tb
                    exception_type, error_message = self._parse_traceback(tb)

        self.logger.info("END (%.3f sec) -> %s", duration, status)
        
        ResultCollector.add_result({
            "test_id": self.TEST_ID,
            "class": self.__class__.__name__,
            "method": self._testMethodName,
            "status": status,
            "duration_sec": round(duration, 3),
            "exception_type": exception_type,
            "error_message": error_message,
            "traceback": traceback_text
        })
        
    @staticmethod
    def _parse_traceback(traceback_text):
        if not traceback_text:
            return None, None

        lines = traceback_text.strip().split("\n")
        last_line = lines[-1] if lines else ""

        # 例: AssertionError: 400 != 200
        match = re.match(r"(\w+):\s*(.*)", last_line)

        if match:
            return match.group(1), match.group(2)

        return None, last_line