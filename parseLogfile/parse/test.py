import re
from pathlib import Path
import xml.etree.ElementTree as ET
from typing import TypedDict
from abc import ABC, abstractmethod
import csv


# ログ1行の開始パターン（Javaの一般的な形式）
LOG_START_PATTERN = re.compile(
    r'^(?P<datetime>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3})\s'
    r'\[(?P<level>[A-Z]+)\]\s'
    r'(?P<message>.*)'
)

# 抽出したいメッセージのパターン
MSG_PATTERN = re.compile(
    r'.*This.*'
)

class LogRecord(TypedDict):
    datetime    : str
    level       : str
    message     : str


# -------------------------
# フィルタ（例: 複数条件）
# -------------------------
class MultiPatternFilter():
    def __init__(self, patterns: list[str]):
        self.patterns = [re.compile(p) for p in patterns]

    def match(self, record: LogRecord) -> bool:
        return any(p.search(record["message"]) for p in self.patterns)


def parse_log_file(filepath: str,
                   output:str,
                   filter:MultiPatternFilter=MultiPatternFilter([r''])) -> None:
    current: LogRecord | None = None

    with Path(filepath).open("r", encoding="utf-8") as in_f ,Path(output).open("w", newline='', encoding="utf-8") as out_f:

        for line in in_f:
            line = line.rstrip("\n")
            
            m = LOG_START_PATTERN.match(line)
            if m:
                # 新しいレコード開始
                if current and filter.match(current):
                    # out_f.write(f"{current['datetime']} {current['level']} {current['message']}\n")
                    csv.writer(out_f).writerow([current['datetime'], current['level'], f'"{current['message']}"'])

                current = {
                    "datetime"  : m.group("datetime"),
                    "level"     : m.group("level"),
                    "message"   : m.group("message")
                }
            else:
                # 前のメッセージの続き
                if current:
                    current["message"] +=  line

        # 最後のレコードを追加
        if current:
            # msg = MSG_PATTERN.match(current["message"])
            msg = filter.match(current)
            if msg:
                # out_f.write(f"{current['datetime']} {current['level']} {current['message']}\n")
                csv.writer(out_f).writerow([current['datetime'], current['level'], f'"{current['message']}"'])

    return 




def parse_xml_message(message: str):
    """メッセージ部分がXMLならElementTreeでパース"""
    try:
        return ET.fromstring(message)
    except ET.ParseError:
        return None

# 使用例
if __name__ == "__main__":
    filter_strategy = MultiPatternFilter([r'.*This.*'])
    parse_log_file("parseLogfile/parse/sample.log", "parseLogfile/parse/sample_out_pre.csv", filter_strategy)
