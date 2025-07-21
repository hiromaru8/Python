"""
extract_strategy.py

このモジュールは、ExtractStrategy クラスを定義します。
ExtractStrategy は、指定されたバイナリファイルから任意の範囲（オフセットとサイズ）を抽出し、
別のファイルとして保存するための戦略クラスです。

Features:
- 指定バイト範囲（オフセット＋サイズ）の抽出
- 抽出後のファイル名に任意の接尾辞（suffix）や拡張子（file_ext）を付与可能
- 出力先ディレクトリの指定が可能。存在しない場合は自動作成
- 抽出結果のファイルパス（文字列）を返すことで、後続処理に活用しやすい

Typical usage:
    strategy = ExtractStrategy(offset=128, size=256, suffix="_header", file_ext=".dat", output_dir="output")
    output_path = strategy.execute("input.bin")
    print(f"抽出ファイル: {output_path}")
    
"""
from pathlib import Path
from typing import Optional

from binary_file_tool.file_operation.strategy_base import FileOperationStrategy
from binary_file_tool.file_error.exceptions import check_file_not_empty,check_offset_in_range,check_size_available

# 任意範囲のデータ抽出戦略
class ExtractStrategy(FileOperationStrategy):
    """
    指定した範囲のバイナリデータを抽出する戦略。
    """
    def __init__(self, offset:int, size:int,
                 suffix :Optional[str] = None, file_ext:Optional[str] = None,
                 output_dir: Optional[str] = None) -> None:
        """
        Args:
            offset (int)    : 抽出開始位置（バイト）
            size (int)      : 抽出サイズ（バイト）
            suffix (Optional[str], optional)    : 出力ファイルの末尾に追加する名称. Defaults to None.
                                                  未指定の場合は、「_extract」を付与。
            file_ext (Optional[str], optional)  : 出力ファイルの拡張子. Defaults to None.
        """

        self.offset     = offset
        self.size       = size
        self.suffix     = f"_{suffix}" if suffix else "_extract"
        self.file_ext   = f".{file_ext.lstrip('.')}" if file_ext else None
        self.output_dir = Path(output_dir) if output_dir else None
        
    def execute(self, filepath:str) -> list[str]:
        """
        ファイルから指定範囲を読み取り、別ファイルに保存する。

        Args:
            filepath (str): 抽出元のファイルパス（絶対または相対パス）

        Raises:
            EmptyFileError: ファイルが空の場合
            OffsetOutOfRangeError: オフセットがファイルサイズの範囲外の場合
            SizeExceedsError: 指定サイズが利用可能なサイズを超えた場合

        Returns:
            list[str]: 出力されたバイナリファイルのパス（1要素）
        """

        file = Path(filepath)
        
        # 範囲外アクセスの対処
        # 空ファイル
        check_file_not_empty(file)
        
        # オフセットが範囲外
        check_offset_in_range(file, self.offset)
        
        read_size = self.size
        # 指定サイズを得られない
        check_size_available(file, self.offset, self.size)
    
    
        # 読み込み
        with open(filepath, 'rb') as f:
            f.seek(self.offset)
            data = f.read(read_size)
        
        # 出力ファイル名
        suffix  = self.suffix 
        new_name = file.with_name(f"{file.stem}{suffix}")
        
        # 出力ファイル拡張子
        if self.file_ext:
            out_path = new_name.with_suffix(self.file_ext)  # 指定した拡張子
        else:
            out_path = new_name.with_suffix(file.suffix)    # 入力ファイルと同じ拡張子
        
        # 出力ディレクトリ
        out_dir = self.output_dir or file.parent
        # 存在しない場合はディレクトリ作成
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / out_path.name
        
        # 書き込み
        with open(out_path, 'wb') as out_file:
            out_file.write(data)
        
        return [str(out_path)]
