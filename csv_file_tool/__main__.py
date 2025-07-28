
import argparse

from csv_file_tool.concat.csv_concat_executor import CSVConcatExecutor
from csv_file_tool.concat.by_index import ConcatByIndexStrategy

from util.resolve_files.resolve_files import resolve_files

def main():

    # メインパーサー
    parser = argparse.ArgumentParser(description="Binary file operation tool")
    subparsers = parser.add_subparsers(dest='command')

    # ==================================================================
    #  ファイル操作コマンド群 
    # ==================================================================
    concat_operation_generate = subparsers.add_parser('concat', help='バイナリファイルを生成する')
    concat_operation_subparsers = concat_operation_generate.add_subparsers(dest='generate_type')

    
    # concat_operation共通オプション用の親パーサー（help を False にして二重表示を防ぐ）
    concat_common_parser = argparse.ArgumentParser(add_help=False)
    concat_common_parser.add_argument('--force', action='store_true',   help='大量ファイル処理の確認をスキップする')
    concat_common_parser.add_argument('--input', required=True,         help='入力ファイルパス（ワイルドカード可）')
    concat_common_parser.add_argument('--output', required=True,        help='出力ファイルパス')
    concat_common_parser.add_argument('--columns', nargs='*',           help="Columns to select from each CSV file")
    concat_common_parser.add_argument('--index-name', type=str,         help='Index name for the concatenated DataFrame. If not specified, index will not be included.')
    

    # Index方向ファイル結合コマンド
    concat_operation_subparsers.add_parser('by-index', parents=[concat_common_parser], help="Concatenate CSV files")
    
    
    args = parser.parse_args()

    if args.command == 'concat':
        # 結合戦略と実行者を初期化
        if args.generate_type == 'by-index':
            strategy = ConcatByIndexStrategy()
        
        executor = CSVConcatExecutor(strategy, 
                                    output_path = args.output, 
                                    columns     = args.columns, 
                                    index_name  = args.index_name)  
    else:
        parser.print_help()
        return
            
    # ==================================================================
    # 入出力ファイルの解決と処理実行
    # ==================================================================
    paths = resolve_files(args.input)
    print("Resolved file paths: ")
    for path in paths:
        print(f" - {path}")
    if not paths:
        print(f" - [警告] 入力パターンにマッチするファイルが見つかりません: {args.input}")
        return

    # 対象ファイルの解決
    # 対象ファイルが多い場合の確認
    # 30件以上のファイルが対象の場合、確認を行う
    MAX_FILES_BEFORE_WARNING = 30
    if len(paths) >= MAX_FILES_BEFORE_WARNING and not args.force:
        print(f"[警告] 対象ファイルが {len(paths)} 件あります。処理を続行しますか？ (y/N): ", end="")
        confirm = input().strip().lower()
        if confirm != 'y':
            print("処理を中止しました。")
            return


    # ==================================================================
    # 実行
    # ==================================================================
    output_files = executor.run(paths)
    if output_files:
        print("出力ファイル:")
        for output_file in output_files:
            print(f" - {output_file}")

if __name__ == '__main__':
    main()
    