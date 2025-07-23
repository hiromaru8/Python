import pandas as pd
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="CSVカラムを列方向に結合（pandas使用）")
    parser.add_argument(
        "--file", nargs="+", action="append", metavar=("FILE", "COL1", "COL2", "..."),
        required=True, help="CSVファイルと抽出カラム名（複数指定可）"
    )
    parser.add_argument("--output", default="merged_output.csv", help="出力ファイル名")
    return parser.parse_args()

def main():
    args = parse_args()

    dfs = []
    for entry in args.file:
        filepath, *columns = entry
        df = pd.read_csv(filepath, usecols=columns)
        df.reset_index(drop=True, inplace=True)
        dfs.append(df)

    # 列方向に結合、カラム名の重複OK
    merged_df = pd.concat(dfs, axis=1)

    # 保存（インデックスなし）
    merged_df.to_csv(args.output, index=False)

if __name__ == "__main__":
    main()
