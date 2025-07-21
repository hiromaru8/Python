"""
generate_file.py


""" 

from binary_file_tool.generate_file.strategy_base import GenerateFileStrategy


# 実行クラス（Strategyを委譲して保持）
class GenerateFile:
    """
    ファイル生成の実行クラス。
    特定の戦略（Strategy）を保持し、指定された方法でファイルを生成する
    """
    def __init__(self, strategy: GenerateFileStrategy):
        """
        :param strategy: ファイル生成戦略（Split, Extract, HexDumpなど）
        """
        self.strategy = strategy

    def execute(self, filepath: str) -> list[str]:
        """
        戦略に基づいてファイル生成を実行する。
        
        Args:
            filepath (str): 出力ファイル

        Returns:
            list[str]: 出力ファイル名のリスト
        """

        try:
            result = self.strategy.execute(filepath)
            
            if isinstance(result, list):
                return result
            else:
                return [result]
        except IOError as e:
            raise  IOError(f"ファイル操作中にエラーが発生しました: {filepath} - {e}")
        except Exception as e:
            raise Exception(f"{e}") from e
