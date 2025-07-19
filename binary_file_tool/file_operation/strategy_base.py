
from abc import ABC, abstractmethod

# Strategyインタフェース：ファイル操作の共通処理
class FileOperationStrategy(ABC):
    """
    ファイル操作の戦略インタフェース。
    execute(filepath) メソッドを実装して、特定のファイル操作を実行する。
    """
    @abstractmethod
    def execute(self, filepath):
        """
        ファイル操作を実行する。

        :param filepath: 操作対象のファイルパス
        """
        pass