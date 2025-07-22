import argparse
import glob
from pathlib import Path
from typing import List

from binary_file_tool.file_operation.file_operation import FileOperation
from binary_file_tool.file_operation.split_strategy import SplitStrategy
from binary_file_tool.file_operation.extract_strategy import ExtractStrategy
from binary_file_tool.file_operation.hexdump_strategy import HexDumpStrategy

from binary_file_tool.generate_file.generate_file import GenerateFile
from binary_file_tool.generate_file.incremental_strategy import IncrementalDataStrategy
from binary_file_tool.generate_file.random_strategy import SecureRandomStrategy
from binary_file_tool.convert_file.convert_file import ConvertFile
from binary_file_tool.convert_file.hextobinary_chunked_strategy import HexToBinaryChunkedStrategy

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
    print(__file__)
    print("hello world")
    print(__file__)
    # メインパーサー
    parser = argparse.ArgumentParser(description="Binary file operation tool")
    subparsers = parser.add_subparsers(dest='command')

    # ==================================================================
    #  ファイル操作コマンド群 
    # ==================================================================
    # file_operation共通オプション用の親パーサー（help を False にして二重表示を防ぐ）
    file_operation_parser = argparse.ArgumentParser(add_help=False)
    file_operation_parser.add_argument('--force', action='store_true',  help='大量ファイル処理の確認をスキップする')
    file_operation_parser.add_argument('--input', required=True,        help='入力ファイルパス（ワイルドカード可）')
    
    # 分割コマンド
    parser_split = subparsers.add_parser('split', parents=[file_operation_parser],      help='バイナリファイルを指定サイズで分割する')
    parser_split.add_argument('--size',         type=non_negative_int,  required=True,  help='分割サイズ（バイト）')
    parser_split.add_argument('--ignore-tail',  action='store_true',                    help='端数チャンクを無視する')
    parser_split.add_argument('--output_dir',   type=str,                               help='出力ディレクトリ。未指定の場合は、入力ファイルと同じ')

    # 抽出コマンド
    parser_extract = subparsers.add_parser('extract', parents=[file_operation_parser],  help='任意範囲のデータを抽出')
    parser_extract.add_argument('--offset',     type=non_negative_int,  default=0,      help='開始位置（バイト）。初期値は０')
    parser_extract.add_argument('--size',       type=non_negative_int,  required=True,  help='抽出サイズ（バイト）')
    parser_extract.add_argument('--suffix',     type=str,                               help='出力ファイル名の末尾。未指定の場合"_extrace"')
    parser_extract.add_argument('--file_ext',   type=str,                               help='出力ファイル拡張子。未指定の場合は入力ファイルと同じ')
    parser_extract.add_argument('--output_dir', type=str,                               help='出力ディレクトリ。未指定の場合は、入力ファイルと同じ')
    
    # hexdumpコマンド
    parser_hexdump = subparsers.add_parser('hexdump', parents=[file_operation_parser],  help='ファイル内容をhexdump表示')
    parser_hexdump.add_argument('--offset', type=non_negative_int, default=0,           help='開始位置（バイト）')
    parser_hexdump.add_argument('--size',   type=non_negative_int, default=None,        help='表示サイズ（バイト）')

    # ==================================================================
    #  ファイル生成コマンド群
    # ==================================================================
    parser_generate = subparsers.add_parser('generate', help='バイナリファイルを生成する')
    generate_subparsers = parser_generate.add_subparsers(dest='generate_type')

    # file_operation共通オプション用の親パーサー（help を False にして二重表示を防ぐ）
    generate_file_parser = argparse.ArgumentParser(add_help=False)
    generate_file_parser.add_argument('--output', required=True, help='出力ファイルパス')
    
    # incremental サブコマンド
    parser_increment = generate_subparsers.add_parser('incremental', parents=[generate_file_parser], help='インクリメントデータで構成されたバイナリファイルを生成')
    parser_increment.add_argument('--size',        type=non_negative_int,       required=True,  help='生成サイズ（バイト）')
    parser_increment.add_argument('--unit_size',   type=non_negative_int,       default=4,      help='単位サイズ（バイト）')
    parser_increment.add_argument('--start_value', type=non_negative_int,       default=0,      help='開始値')
    parser_increment.add_argument('--endian',      choices=['little', 'big'],   default='big',  help='バイトオーダー')
    
    # random サブコマンド
    parser_random = generate_subparsers.add_parser('random', parents=[generate_file_parser], help='暗号論的に安全な乱数で構成されたバイナリファイルを生成')
    parser_random.add_argument('--size', type=non_negative_int, required=True, help='生成サイズ（バイト）')

    # ==================================================================
    #  ファイル変換コマンド群
    # ==================================================================
    parser_convert = subparsers.add_parser('convert', help='ファイル変換を実行する')
    convert_subparsers = parser_convert.add_subparsers(dest='convert_type')
    
    # convert_file共通オプション用の親パーサー（help を False にして二重表示を防ぐ）
    convert_file_parser = argparse.ArgumentParser(add_help=False)
    convert_file_parser.add_argument('--output_dir', type=str, help='出力ディレクトリ。未指定の場合は、入力ファイルと同じ')
    convert_file_parser.add_argument('--input', required=True,        help='入力ファイルパス（ワイルドカード可）')
    convert_file_parser.add_argument('--force', action='store_true',  help='大量ファイル処理の確認をスキップする')
    
    # hextobinary サブコマンド
    parser_hextobinary = convert_subparsers.add_parser('hextobinary', parents=[convert_file_parser], help='16進数テキストファイルをバイナリファイルに変換する')
    parser_hextobinary.add_argument('--chunk_size', type=non_negative_int, default=8192,    help='チャンクサイズ（バイト）処理単位で、メモリ使用量を抑える')



    # ==================================================================
    # コマンドライン引数に基づき、該当する戦略インスタンスを生成する
    # ==================================================================
    args = parser.parse_args()
    # 各サブコマンドごとの戦略生成
    # ファイル操作群
    if args.command == 'split':
        strategy = SplitStrategy(args.size, args.ignore_tail,output_dir=args.output_dir)
        operation = FileOperation(strategy)
    elif args.command == 'extract':
        strategy = ExtractStrategy(args.offset, args.size,suffix=args.suffix,file_ext=args.file_ext,output_dir=args.output_dir)
        operation = FileOperation(strategy)
    elif args.command == 'hexdump':
        strategy = HexDumpStrategy(args.offset, args.size)
        operation = FileOperation(strategy)
    # ファイル生成群
    elif args.command == 'generate':
        if args.generate_type == 'incremental':
            strategy = IncrementalDataStrategy(args.size, args.unit_size, args.start_value, args.endian)
            operation = GenerateFile(strategy)
        elif args.generate_type == 'random':
            strategy = SecureRandomStrategy(args.size)
            operation = GenerateFile(strategy)
        else:
            parser_generate.print_help()
            return
    # ファイル変換群
    elif args.command == 'convert':
        if args.convert_type == 'hextobinary':
            strategy = HexToBinaryChunkedStrategy(encoding='utf-8-sig', chunk_size=args.chunk_size, output_dir=args.output_dir)
            operation = ConvertFile(strategy)
        else:
            parser_convert.print_help()
            return
    else:
        parser.print_help()
        return
    
    # ==================================================================
    # 入出力ファイルの解決と処理実行
    # ==================================================================
    if args.command in ('split', 'extract', 'hexdump', 'convert'):
        paths = resolve_files(args.input)
        if not paths:
            print(f"[警告] 入力パターンにマッチするファイルが見つかりません: {args.input}")
            return
    elif args.command in ('generate'):
        paths = [args.output]
    else:
        parser.print_help()
        return
    
    #==================================================================
    # 対象ファイルの解決
    # ==================================================================
    # 対象ファイルが多い場合の確認
    # 30件以上のファイルが対象の場合、確認を行う
    MAX_FILES_BEFORE_WARNING = 30
    if len(paths) >= MAX_FILES_BEFORE_WARNING and not args.force:
        print(f"[警告] 対象ファイルが {len(paths)} 件あります。処理を続行しますか？ (y/N): ", end="")
        confirm = input().strip().lower()
        if confirm != 'y':
            print("処理を中止しました。")
            return
    
    # 各ファイルに対して処理を実行
    for path in paths:
        try:
            outpath = operation.execute(path)
            
            for path in outpath:
                print(f"出力ファイル：{path}")
        except Exception as e:
            print(f"予期しないエラーが発生しました: {path} - {e}")

# エントリーポイント
if __name__ == '__main__':
    print(__file__)
    main()
