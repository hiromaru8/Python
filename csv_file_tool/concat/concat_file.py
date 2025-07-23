from typing import List

import pandas as pd

from csv_file_tool.concat.by_index import ConcatByIndexStrategy
from csv_file_tool.concat.base import ConcatStrategy

class Concat:
    def __init__(self, strategy: ConcatStrategy, columns: List[str] = None):
        self.strategy = strategy
        self.columns = columns

    def run(self, file_paths: List[str]) -> pd.DataFrame:
        # ファイルパスからDataFrameを読み込む
        dfs = [pd.read_csv(path, usecols=self.columns) for path in file_paths if isinstance(path, str)]
        return self.strategy.concat(dfs)
    
    


if __name__ == "__main__":
    # ワイルドカード指定でCSVファイル一覧取得
    import glob
    file_paths = glob.glob("concat*.csv")
    print(file_paths)
    concat = Concat(ConcatByIndexStrategy())
    result_df = concat.run(file_paths)
    result_df.to_csv("output.csv", index=True, index_label="No.")