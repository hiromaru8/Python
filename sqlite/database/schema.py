from typing import List
from dataclasses import dataclass

@dataclass(frozen=True)
class TableSchema:
    """
    テーブル構造を表すデータクラス
    """
    table_name: str
    columns: List[str]
    primary_keys: List[str]
    