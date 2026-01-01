import sqlite3
from abc import ABC, abstractmethod
from typing import List

from sqlite.database.schema import TableSchema


class DatabaseStrategy(ABC):
    """
    データベース初期化処理の Strategy インタフェース
    """

    @abstractmethod
    def connect(self) -> sqlite3.Connection:
        pass

    @abstractmethod
    def initialize(
        self,
        conn: sqlite3.Connection,
        schemas: List[TableSchema],
        recreate: bool = False
    ) -> None:
        """
        Args:
            conn:
                DB接続オブジェクト
            schemas:
                作成対象のテーブルスキーマ一覧
            recreate:
                True の場合、既存テーブルを削除して再作成する
        """
        pass