import secrets
import os
import pytest
import sqlite3

from sqlite.database.context import DatabaseContext
from sqlite.database.schema import TableSchema
from sqlite.database.strategy.sqlite import SQLiteStrategy
from sqlite.database.table.generic_table_strategy import GenericTableStrategy

from sqlite.util.combination import gen_unique_pairs

from pathlib import Path

# このソースファイル自身の場所
BASE_DIR = Path(__file__).resolve().parent
test_db_path = os.path.join(BASE_DIR, "test_initialize.db")

# =========================
# テーブルスキーマ定義
# （テーブル構成が変わったらここだけ修正）
# =========================
combination_schema = TableSchema(
    table_name="combination_unit",
    columns={
        "src_id": "INTEGER",
        "dest_id": "INTEGER",
        "data1": "BLOB",
        "data2": "BLOB",
    },
    primary_keys=["src_id", "dest_id"]
)

single_schema = TableSchema(
    table_name="single_unit",
    columns={
        "id": "INTEGER",
        "data1": "BLOB",
        "data2": "BLOB",
    },
    primary_keys=["id"]
)

schemas = [combination_schema, single_schema]


def test_1():
    """初回作成（初期化）テスト
    """
    RECORD_COUNT = 4
    # =========================
    # DB 初期化
    # recreate=True → テーブル再作成
    # =========================
    db = DatabaseContext(
            SQLiteStrategy(":memory:"),# メモリ上に新規作成(クローズで消える。接続ごとに別のDB)
            schemas=schemas,
            initialize=True,
            recreate=True
            )

    # =========================
    # 汎用 Table Strategy 作成
    # =========================
    single_table        = GenericTableStrategy(single_schema)

    # =========================
    # レコード追加
    # =========================
    for id in range(1,RECORD_COUNT + 1):
        data3 = secrets.token_bytes(16)
        data4 = secrets.token_bytes(4)  
        single_table.insert(
            db.conn,
            id=id,
            data1=data3,
            data2=data4
            )

    assert RECORD_COUNT == single_table.count_all(db.conn)
    
    # =========================
    # DB クローズ
    # =========================
    db.close()


def test_2():
    """再作成（初期化）テスト
    """
    RECORD_COUNT = 4

    # =========================
    # DB 初期化
    # recreate=True → テーブル再作成
    # =========================
    db = DatabaseContext(
            SQLiteStrategy(test_db_path),# メモリ上に新規作成(クローズで消える。接続ごとに別のDB)
            schemas=schemas,
            initialize=True,
            recreate=True
            )

    # =========================
    # 汎用 Table Strategy 作成
    # =========================
    single_table        = GenericTableStrategy(single_schema)

    # =========================
    # レコード追加
    # =========================
    for id in range(1,5):
        data3 = secrets.token_bytes(16)
        data4 = secrets.token_bytes(4)  
        single_table.insert(
            db.conn,
            id=id,
            data1=data3,
            data2=data4
            )
    db = DatabaseContext(
            SQLiteStrategy(test_db_path),# メモリ上に新規作成(クローズで消える。接続ごとに別のDB)
            schemas=schemas,
            recreate=False
            )
    # レコードが残っていることを確認
    assert RECORD_COUNT == single_table.count_all(db.conn)
    # レコードが重複して追加できないことを確認
    with pytest.raises(sqlite3.IntegrityError):
        for id in range(1,RECORD_COUNT + 1):
            data3 = secrets.token_bytes(16)
            data4 = secrets.token_bytes(4)  
            single_table.insert(
                db.conn,
                id=id,
                data1=data3,
                data2=data4
                )
    
    db.close()


def test_3():
    """再作成（初期化）テスト
    """
    RECORD_COUNT = 4

    test_2()  # まずは test_2 を実行して DB 作成
    # =========================
    # DB 初期化
    # recreate=True → テーブル再作成
    # =========================
    db = DatabaseContext(
            SQLiteStrategy(test_db_path),# メモリ上に新規作成(クローズで消える。接続ごとに別のDB)
            schemas=schemas,
            initialize=False
            )

    # =========================
    # 汎用 Table Strategy 作成
    # =========================
    single_table        = GenericTableStrategy(single_schema)

    # レコードが残っていることを確認
    assert RECORD_COUNT == single_table.count_all(db.conn)

    # =========================
    # レコード追加
    # =========================
    with pytest.raises(sqlite3.IntegrityError):
        for id in range(1,RECORD_COUNT + 1):
            data3 = secrets.token_bytes(16)
            data4 = secrets.token_bytes(4)  
            single_table.insert(
                db.conn,
                id=id,
                data1=data3,
                data2=data4
                )

    
    db.close()