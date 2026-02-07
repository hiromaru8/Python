# Tkinterライブラリのインポート（Pythonに標準搭載されているGUIツールキット）
import tkinter as tk
from tkinter import Entry, Label, Button  # 型アノテーション用（任意）

# 関数 calc(): 入力欄に入力された式を評価して、結果をラベルに表示する
def calc() -> None:
    try:
        # Entryウィジェットから文字列を取得し、evalで式として評価
        result: float = eval(entry.get())  # 入力が "2+3" なら 5 に評価される
        label.config(text=f"結果: {result}")  # ラベルのテキストを更新
    except Exception as e:
        # 式の評価に失敗した場合（例：空欄、文法エラーなど）
        label.config(text="エラー")

# アプリケーションのメインウィンドウを作成
root: tk.Tk = tk.Tk()
root.title("ミニ電卓")        # ウィンドウのタイトル
root.geometry("300x150")     # ウィンドウのサイズ（任意）

# Entry（1行のテキスト入力欄）を作成
entry: Entry = tk.Entry(root, font=("Arial", 14))
entry.pack(pady=10)  # 上下に10ピクセルの余白を設定

# Button（ボタン）を作成。クリックすると calc 関数が実行される
button: Button = tk.Button(root, text="計算", font=("Arial", 12), command=calc)
button.pack(pady=5)

# Label（結果を表示するラベル）を作成
label: Label = tk.Label(root, text="ここに結果", font=("Arial", 12))
label.pack(pady=10)

# イベントループを開始（ウィンドウの表示とイベント処理）
root.mainloop()
# これにより、ウィンドウが表示され、ユーザーの操作を待ち受ける