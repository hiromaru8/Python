from binary_file_tool.file_operation.strategy_base import FileOperationStrategy


# バイナリファイルを指定サイズで分割する戦略
class SplitStrategy(FileOperationStrategy):
    """
    バイナリファイルを指定サイズのチャンクに分割する戦略。
    """
    def __init__(self, chunk_size, ignore_tail):
        """
        :param chunk_size: 分割サイズ（バイト）
        :param ignore_tail: 最後の端数チャンクを無視するかどうか
        """
        self.chunk_size = chunk_size
        self.ignore_tail = ignore_tail

    def execute(self, filepath):
        """
        ファイルを読み込み、指定サイズで分割して別ファイルに保存する。
        """
        with open(filepath, 'rb') as f:
            index = 0
            while True:
                chunk = f.read(self.chunk_size)
                if not chunk:
                    break
                # 端数がある場合、指定があれば破棄する
                if self.ignore_tail and len(chunk) < self.chunk_size:
                    break
                out_path = f"{filepath}_part{index}"
                with open(out_path, 'wb') as out_file:
                    out_file.write(chunk)
                index += 1

