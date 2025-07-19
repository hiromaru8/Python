from binary_file_tool.file_operation.strategy_base import FileOperationStrategy


# 実行クラス（Strategyを委譲して保持）
class FileOperation:
    """
    ファイル操作の実行クラス。
    特定の戦略（Strategy）を保持し、指定されたファイルに対して処理を実行する。
    """
    def __init__(self, strategy: FileOperationStrategy):
        """
        :param strategy: ファイル操作戦略（Split, Extract, HexDumpなど）
        """
        self.strategy = strategy

    def execute(self, filepath):
        """
        戦略に基づいてファイル操作を実行する。

        :param filepath: 対象ファイルパス
        """
        try:
            self.strategy.execute(filepath)
        except IOError as e:
            print(f"ファイル操作中にエラーが発生しました: {filepath} - {e}")
        except Exception as e:
            print(f"予期しないエラーが発生しました: {filepath} - {e}")
