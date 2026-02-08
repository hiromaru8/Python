import json
import datetime
import logging
import sys
import unittest
from pathlib import Path

from src.utils.logger import setup_logger


BASE_DIR = Path(__file__).parent


def load_test_selection():
    path = BASE_DIR / "config" / "test_selection.json"
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
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

        if test_id in selected_ids:
            suite.addTest(test_case)

    return suite

class IntegrationTestResult(unittest.TextTestResult):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.test_results = []

    def addSuccess(self, test):
        super().addSuccess(test)
        self._record(test, "SUCCESS")

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self._record(test, "FAIL")

    def addError(self, test, err):
        super().addError(test, err)
        self._record(test, "ERROR")

    def _record(self, test, status):
        test_id = getattr(test.__class__, "TEST_ID", None)
        self.test_results.append({
            "test_id": test_id,
            "test_name": test.id(),
            "status": status
        })

def save_json_report(result_obj):
    report = {
        "timestamp": datetime.datetime.now().isoformat(),
        "total": result_obj.testsRun,
        "results": result_obj.test_results
    }

    output_path = Path("reports") / "result.json"

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4, ensure_ascii=False)

def main():
    setup_logger()

    selection = load_test_selection()
    selected_ids = set(selection.get("execute", []))

    logging.info("=== Integration Test Start ===")
    logging.info("Tester: %s", selection.get("tester"))
    logging.info("Target Version: %s", selection.get("target_version"))
    logging.info("Selected IDs: %s", sorted(selected_ids))

    suite = discover_and_filter_tests(selected_ids)

    if suite.countTestCases() == 0:
        logging.warning("No test cases selected.")
        print("No test cases selected.")
        sys.exit(1)

    runner = unittest.TextTestRunner(
                verbosity=2,
                resultclass=IntegrationTestResult
                )
    result = runner.run(suite)
    save_json_report(result)
    
    logging.info("Ran       : %d", result.testsRun)
    logging.info("Successes : %d", len(result.successes) if hasattr(result, 'successes') else result.testsRun - len(result.failures) - len(result.errors))  
    logging.info("Failures  : %d", len(result.failures))
    logging.info("Errors    : %d", len(result.errors))
    logging.info("=== Integration Test End ===")

    if not result.wasSuccessful():
        sys.exit(1)


if __name__ == "__main__":
    main()