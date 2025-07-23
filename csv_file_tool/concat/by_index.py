import pandas as pd
from typing import List
from csv_file_tool.concat.base import ConcatStrategy

class ConcatByIndexStrategy(ConcatStrategy):
    """
    DataFrameをインデックスに基づいて横方向（axis=1）に結合する戦略。
    """
    def concat(self, dfs: List[pd.DataFrame]) -> pd.DataFrame:
        return pd.concat(dfs, axis=1)
