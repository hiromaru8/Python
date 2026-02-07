from typing import List

from sqlite.database.strategy.sqlite import DatabaseStrategy
from sqlite.database.schema import TableSchema

class DatabaseContext:
    """
    DatabaseStrategy を利用する Context クラス
    """

    def __init__(
        self,
        db_strategy : DatabaseStrategy,
        schemas     : List[TableSchema],
        initialize  : bool = True,
        recreate    : bool = False,
        ):
        """_summary_

        Args:
            db_strategy (DatabaseStrategy): db strategy インスタンス
            schemas (List[TableSchema]): テーブルスキーマリスト
            recreate (bool, optional): テーブル再作成フラグ. Defaults to False. 
        """
        
        self.db_strategy    = db_strategy
        self.conn           = self.db_strategy.connect()
        if initialize:
            self.db_strategy.initialize(
                self.conn,
                schemas     = schemas,
                recreate    = recreate
            )

    def close(self):
        self.conn.close()
