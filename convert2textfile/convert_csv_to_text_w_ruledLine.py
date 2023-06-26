import pandas as pd

def convert_csv_to_text_w_ruledLine(csv_file):
    # CSVファイルを読み込む
    df = pd.read_csv(csv_file)

    # 表をテキスト形式に変換する
    text = ""
    for _, row in df.iterrows():
        for value in row:
            text += str(value) + "│"
        text += "\n━━━" * len(row) + "\n"

    return text

# CSVファイルのパスを指定して変換する
csv_file = "path/to/your/csv/file.csv"
converted_text = convert_csv_to_text_w_ruledLine(csv_file)

# 変換結果を表示する
print(converted_text)
