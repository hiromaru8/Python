"""
インデックスによって結合（concat）する戦略
列方向の結合を行う。
"""

import pandas as pd
from csv_file_tool.concat.base import ConcatStrategy

class ConcatByIndexStrategy(ConcatStrategy):
    """
    DataFrameをインデックスに基づいて横方向（列方向）に単純結合する戦略。
    df1, df2, ... を pd.concat(..., axis=1) で結合。
    """
    def execute(self, in_filepath_list: str) -> list[str]:
        df_list = self._read_csv_files(in_filepath_list)
        merged_df = pd.concat(df_list, axis=1)

        merged_df.to_csv("concat_output.csv", index=True, index_label="No.")

        return merged_df
    

    
    def _read_csv_files(self, in_filepath_list: str) -> list[pd.DataFrame]:
        """
        指定されたCSVファイルを読み込み、DataFrameのリストを返す。
        
        Args:
            in_filepath_list (str): CSVファイルのパス
        
        Returns:
            list[pd.DataFrame]: 読み込まれたDataFrameのリスト
        """
        df_list = []
        for file in in_filepath_list:
            df = pd.read_csv(file)
            df_list.append(df)
        
        return df_list