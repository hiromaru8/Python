# result_collector.py
import json
import hashlib
import platform
import sys
from pathlib import Path
from datetime import datetime


class ResultCollector:
    
    def __init__(self):
        self.results = []

    def add_result(self, result):
        self.results.append(result)

    def save_json(self, filename=None):
        
        report_dir = Path("reports")
        report_dir.mkdir(exist_ok=True)

        # デフォルトファイル名
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"integration_result_{timestamp}.json"

        output = {
            "meta" : {
                "generated_at": datetime.now().isoformat(),
                "environment": self._get_environment_info()
            },
            "summary": {
                "total": len(self.results),
                "success": len([r for r in self.results if r["status"] == "SUCCESS"]),
                "fail": len([r for r in self.results if r["status"] == "FAIL"]),
                "error": len([r for r in self.results if r["status"] == "ERROR"]),
            },
            "results"   : self.results
        }

        output_path = report_dir / filename

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(output, f, indent=4, ensure_ascii=False)

        # ハッシュ生成
        hash_value = self._generate_sha256(output_path)
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

