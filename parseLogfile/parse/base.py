from abc import ABC, abstractmethod
from pathlib import Path
import re
from typing import List
from typing import TypedDict, Callable
# -------------------------
# データモデル
# -------------------------
class LogRecord(TypedDict):
    datetime: str
    level: str
    message: str
    
# -------------------------
# 抽象クラス
# -------------------------
class LogParserStrategy(ABC):
    @abstractmethod
    def parse_line(self, line: str, current: LogRecord | None) -> tuple[LogRecord | None, LogRecord | None, bool]:
        """
        1行を解析し、レコードを返す。
        - 戻り値: (currentレコード, 完成したかどうか)
        """
        pass

class FilterStrategy(ABC):
    @abstractmethod
    def match(self, record: LogRecord) -> bool:
        """対象メッセージかどうかを判定"""
        pass


class PostProcessor(ABC):
    @abstractmethod
    def process(self, record: LogRecord) -> LogRecord:
        """抽出したメッセージを加工"""
        pass


# -------------------------
# 具象クラス（例: ログパーサ）
# -------------------------
class LogParser(LogParserStrategy):
    LOG_START_PATTERN = re.compile(
        r'^(?P<datetime>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3})\s'
        r'\[(?P<level>[A-Z]+)\]\s'
        r'(?P<message>.*)'
    )

    def __init__(self, filter: FilterStrategy | None = None):
        self.filter = filter

    def parse_line(self, line: str, current: LogRecord | None) -> tuple[LogRecord | None, LogRecord | None, bool]:
        line = line.rstrip("\n")

        m = self.LOG_START_PATTERN.match(line)
        if m:
            # 新しいレコード開始
            if current and self.filter.match(finished_log_message):
                finished_log_message = current
            else:
                finished_log_message = None

            new_record: LogRecord = {
                "datetime": m.group("datetime"),
                "level"   : m.group("level"),
                "message" : m.group("message"),
            }
            return new_record, finished_log_message, True

        else:
            # 続き
            if current:
                current["message"] += " " + line.strip()
            return current, None, False

# -------------------------
# フィルタ（例: 複数条件）
# -------------------------
class MultiPatternFilter(FilterStrategy):
    def __init__(self, patterns: list[str]):
        self.patterns = [re.compile(p) for p in patterns]

    def match(self, record: LogRecord) -> bool:
        return any(p.search(record["message"]) for p in self.patterns)


# -------------------------
# 加工処理（例: XMLを日本語に変換）
# -------------------------
import xml.etree.ElementTree as ET

class XmlToJapaneseMessageProcessor(PostProcessor):
    def process(self, record: LogRecord) -> LogRecord:
        msg = record["message"]
        try:
            root = ET.fromstring(msg)
            # 例: <message code="001">Hello</message> → 「001: こんにちは」
            if root.tag == "message":
                code = root.attrib.get("code", "")
                text = root.text or ""
                record["message"] = f"{code}: {self.translate(text)}"
        except ET.ParseError:
            pass
        return record

    def translate(self, text: str) -> str:
        table = {"Hello": "こんにちは", "Bye": "さようなら"}
        return table.get(text, text)



# -------------------------
# メイン処理
# -------------------------
def parse_log_file(
    filepath: str,
    output: str,
    parser: LogParserStrategy,
    filter_strategy: FilterStrategy,
    post_processor: PostProcessor | None = None,
) -> None:
    current: LogRecord | None = None

    with Path(filepath).open("r", encoding="utf-8") as in_f, Path(output).open("w", encoding="utf-8") as out_f:
        for line in in_f:
            current, finished_log_message, finished = parser.parse_line(line, current)
            if finished and current and filter_strategy.match(current):
                if post_processor:
                    current = post_processor.process(current)
                print(current)
                out_f.write(f"{current['datetime']} {current['level']} {current['message']}\n")

        # 最後のレコードも処理
        if current and filter_strategy.match(current):
            if post_processor:
                current = post_processor.process(current)
            out_f.write(f"{current['datetime']} {current['level']} {current['message']}\n")


# -------------------------
# 実行例
# -------------------------
if __name__ == "__main__":
    parser = LogParser()
    filter_strategy = MultiPatternFilter([r"message"])
    post_processor = XmlToJapaneseMessageProcessor()

    parse_log_file("./parseLogfile/parse/sample.log", "./parseLogfile/parse/sample_out1.log", parser, filter_strategy)