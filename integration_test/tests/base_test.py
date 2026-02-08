import unittest
import logging

class BaseIntegrationTest(unittest.TestCase):

    TEST_ID = None

    def setUp(self):
        # 実際のテストクラスのモジュール名でロガーを作る
        self.logger = logging.getLogger(
                        f"{self.__class__.__module__}.{self.__class__.__name__}.{self._testMethodName}")
    def log_start(self):
        self.logger.info("[%s] START", self.TEST_ID)

    def log_end(self):
        self.logger.info("[%s] END", self.TEST_ID)