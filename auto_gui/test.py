from pywinauto.timings import wait_until
from pywinauto.findwindows import ElementNotFoundError

from pywinauto.application import Application


# 「処理完了」などのポップアップウィンドウを待つ関数
def wait_for_popup(title_re, timeout=10):
    try:
        print("ポップアップを待っています...")
        # タイトルに正規表現を使ってポップアップを待つ
        wait_until(timeout, 1, lambda: app.window(title_re=title_re).exists())
        print("ポップアップが表示されました。")
        popup = app.window(title_re=title_re)
        popup.set_focus()
        return popup
    except Exception as e:
        print("ポップアップが表示されませんでした:", e)
        return None
    
# アプリを起動する例（exeパスを指定）
app = Application(backend="uia").start(r"D:\tools\tera\teraterm\ttermpro.exe")

# または既存のウィンドウに接続する例
# app = Application(backend="uia").connect(title_re=".*アプリタイトル.*")


popup = wait_for_popup(".*未接続.*", timeout=10)
if popup:
    try:
        button = "閉じる"
        popup[button].click()  # ボタンの名前で指定
        print(f"{button}ボタンをクリックしました。")
        
        
    except Exception:
        print(f"{button}ボタンが見つかりません。")
else:
    print("ポップアップが見つかりませんでした。")


window = app.window(title_re=".*未接続.*")

# タブを列挙してクリック（例：2番目のタブをクリック）
window.menu_select("ファイル(F)->新しい接続(N)...")

# メインウィンドウ内のすべての要素を探索
for ctrl in window.descendants():
    try:
        text = ctrl.window_text()
        if text.strip():  # 空でなければ表示
            print(f"[{ctrl.friendly_class_name()}] {text}")
    except Exception:
        pass
    