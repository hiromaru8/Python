import json
from pathlib import Path
from datetime import datetime


class ResultCollector:
    results = []

    @classmethod
    def add_result(cls, result):
        """
            Adds a test result to the collection.
        Args:
            result (_type_): The test result to be added.
        """
        cls.results.append(result)

    @classmethod
    def save_json(cls, filename=None):
        """
            JSON fileに結果を保存する。
        
        :param cls: 結果を保持するクラス変数resultsを使用する。
        """
        report_dir = Path("reports")
        report_dir.mkdir(exist_ok=True)

        # デフォルトファイル名
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"integration_result_{timestamp}.json"

        output = {
            "generated_at": datetime.now().isoformat(),
            "total": len(cls.results),
            "results": cls.results
        }

        output_path = report_dir / filename

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(output, f, indent=4, ensure_ascii=False)

        return output_path
