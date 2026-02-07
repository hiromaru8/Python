from sqlite.database.schema import TableSchema


class GenericTableStrategy:
    """
    テーブル構造に依存しない汎用 CRUD Strategy クラス。

    ・テーブル名、カラム構成、主キー情報は TableSchema に集約する
    ・本クラスは SQL を動的に生成することで、テーブル構成変更に耐える
    ・テーブルごとの個別 Strategy を作らずに再利用できる
    """

    def __init__(self, schema: TableSchema):
        """
        Args:
            schema (TableSchema):
                操作対象テーブルのスキーマ定義
        """
        self.schema = schema

    def insert(self, conn, **values):
        """
        レコードを 1 件追加する。

        ・TableSchema に定義されたすべてのカラムを対象とする
        ・values にはカラム名をキーとして値を指定する
        ・主キーが既存の場合の挙動は DB 定義（制約）に依存する

        Args:
            conn:
                sqlite3.Connection オブジェクト
            **values:
                カラム名 = 値 の形式で指定するパラメータ
        """
        # スキーマからカラム順を取得
        columns = list(self.schema.columns.keys())

        # INSERT 文の列定義とプレースホルダ生成
        cols = ", ".join(columns)
        placeholders = ", ".join("?" for _ in columns)

        # INSERT 文を動的に生成
        sql = f"""
        INSERT INTO {self.schema.table_name}
        ({cols})
        VALUES ({placeholders});
        """

        # スキーマ順に値を並べ替えて SQL に渡す
        params = tuple(values[col] for col in columns)

        conn.execute(sql, params)
        conn.commit()

    def update(self, conn, **values):
        """
        主キーを条件にレコードを更新する。

        ・主キー以外のカラムを UPDATE 対象とする
        ・WHERE 句は TableSchema.primary_keys から自動生成される
        ・values には主キーおよび更新対象カラムの両方を含める必要がある

        Args:
            conn:
                sqlite3.Connection オブジェクト
            **values:
                カラム名 = 値 の形式で指定するパラメータ
        """
        # 更新対象カラム（主キー以外）
        set_cols = [
            c for c in self.schema.columns.keys()
            if c not in self.schema.primary_keys
        ]

        # SET 句と WHERE 句を動的生成
        set_clause = ", ".join(f"{c}=?" for c in set_cols)
        where_clause = " AND ".join(
            f"{pk}=?" for pk in self.schema.primary_keys
        )

        sql = f"""
        UPDATE {self.schema.table_name}
        SET {set_clause}
        WHERE {where_clause};
        """

        # SET 用パラメータ → WHERE 用パラメータの順で結合
        params = (
            tuple(values[c] for c in set_cols) +
            tuple(values[pk] for pk in self.schema.primary_keys)
        )

        conn.execute(sql, params)
        conn.commit()

    def select_columns(self, conn, columns):
        """
        指定したカラムのみを取得する。

        Args:
            conn:
                sqlite3.Connection オブジェクト
            columns (list[str]):
                取得したいカラム名のリスト

        Returns:
            list[tuple]:
                取得結果（行単位のタプル）
        """
        col = ", ".join(columns)

        cursor = conn.execute(
            f"SELECT {col} FROM {self.schema.table_name};"
        )
        return cursor.fetchall()

    def select_all(self, conn):
        """
        テーブル内の全カラム・全レコードを取得する。

        Args:
            conn:
                sqlite3.Connection オブジェクト

        Returns:
            list[tuple]:
                取得結果（行単位のタプル）
        """
        cursor = conn.execute(
            f"SELECT * FROM {self.schema.table_name};"
        )
        return cursor.fetchall()
    
    def count_all(self, conn):
        """
        テーブル内の全レコード数を取得する。

        Args:
            conn:
                sqlite3.Connection オブジェクト

        Returns:
            int:
                レコード数
        """
        cursor = conn.execute(
            f"SELECT COUNT(*) FROM {self.schema.table_name};"
        )
        result = cursor.fetchone()
        return result[0] if result else 0
    
    def select_by_pk(self, conn, **pk_values):
        """
        主キーを指定してレコードを取得する。
        """
        where_clause = " AND ".join(
            f"{pk}=?" for pk in self.schema.primary_keys
        )

        sql = f"""
        SELECT * FROM {self.schema.table_name}
        WHERE {where_clause};
        """

        params = tuple(pk_values[pk] for pk in self.schema.primary_keys)

        cursor = conn.execute(sql, params)
        return cursor.fetchone()
    
    def delete_by_pk(self, conn, **pk_values):
        """
        主キーを指定してレコードを削除する。
        """
        where_clause = " AND ".join(
            f"{pk}=?" for pk in self.schema.primary_keys
        )

        sql = f"""
        DELETE FROM {self.schema.table_name}
        WHERE {where_clause};
        """

        params = tuple(pk_values[pk] for pk in self.schema.primary_keys)

        conn.execute(sql, params)
        conn.commit()


    def exists_by_pk(self, conn, **pk_values) -> bool:
        """
        主キーを指定してレコードの存在確認を行う。
        Returns:
            bool: レコードが存在する場合は True、存在しない場合は False
        """
        where_clause = " AND ".join(
            f"{pk}=?" for pk in self.schema.primary_keys
        )

        sql = f"""
        SELECT 1
        FROM {self.schema.table_name}
        WHERE {where_clause}
        LIMIT 1;
        """

        params = tuple(pk_values[pk] for pk in self.schema.primary_keys)

        cursor = conn.execute(sql, params)
        return cursor.fetchone() is not None
    
    
