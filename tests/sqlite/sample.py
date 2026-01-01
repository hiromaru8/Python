import secrets

from sqlite.database.context import DatabaseContext
from sqlite.database.schema import TableSchema
from sqlite.database.strategy.sqlite import SQLiteStrategy
from sqlite.database.table.generic_table_strategy import GenericTableStrategy

from sqlite.util.combination import gen_unique_pairs

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


def main():

    # =========================
    # DB 初期化
    # recreate=True → テーブル再作成
    # =========================
    db = DatabaseContext(
            SQLiteStrategy(":memory:"),
            schemas=schemas,
            recreate=True
            )

    # =========================
    # 汎用 Table Strategy 作成
    # =========================
    combination_table   = GenericTableStrategy(combination_schema)
    single_table        = GenericTableStrategy(single_schema)

    # =========================
    # レコード追加
    # =========================
    for src_id, dest_id in gen_unique_pairs(5):
        data1 = secrets.token_bytes(32)
        data2 = secrets.token_bytes(2)
        combination_table.insert(
            db.conn,
            src_id=src_id,
            dest_id=dest_id,
            data1=data1,
            data2=data2
        )

    for id in range(1,5):
        data3 = secrets.token_bytes(16)
        data4 = secrets.token_bytes(4)  
        single_table.insert(
            db.conn,
            id=id,
            data1=data3,
            data2=data4
            )

    # =========================
    # レコード更新
    # =========================
    single_table.update(
        db.conn,
        id=10,
        data1=b"\xCC",
        data2=b"\xDD"
    )

    # =========================
    # 全カラム取得
    # =========================
    print("single_unit all:")
    print(single_table.select_all(db.conn))



    combination_table.delete_by_pk(
        db.conn,
        src_id=1,
        dest_id=2
    )
    
    # =========================
    # 特定カラム取得
    # =========================
    print("combination_unit src_id, dest_id:")
    print(
        combination_table.select_columns(
            db.conn,
            columns=["src_id", "dest_id", "data2"]
        )
    )

    # =========================
    # DB クローズ
    # =========================
    db.close()


if __name__ == "__main__":
    main()

