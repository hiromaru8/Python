# Tkinterモジュールをインポート
import tkinter as tk

# ① メインウィンドウ（アプリケーションの土台）を作成
root = tk.Tk()  # インスタンス名は慣習的に root がよく使われる

# ② ウィンドウのタイトルを設定
root.title("はじめてのTkinterアプリ")

# ③ ウィンドウのサイズを設定（幅x高さ）
root.geometry("300x200")

# ④ ラベル（テキストを表示する部品）を作成
label = tk.Label(
    root,              # 親ウィジェット（今回はメインウィンドウ）
    text="こんにちは、Tkinter！",  # 初期テキスト
    font=("Arial", 14) # フォント指定（任意）
)

# ⑤ ラベルを画面に配置
label.pack(pady=20)  # 上下に20ピクセルの余白

# ⑥ ボタンが押されたときに呼び出す関数を定義
now = 0
def on_click():
    global now
    
    if now == 0:
        # 初回のクリック時にラベルのテキストを変更
        label.config(text="ボタンが押されました！")
        now = 1
        button.config(text="戻る")
    elif now == 1:
        # 2回目のクリック時にラベルのテキストを変更
        label.config(text="こんにちは、Tkinter！")
        now = 0
        button.config(text="押してね")


button = tk.Button(
    root,               # 親ウィジェット
    text="押してね",    # ボタンに表示する文字
    command=on_click,   # 押されたときに呼び出される関数
    font=("Arial", 12)
)

# ⑧ ボタンを画面に配置
button.pack()
# ⑨ メインループを開始（イベントを待ち受けるループ）
# これを呼び出すことでウィンドウが表示され、閉じられるまでアプリが動作する
root.mainloop()
