"""
hextobinary_chunked_strategy.py

大容量の16進数テキストファイルを効率的にバイナリファイルへ変換する戦略クラス。
チャンク単位で読み込み・変換を行うことで、メモリ使用量を抑えつつ高速処理を実現する。

使用例:
    strategy = HexToBinaryChunkedStrategy()
    strategy.execute("hexdata.txt")  # → ["hexdata.bin"]

このクラスは ConvertFileStrategy を継承しており、convert_file モジュール内で使用される。
"""
import os
import re
from pathlib import Path
from typing import Optional

from binary_file_tool.convert_file.strategy_base import ConvertFileStrategy
from binary_file_tool.file_error.exceptions import check_file_not_empty

# 任意範囲のデータ抽出戦略
class HexToBinaryChunkedStrategy(ConvertFileStrategy):
    """
    16進数テキストファイルからバイナリファイルに変換する戦略(超大容量向け)。
    chunk_sizeで指定したサイズごとに読み込み、変換を行います。
    
    """
    def __init__(self, 
                 encoding: str = 'utf-8-sig', chunk_size: int = 8192,
                 output_dir: Optional[str] = None) -> None:
        """
        Args:
            encoding (str) : ファイルのエンコーディング. Defaults to 'utf-8-sig'（BOM付きも対応）.
            chunk_size (int): 読み込みチャンクサイズ. Defaults to 8192.
            output_dir (Optional[str]): 出力ディレクトリ. Defaults to None.
        """
        self.encoding   = encoding
        self.chunk_size = chunk_size
        self.output_dir = Path(output_dir) if output_dir else None

        
    def execute(self, filepath:str) -> list[str]:
        """
        16進数テキストファイルからバイナリファイルに変換する

        Args:
            filepath (str): 抽出元のファイルパス（絶対または相対パス）

        Raises:
            EmptyFileError: ファイルが空の場合

        Returns:
            list[str]: 出力されたバイナリファイルのパス（1要素）
        """

        file = Path(filepath)
        
        # 空ファイルの検出と例外処理
        check_file_not_empty(file)
        
        # 出力ファイル名
        out_path = file.with_suffix('.bin')
           
        # 出力ディレクトリ
        out_dir = self.output_dir or file.parent
        # 出力ディレクトリが存在しない場合は作成
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / out_path.name

        buffer = ""
        with open(filepath, 'r', encoding=self.encoding) as fin, \
            open(out_path, 'wb') as fout:

            while True:
                chunk = fin.read(self.chunk_size)
                if not chunk:
                    break

                # 空白・改行などを取り除きバッファに追加
                cleaned = re.sub(r'[^0-9a-fA-F]', '', chunk)  # 16進数文字（0-9, a-f, A-F）のみ抽出
                buffer += cleaned

                # 偶数文字数まで処理、残りは次回に持ち越し
                process_len = len(buffer) - (len(buffer) % 2)
                process_part = buffer[:process_len]
                buffer = buffer[process_len:]

                try:
                    binary_data = bytes.fromhex(process_part)
                except ValueError as e:
                    if out_path.exists():
                        os.remove(out_path)
                    raise ValueError(f"16進数変換エラー: {e}（データ抜粋: {process_part[:32]}...）")

                fout.write(binary_data)
        
            if buffer:
                raise ValueError(f"変換できない1文字が残りました（不正な16進数？）: '{buffer}'")
            
        return [str(out_path)]
