"""
convert_file.py

このモジュールは、ファイル変換のStrategyパターンのインタフェースを定義します。

クラス:
    ConvertFileStrategy (ABC): すべてのファイル変換戦略クラスが継承すべき抽象基底クラス。

備考:
    このクラスは拡張性を持たせるためにStrategyパターンを利用しています。
    さまざまなファイル変換をこのインタフェースを通じて統一的に実装できます。
"""

from binary_file_tool.convert_file.strategy_base import ConvertFileStrategy


# 実行クラス（Strategyを委譲して保持）
class ConvertFile:
    """
    ファイル変換の実行クラス。
    特定の戦略（Strategy）を保持し、指定された方法でファイルを変換する
    """
    def __init__(self, strategy: ConvertFileStrategy):
        """
        :param strategy: ファイル変換戦略
        """
        self.strategy = strategy

    def execute(self, filepath: str) -> list[str]:
        """
        戦略に基づいてファイル変換を実行する。

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
