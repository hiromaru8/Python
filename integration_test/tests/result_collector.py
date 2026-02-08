import json
import hashlib
import platform
import sys
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
            "environment": cls._get_environment_info(),
            "total"     : len(cls.results),
            "success"   : len([r for r in cls.results if r["status"] == "SUCCESS"]),
            "fail"      : len([r for r in cls.results if r["status"] == "FAIL"]),
            "error"     : len([r for r in cls.results if r["status"] == "ERROR"]),
            "results"   : cls.results
        }

        output_path = report_dir / filename

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(output, f, indent=4, ensure_ascii=False)

        # ハッシュ生成
        hash_value = cls._generate_sha256(output_path)

        # ハッシュ保存
        with open(str(output_path) + ".sha256", "w", encoding="utf-8") as f:
            f.write(hash_value)

        return output_path


    @staticmethod
    def _generate_sha256(file_path):
        sha256 = hashlib.sha256()

        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256.update(chunk)

        return sha256.hexdigest()


    @staticmethod
    def _get_environment_info():
        return {
            "os": platform.system(),
            "os_version": platform.version(),
            "platform": platform.platform(),
            "hostname": platform.node(),
            "cpu": platform.processor(),
            "python_version": platform.python_version(),
            "python_implementation": platform.python_implementation(),
            "python_executable": sys.executable
        }

