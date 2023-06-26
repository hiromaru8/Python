import pandas as pd
import pyperclip

def convert_csv_to_text_w_ruledLine(csv_file):
    # CSVファイルを読み込む
    df = pd.read_csv(csv_file)

    # 各列の最大幅を取得
    col_widths = [df[col].astype(str).str.len().max() for col in df.columns]

    # 表をテキスト形式に変換する
    text = ""
    for _, row in df.iterrows():
        for i, value in enumerate(row):
            text += str(value).ljust(col_widths[i]) + "|"
        text += "\n"
        #text += "-" * (sum(col_widths) + len(col_widths) - 1) + "\n"

    return text

# CSVファイルのパスを指定して変換する
csv_file = "D:\\download\\file.csv"
converted_text = convert_csv_to_text_w_ruledLine(csv_file)

# 変換結果を表示する
print(converted_text)

# 変換結果をクリップボードにコピーする
pyperclip.copy(converted_text)
