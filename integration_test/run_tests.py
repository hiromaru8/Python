# run_tests.py
import json
import datetime
import logging
import sys
import unittest
import argparse
import time
from pathlib import Path

from src.utils.logger import setup_logger
from tests.result_collector import ResultCollector

BASE_DIR = Path(__file__).parent


def load_test_selection():
    path = BASE_DIR / "config" / "test_selection.json"
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        logging.warning("test_selection.json not found.")
        data = {}
        
    return data

def iter_testcases(suite):
    for item in suite:
        if isinstance(item, unittest.TestSuite):
            yield from iter_testcases(item)
        else:
            yield item

def discover_and_filter_tests(selected_ids):
    loader = unittest.TestLoader()
    discovered = loader.discover("tests")

    suite = unittest.TestSuite()

    for test_case in iter_testcases(discovered):
        test_class = test_case.__class__
        test_id = getattr(test_class, "TEST_ID", None)

        # 選択されたIDに基づいてフィルタリング
        # selected_idsが空の場合は全て実行
        if not selected_ids or test_id in selected_ids:
            suite.addTest(test_case)


    return suite

class IntegrationTestResult(unittest.TextTestResult):

    def __init__(self, *args, collector=None, **kwargs):
        """ カスタムテスト結果クラス
         :param collector: ResultCollectorインスタンス
         """
        super().__init__(*args, **kwargs)
        self.successes = []
        self.collector = collector

    def startTest(self, test):
        """ テスト開始時の処理
            :param test: 実行されるテストケース
        """
        test._start_time = time.perf_counter()
        super().startTest(test)

    def addSuccess(self, test):
        """ テスト成功時の処理
            :param test: 成功したテストケース
        """
        duration = self._calc_duration(test)
        self.successes.append(test)
        self._record(test, "SUCCESS", duration)

    def addFailure(self, test, err):
        """ テスト失敗時の処理
            :param test: 失敗したテストケース
            :param err: 例外情報のタプル (type, value, traceback)
        """
        duration = self._calc_duration(test)
        self._record(test, "FAIL", duration, err)
        super().addFailure(test, err)

    def addError(self, test, err):
        """ テストエラー時の処理
            :param test: エラーが発生したテストケース
            :param err: 例外情報のタプル (type, value, traceback)
        """
        duration = self._calc_duration(test)
        self._record(test, "ERROR", duration, err)
        super().addError(test, err)

    def _calc_duration(self, test):
        """ テストケースの実行時間を計算
            :param test: テストケース
            :return: 実行時間（秒）
        """
        return round(time.perf_counter() - test._start_time, 3)

    def _record(self, test, status, duration, err=None):
        """ テスト結果をResultCollectorに記録
            :param test: テストケース
            :param status: 結果ステータス ("SUCCESS", "FAIL", "ERROR")
            :param duration: 実行時間（秒）
            :param err: 例外情報のタプル (type, value, traceback)（失敗・エラー時のみ）
        """
        exception_type = None
        error_message = None
        traceback_text = None

        # 例外情報の抽出
        if err:
            exc_type, exc_value, tb = err
            exception_type = exc_type.__name__
            error_message = str(exc_value)
            traceback_text = self._exc_info_to_string(err, test)
        
        test_id = getattr(test.__class__, "TEST_ID", None)
        if not test_id:
            raise ValueError(f"{test.__class__.__name__} has no TEST_ID")
        
        # 結果をResultCollectorに追加
        if self.collector:
            self.collector.add_result({
                "test_id": test_id,
                "class": test.__class__.__name__,
                "method": test._testMethodName,
                "status": status,
                "duration_sec": duration,
                "exception_type": exception_type,
                "error_message": error_message,
                "traceback": traceback_text
            })


def main():
    # コマンドライン引数の解析
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--report", "-r",
        help="Output JSON report filename (e.g. result.json)"
    )
    args = parser.parse_args()    
    
    # ロガーの設定
    setup_logger()

    # テスト選択の読み込み
    selection = load_test_selection()
    selected_ids = set(selection.get("execute", []))

    # テスト実行の開始ログ
    logging.info("=== Integration Test Start ===")
    logging.info("Tester: %s", selection.get("tester"))
    logging.info("Target Version: %s", selection.get("target_version"))
    logging.info("Selected IDs: %s", sorted(selected_ids))

    # テスト実行
    start_time = datetime.datetime.now()
    
    # テストスイートの構築
    suite = discover_and_filter_tests(selected_ids)
    # テストケースがない場合は警告を出して終了
    if suite.countTestCases() == 0:
        logging.warning("No test cases selected.")
        print("No test cases selected.")
        sys.exit(1)

    # カスタムテストランナーの使用
    collector = ResultCollector()
    # テストランナーの作成
    runner = unittest.TextTestRunner(
        verbosity=2,
        resultclass=lambda *args, **kwargs:
            IntegrationTestResult(
                *args,
                collector=collector,
                **kwargs
            )
    )
    # テストの実行
    result = runner.run(suite)
    # テスト実行の終了ログ
    end_time = datetime.datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    logging.info("Ran       : %d", result.testsRun)
    logging.info("Successes : %d", len(result.successes)) 
    logging.info("Failures  : %d", len(result.failures))
    logging.info("Errors    : %d", len(result.errors))
    logging.info("Total Duration  : %.3f sec", duration)
    logging.info("=== Integration Test End ===")
    
    # 結果のJSON保存
    output_path = collector.save_json(filename=args.report)
    print(f"JSON report saved to: {output_path}")

    # 終了コードの設定
    if not result.wasSuccessful():
        sys.exit(1)


if __name__ == "__main__":
    main()