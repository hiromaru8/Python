import sqlite3
from typing import List

from sqlite.database.strategy.base import DatabaseStrategy
from sqlite.database.schema import TableSchema


class SQLiteStrategy(DatabaseStrategy):
    """
    SQLite 用 DatabaseStrategy 実装
    """

    def __init__(self, db_path: str):
        self.db_path = db_path

    def connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def initialize(
        self,
        conn: sqlite3.Connection,
        schemas: List[TableSchema],
        recreate: bool = False
    ) -> None:
        cursor = conn.cursor()

        for schema in schemas:
            # 再作成オプションが有効な場合はテーブル削除
            if recreate:
                cursor.execute(
                    f"DROP TABLE IF EXISTS {schema.table_name};"
                )

            # カラム定義生成
            column_defs = [
                f"{name} {ctype}"
                for name, ctype in schema.columns.items()
            ]

            # 主キー定義生成
            pk_def = ""
            if schema.primary_keys:
                pk_cols = ", ".join(schema.primary_keys)
                pk_def = f", PRIMARY KEY ({pk_cols})"

            # CREATE TABLE 文生成
            ddl = f"""
            CREATE TABLE IF NOT EXISTS {schema.table_name} (
                {", ".join(column_defs)}
                {pk_def}
            );
            """

            cursor.execute(ddl)

        conn.commit()
