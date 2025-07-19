import argparse
from pathlib import Path

from binary_file_tool.file_operation.file_operation import FileOperation
from binary_file_tool.file_operation.split_strategy import SplitStrategy
from binary_file_tool.file_operation.extract_strategy import ExtractStrategy
from binary_file_tool.file_operation.hexdump_strategy import HexDumpStrategy

# ワイルドカードを展開し、対象ファイル一覧を取得
def resolve_files(pattern):
    """
    入力パターン（ワイルドカード含む）にマッチするファイル一覧を取得する。

    :param pattern: 入力ファイルパターン（例: *.bin）
    :return: ファイルパスのリスト
    """
    path = Path(pattern)
    if path.parent != Path('.'):
        base = path.parent
        pattern = path.name
    else:
        base = Path()
        pattern = str(path)

    return list(base.rglob(pattern))

# メイン関数：コマンドライン引数の解析と処理実行
def main():
    """
    コマンドライン引数を解析し、対応するファイル処理を実行する。
    """
    parser = argparse.ArgumentParser(description="Binary file operation tool")
    subparsers = parser.add_subparsers(dest='command')

    # 分割コマンド
    parser_split = subparsers.add_parser('split', help='バイナリファイルを指定サイズで分割する')
    parser_split.add_argument('--input', required=True, help='入力ファイルパス（ワイルドカード可）')
    parser_split.add_argument('--size', type=int, required=True, help='分割サイズ（バイト）')
    parser_split.add_argument('--ignore-tail', action='store_true', help='端数チャンクを無視する')

    # 抽出コマンド
    parser_extract = subparsers.add_parser('extract', help='任意範囲のデータを抽出')
    parser_extract.add_argument('--input', required=True, help='入力ファイルパス（ワイルドカード可）')
    parser_extract.add_argument('--offset', type=int, required=True, help='開始位置（バイト）')
    parser_extract.add_argument('--size', type=int, required=True, help='抽出サイズ（バイト）')

    # hexdumpコマンド
    parser_hexdump = subparsers.add_parser('hexdump', help='ファイル内容をhexdump表示')
    parser_hexdump.add_argument('--input', required=True, help='入力ファイルパス（ワイルドカード可）')
    parser_hexdump.add_argument('--offset', type=int, default=0, help='開始位置（バイト）')
    parser_hexdump.add_argument('--size', type=int, default=None, help='表示サイズ（バイト）')

    args = parser.parse_args()
    # 各サブコマンドごとの戦略生成
    if args.command == 'split':
        strategy = SplitStrategy(args.size, args.ignore_tail)
    elif args.command == 'extract':
        strategy = ExtractStrategy(args.offset, args.size)
    elif args.command == 'hexdump':
        strategy = HexDumpStrategy(args.offset, args.size)
    else:
        parser.print_help()
        return
    
    operation = FileOperation(strategy)
    paths = resolve_files(args.input)
    if not paths:
        print(f"[警告] ファイルが見つかりません: {args.input}")
        return

    for path in paths:
        operation.execute(path)

# エントリーポイント
if __name__ == '__main__':
    main()
