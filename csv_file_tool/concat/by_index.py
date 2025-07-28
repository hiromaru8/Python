import pandas as pd
from typing import List
from csv_file_tool.concat.base import ConcatStrategy

class ConcatByIndexStrategy(ConcatStrategy):
    """
    DataFrameをインデックスに基づいて横方向（列方向）に結合する戦略。
    同じインデックスに対して列を追加する形で統合。
    """

    def concat(self, dfs: List[pd.DataFrame]) -> pd.DataFrame:
        df = pd.concat(dfs, axis=1)
        df.dropna(how='all', inplace=True)  # 全ての値がNaNの行を削除
        return df