"""
strategy_base.py

このモジュールは、ファイル生成のためのStrategyパターンのインタフェースを定義します。

クラス:
    GenerateFileStrategy (ABC): すべてのファイル生成戦略クラスが継承すべき抽象基底クラス。

使い方例:
    class SplitStrategy(GenerateFileStrategy):
        def execute(self, filepath):
            # バイナリファイル生成
            pass

備考:
    このクラスは拡張性を持たせるためにStrategyパターンを利用しています。
    さまざまなファイル生成をこのインタフェースを通じて統一的に実装できます。
""" 
from abc import ABC, abstractmethod

# Strategyインタフェース：ファイル生成の共通処理
class GenerateFileStrategy(ABC):
    """
    ファイル生成の戦略インタフェース。
    execute(filepath) メソッドを実装して、特定のファイル生成を実行する。
    """
    @abstractmethod
    def execute(self, filepath: str) -> list[str]:
        """
        ファイル生成を実装する。

        :param filepath: 出力ファイル名のリスト
        """
        pass