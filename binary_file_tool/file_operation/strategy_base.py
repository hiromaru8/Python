"""
strategy_base.py

このモジュールは、ファイル操作のためのStrategyパターンのインタフェースを定義します。

クラス:
    FileOperationStrategy (ABC): すべてのファイル操作戦略クラスが継承すべき抽象基底クラス。

使い方例:
    class SplitStrategy(FileOperationStrategy):
        def execute(self, filepath):
            # 分割処理を実装
            pass

備考:
    このクラスは拡張性を持たせるためにStrategyパターンを利用しています。
    さまざまなファイル操作（分割、抽出、ダンプなど）をこのインタフェースを通じて統一的に実装できます。
""" 
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