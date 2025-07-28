from typing import List
from typing import Optional
import pandas as pd
from pathlib import Path

from csv_file_tool.concat.by_index import ConcatByIndexStrategy
from csv_file_tool.concat.base import ConcatStrategy

class CSVConcatExecutor:
    def __init__(self, strategy: ConcatStrategy, 
                 output_path: str, 
                 columns: Optional[list[str]] = None,
                 index_name: Optional[str] = None):
        
        self.strategy       = strategy
        self.output_path    = output_path
        self.columns        = columns
        self.index_name     = index_name
        if self.columns:
            if not isinstance(self.columns, list):
                raise ValueError("columns must be a list of column names to select from each CSV file.")
        if not self.output_path.endswith('.csv'):
            raise ValueError("output_path must end with '.csv' to save the concatenated result as a CSV file.")

    def run(self, file_paths: List[str]) -> Optional[List[str]]:
        try:
            if not file_paths:
                raise ValueError("ファイルパスのリストが空です。少なくとも1つのCSVファイルを指定してください。")
            

            # ファイルパスからDataFrameを読み込む
            dfs = self._load_csv_files(file_paths)


            # DataFrameを結合する
            if not dfs:
                raise ValueError("No valid DataFrames to concatenate.")
            result_df = self.strategy.concat(dfs)
            
            
            # インデックスをリセットしてNo.列を追加
            # インデックス名が指定されている場合はその名前に変更
            # インデックス名が指定されていない場合はindexは無し
            if self.index_name:
                result_df.reset_index(drop=False, inplace=True)
                result_df.rename(columns={'index': self.index_name}, inplace=True)


            # 結果をCSVファイルに保存
            output_dir = Path(self.output_path).parent
            output_dir.mkdir(parents=True, exist_ok=True)
            result_df.to_csv(self.output_path, index=False, encoding='utf-8')
            
            return [str(self.output_path)]  
            
        except Exception as e:
            print(f"An error occurred during concatenation: {e}")
            return None

    def _load_csv_files(self, file_paths: List[str]) -> List[pd.DataFrame]:
        """
        複数のCSVファイルをDataFrameとして読み込む。
        このメソッドは、指定された各CSVファイルから指定されたカラムを読み込み、
        DataFrameのリストを返します。
        ファイルが読み込めない場合や、指定されたカラムが存在しない場合は、
        ValueError を発生させます。
        
        Args:
            file_paths (List[str]):  読み込むCSVファイルのパスのリスト。

        Raises:
            ValueError: CSVファイルが読み込めない場合、または指定したカラムが見つからない場合。

        Returns:
            List[pd.DataFrame]: 読み込まれたCSVファイルのDataFrameリスト。
        """
        df_list = []
        for path in file_paths:
            if not isinstance(path, str):
                continue
            try:
                # 指定されたカラムのみを読み込む
                df = pd.read_csv(path, usecols=self.columns)
                df_list.append(df)
            except ValueError as e:
                raise ValueError(f"ファイル '{path}' の読み込みに失敗しました。指定されたカラム {self.columns} が存在しない可能性があります。: {e}")

        return df_list

if __name__ == "__main__":
    # ワイルドカード指定でCSVファイル一覧取得
    import glob
    file_paths = glob.glob("test/concat*.csv")
    print(file_paths)
    concat = CSVConcatExecutor(ConcatByIndexStrategy(), 
                               output_path="test/result.csv", 
                            #    columns=["Group.1"],
                               index_name="No."
                               )
    concat.run(file_paths)