"""
split_strategy.py

このモジュールは、SplitStrategy クラスを提供します。
SplitStrategy は、指定されたバイナリファイルを固定サイズで分割し、
個別のファイルとして保存するファイル操作戦略です。

Features:
- 任意のチャンクサイズでファイルを分割
- 分割後の出力ファイルを自動生成（_part0, _part1,... 形式）
- 出力ディレクトリの指定が可能（省略時は入力ファイルと同じ場所に保存）
- 端数チャンクの無視オプション（ignore_tail）

使用例:
    strategy = SplitStrategy(chunk_size=1024, ignore_tail=False)
    output_files = strategy.execute("sample.bin")
"""

from pathlib import Path
from typing import Optional

from binary_file_tool.file_operation.strategy_base import FileOperationStrategy
from binary_file_tool.file_error.exceptions import check_chunk_size


# バイナリファイルを指定サイズで分割する戦略
class SplitStrategy(FileOperationStrategy):
    """
    SplitStrategy は、バイナリファイルを指定サイズで分割し、
    ファイル単位で保存する戦略クラスです。
    """
    def __init__(self, chunk_size: int, ignore_tail: bool,
                 output_dir: Optional[str] = None) -> None:
        """

        Args:
            chunk_size (int): 分割サイズ（バイト）
            ignore_tail (bool): 最後の端数チャンクを無視するかどうか
        """

        self.chunk_size = chunk_size
        self.ignore_tail = ignore_tail
        self.output_dir = Path(output_dir) if output_dir else None

    def execute(self, filepath: str) -> list[str]:
        """
        ファイルを読み込み、指定サイズで分割して別ファイルに保存する。

        Args:
            filepath (str): 抽出元のファイルパス（絶対または相対パス）

        Returns:
            list[str]: 出力ファイルパスのリスト
        """
        file = Path(filepath)
        
        # チャンクサイズをチェック
        check_chunk_size(file,self.chunk_size)
        
        # 出力ディレクトリ
        out_dir = self.output_dir or file.parent
        # 存在しない場合はディレクトリ作成
        out_dir.mkdir(parents=True, exist_ok=True)
        
        output_paths = []
        with open(filepath, 'rb') as f:
            index = 0
            while True:
                # chunk_size読み込み
                chunk = f.read(self.chunk_size)
                # 空であれば終了
                if not chunk:
                    break
                # 端数がある場合、指定があれば破棄する
                if len(chunk) < self.chunk_size and self.ignore_tail:
                    break
                # 出力ファイル名
                base_name = file.stem
                ext = file.suffix
                out_path = out_dir / f"{base_name}_part{index}{ext}"
                
                # 書き込み
                with open(out_path, 'wb') as out_file:
                    out_file.write(chunk)
                output_paths.append(str(out_path))
                index += 1

        return output_paths
    