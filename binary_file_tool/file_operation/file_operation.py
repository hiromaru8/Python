"""
file_operation.py

このモジュールは、ファイル操作の実行を担当する FileOperation クラスを提供します。

FileOperation クラスは、Strategy パターンに基づき、特定のファイル操作戦略
（例：分割、抽出、ダンプなど）を委譲し、与えられたファイルに対して処理を実行します。
実際の処理内容は、strategy に指定されたオブジェクト（FileOperationStrategy のサブクラス）に依存します。

主な特徴:
- 処理の実装と実行を分離し、柔軟かつ再利用可能な設計
- 実行時の例外処理を統一して管理
- 抽出など、出力ファイルを生成する strategy の戻り値を取得可能
使用例:
    strategy = ExtractStrategy(offset=128, size=256)
    operator = FileOperation(strategy)
    output_path = operator.execute("input.bin")
    print(f"出力先: {output_path}")
""" 
from typing import Optional

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

    def execute(self, filepath: str) -> list[str]:
        """
        戦略に基づいてファイル操作を実行する。

        :param filepath: 対象ファイルパス
        """
        try:
            output = []
            output.append(self.strategy.execute(filepath))
            
            return output
        except IOError as e:
            raise  IOError(f"ファイル操作中にエラーが発生しました: {filepath} - {e}")
        except Exception as e:
            raise Exception(f"{e}")
        return None
