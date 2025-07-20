import argparse
import glob
from pathlib import Path
from typing import List

from binary_file_tool.file_operation.file_operation import FileOperation
from binary_file_tool.file_operation.split_strategy import SplitStrategy
from binary_file_tool.file_operation.extract_strategy import ExtractStrategy
from binary_file_tool.file_operation.hexdump_strategy import HexDumpStrategy

# ワイルドカードを展開し、対象ファイル一覧を取得
def resolve_files(pattern: str) -> List[Path]:
    """
    入力パターン（ワイルドカード含む）にマッチするファイル一覧を取得する。

    :param pattern: 入力ファイルパターン（例: *.bin, data/**/*.bin など）
    :return: Path オブジェクトのリスト（ファイルパス）
    """
    return [Path(p) for p in glob.glob(pattern, recursive=True) if Path(p).is_file()]

def non_negative_int(value):
    """
    文字列を0以上の整数に変換し、妥当性を検証する。

    argparse の type 引数として使用することを想定。

    :param value: コマンドライン引数として渡される文字列
    :return: 変換後の整数値（0以上）
    :raises argparse.ArgumentTypeError: 0未満の値が指定された場合
    """
    ivalue = int(value)
    if ivalue < 0:
        raise argparse.ArgumentTypeError(f"{value} は0以上の整数ではありません")
    return ivalue

# メイン関数：コマンドライン引数の解析と処理実行
def main():
    """
    コマンドライン引数を解析し、対応するファイル処理を実行する。
    """
    parser = argparse.ArgumentParser(description="Binary file operation tool")
    subparsers = parser.add_subparsers(dest='command')

    # 分割コマンド
    parser_split = subparsers.add_parser('split',                                       help='バイナリファイルを指定サイズで分割する')
    parser_split.add_argument('--input',                                required=True,  help='入力ファイルパス（ワイルドカード可）')
    parser_split.add_argument('--size',         type=non_negative_int,  required=True,  help='分割サイズ（バイト）')
    parser_split.add_argument('--ignore-tail',  action='store_true',                    help='端数チャンクを無視する')
    parser_split.add_argument('--output_dir',   type=str,                               help='出力ディレクトリ。未指定の場合は、入力ファイルと同じ')

    # 抽出コマンド
    parser_extract = subparsers.add_parser('extract', help='任意範囲のデータを抽出')
    parser_extract.add_argument('--input',                              required=True,  help='入力ファイルパス（ワイルドカード可）')
    parser_extract.add_argument('--offset',     type=non_negative_int,  default=0,      help='開始位置（バイト）。初期値は０')
    parser_extract.add_argument('--size',       type=non_negative_int,  required=True,  help='抽出サイズ（バイト）')
    parser_extract.add_argument('--suffix',     type=str,                               help='出力ファイル名の末尾。未指定の場合"_extrace"')
    parser_extract.add_argument('--file_ext',   type=str,                               help='出力ファイル拡張子。未指定の場合は入力ファイルと同じ')
    parser_extract.add_argument('--output_dir', type=str,                               help='出力ディレクトリ。未指定の場合は、入力ファイルと同じ')
    
    # hexdumpコマンド
    parser_hexdump = subparsers.add_parser('hexdump', help='ファイル内容をhexdump表示')
    parser_hexdump.add_argument('--input',  required=True,                          help='入力ファイルパス（ワイルドカード可）')
    parser_hexdump.add_argument('--offset', type=non_negative_int, default=0,       help='開始位置（バイト）')
    parser_hexdump.add_argument('--size',   type=non_negative_int, default=None,    help='表示サイズ（バイト）')

    args = parser.parse_args()
    # 各サブコマンドごとの戦略生成
    if args.command == 'split':
        strategy = SplitStrategy(args.size, args.ignore_tail,output_dir=args.output_dir)
    elif args.command == 'extract':
        strategy = ExtractStrategy(args.offset, args.size,suffix=args.suffix,file_ext=args.file_ext,output_dir=args.output_dir)
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
