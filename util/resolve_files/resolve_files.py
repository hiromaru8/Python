import glob 
from pathlib import Path
from typing import List

def resolve_files(pattern: str) -> List[str]:
    """
    入力パターン（ワイルドカード含む）にマッチするファイル一覧を取得する。

    :param pattern: 入力ファイルパターン（例: *.bin, data/**/*.bin など）
    :return: Path オブジェクトのリスト（ファイルパス）
    """
    return [str(p) for p in glob.glob(pattern, recursive=True) if Path(p).is_file()]
