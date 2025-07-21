import secrets
from pathlib import Path
from binary_file_tool.generate_file.strategy_base import GenerateFileStrategy
class SecureRandomStrategy(GenerateFileStrategy):
    """
    暗号論的に安全な乱数で構成されたバイナリファイルを生成する戦略。
    例: secrets.token_bytes() を用いて、指定サイズのランダムデータを出力する。
    """

    def __init__(self, size: int):
        """        

        Args:
            size (int): 出力するファイルサイズ（バイト数）。セキュアなランダムバイト列を生成します。
        
        Raises:
            ValueError: size が正の整数でない場合
        """
        if size <= 0:
            raise ValueError(f"size({size}) は正の整数である必要があります")

        self.size = size

    def execute(self, filepath: str) -> list[str]:
        
        file = Path(filepath)
        
        # 出力ディレクトリ
        out_dir = file.parent
        # 存在しない場合はディレクトリ作成
        out_dir.mkdir(parents=True, exist_ok=True)
        
        # ファイルにセキュアなランダムバイトを書き込む        
        with open(filepath, "wb") as f:
            f.write(secrets.token_bytes(self.size))
        return [str(file)]
