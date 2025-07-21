"""
strategy_base.py

このモジュールは、ファイル変換のStrategyパターンのインタフェースを定義します。

クラス:
    GenerateFileStrategy (ABC): すべてのファイル変換戦略クラスが継承すべき抽象基底クラス。

使い方例:
    class SplitStrategy(ConvertFileStrategy):
        def execute(self, filepath):
            # バイナリファイル変換
            pass

備考:
    このクラスは拡張性を持たせるためにStrategyパターンを利用しています。
    さまざまなファイル変換をこのインタフェースを通じて統一的に実装できます。
""" 
from abc import ABC, abstractmethod

# Strategyインタフェース：ファイル変換の共通処理
class ConvertFileStrategy(ABC):
    """
    ファイル変換の戦略インタフェース。
    execute(filepath) メソッドを実装して、特定のファイル変換を実行する。
    """
    @abstractmethod
    def execute(self, filepath: str) -> list[str]:
        """
        ファイル変換を実装する。

        :param filepath: 出力ファイル名のリスト
        """
        pass