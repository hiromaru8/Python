from binary_file_tool.file_operation.strategy_base import FileOperationStrategy


# バイナリファイルをhexdump出力する戦略
class HexDumpStrategy(FileOperationStrategy):
    """
    バイナリファイルをhexdump形式で標準出力に表示する戦略。
    """
    def __init__(self, offset=0, size=None):
        """
        :param offset: 表示開始位置（バイト）
        :param size: 表示サイズ（バイト）。Noneの場合は末尾まで。
        """
        self.offset = offset
        self.size = size

    def execute(self, filepath):
        """
        指定範囲のバイナリを16バイトごとに整形し表示する。
        """
        print(f"Path : {filepath}")
        with open(filepath, 'rb') as f:
            f.seek(self.offset)
            data = f.read() if self.size is None else f.read(self.size)
            for i in range(0, len(data), 16):
                chunk = data[i:i+16]
                hex_chunk = ' '.join(f"{b:02x}" for b in chunk)
                ascii_chunk = ''.join((chr(b) if 32 <= b < 127 else '.') for b in chunk)
                print(f"{self.offset + i:08x}  {hex_chunk:<48}  |{ascii_chunk}|")
