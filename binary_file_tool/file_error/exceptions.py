"""
exceptions.py

ファイル操作に関連する共通例外クラスと、
ファイルの状態チェック用ユーティリティ関数を提供するモジュール。

- FileError: ファイル操作全般の共通例外基底クラス
- EmptyFileError: ファイルが空の場合に発生する例外
- OffsetOutOfRangeError: 指定オフセットがファイルサイズ範囲外の場合に発生する例外
- SizeExceedsError: 指定サイズが利用可能サイズを超えた場合に発生する例外

- check_file_not_empty: ファイルが空でないことを検証する関数
- check_offset_in_range: オフセットがファイルサイズ内か検証する関数
- check_size_available: 指定範囲の読み込みが可能か検証する関数

このモジュールを用いることで、複数のストラテジークラス間で例外処理や
ファイル状態チェックの一貫性を保つことができる。
"""

from pathlib import Path

class FileError(Exception):
    """ファイル操作全般の共通例外基底クラス"""
    pass

class EmptyFileError(FileError):
    """ファイルが空の場合の例外"""
    pass

class OffsetOutOfRangeError(FileError):
    """オフセットがファイルサイズの範囲外の場合の例外"""
    pass

class SizeExceedsError(FileError):
    """指定されたサイズが利用可能なサイズを超えた場合の例外"""
    pass

def check_file_not_empty(filepath: Path) -> None:
    """
    ファイルが空でないかをチェックする。
    
    Args:
        filepath (Path): チェック対象のファイルパス
    
    Raises:
        EmptyFileError: ファイルサイズが0の場合に発生
    """
    size = filepath.stat().st_size
    if size == 0:
        raise EmptyFileError(f"ファイル'{filepath}'は空です。")
    
def check_offset_in_range(filepath: Path, offset: int) -> None:
    """
    指定したオフセットがファイルサイズの範囲内かチェックする。
    
    Args:
        filepath (Path): 対象ファイルのパス
        offset (int): チェックするオフセット値（バイト単位）
    
    Raises:
        OffsetOutOfRangeError: オフセットがファイルサイズを超える場合に発生
    """
    size = filepath.stat().st_size
    if offset > size:
        raise OffsetOutOfRangeError(f"オフセット({offset})がファイルサイズ({size})を超えています。ファイル: '{filepath}'")

def check_size_available(filepath: Path, offset: int, requested_size: int) -> int:
    """
    指定したオフセットから要求されたサイズが読み込み可能かをチェックする。
    
    Args:
        filepath (Path): 対象ファイルのパス
        offset (int): 読み込み開始オフセット
        requested_size (int): 読み込みを要求するサイズ（バイト）
    
    Raises:
        SizeExceedsError: 要求サイズが利用可能サイズを超える場合に発生
    
    """
    size = filepath.stat().st_size
    available = size - offset
    if requested_size > available:
        raise SizeExceedsError(
            f"要求サイズ({requested_size}バイト)は利用可能サイズ({available}バイト)を超えています。"
            f"ファイル: '{filepath}', オフセット: {offset}"
        )

