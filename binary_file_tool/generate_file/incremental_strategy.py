from typing import Literal
from pathlib import Path

from binary_file_tool.generate_file.strategy_base import GenerateFileStrategy

class IncrementalDataStrategy(GenerateFileStrategy):
    """
    インクリメント値で構成されたバイナリファイルを生成する戦略。
    例: 00 01 02 03 ... FF 00 01 ...
    """

    def __init__(self, size: int, unit_size: int = 4,
                 start_value: int = 0, endian: Literal['little', 'big'] = 'little'):
        """

        Args:
            size (int)                  : 出力する総バイト数。unit_size の倍数である必要があります。
            unit_size (int, optional)   : 1整数あたりのバイト数。Defaults to 4.
            start_value (int, optional) : 出力データの開始値（初期値）。Defaults to 0.
            endian (Literal['little', 'big'], optional): エンディアン指定。Defaults to 'little'.

        Raises:
            ValueError: sizeがunit_sizeの倍数でない場合
            ValueError: unit_sizeがサポート外の値の場合
        """

        if endian not in ('little', 'big'):
            raise ValueError("endian は 'little' または 'big' のいずれかである必要があります")
        if size % unit_size != 0:
            raise ValueError(f"size({size}) は unit_size({unit_size}) の倍数である必要があります")
        if start_value < 0:
            raise ValueError(f"start_value({start_value}) は 0 以上である必要があります")

        self.size       = size
        self.unit_size  = unit_size
        self.start_value = start_value
        self.endian  = endian

    def execute(self, filepath: str) -> list[str]:
        
        file = Path(filepath)
        # 出力ディレクトリ
        out_dir = file.parent
        # 存在しない場合はディレクトリ作成
        out_dir.mkdir(parents=True, exist_ok=True)
        
        
        with open(filepath, "wb") as f:
            # 書き込むデータ数（unit単位）と最大値（ラップアラウンド用）
            count = self.size // self.unit_size
            current = self.start_value
            max_value = 2 ** (self.unit_size * 8)
            # 指定サイズ分のインクリメントデータを順次書き込み
            for _ in range(count):
                value = current % max_value  # 指定bit幅を超えたら0に戻る
                f.write(value.to_bytes(self.unit_size, byteorder=self.endian, signed=False))
                current += 1
        return [filepath]


