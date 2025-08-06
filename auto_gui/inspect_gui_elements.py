from pywinauto import Desktop, Application

def print_control_tree(elem, indent=0):
    """
    再帰的にGUI要素ツリーを表示する関数。

    Args:
        elem: pywinautoのWrapperオブジェクト。探索対象のGUI要素。
        indent: int。階層表示のインデントレベル（再帰で使用）。

    Note:
        - UIAバックエンドの場合、element_infoから control_type, class_nameを取得。
        - Win32バックエンドの場合は class_name と window_text を使用。
        - 例外発生時はエラーメッセージを表示し探索継続。
    """
    try:
        # UIAとWin32で属性取得が異なるため分岐
        if hasattr(elem, 'element_info'):
            control_type = getattr(elem.element_info, 'control_type', '')
            class_name = getattr(elem.element_info, 'class_name', '')
        else:
            control_type = ''
            class_name = elem.class_name() if hasattr(elem, 'class_name') else ''

        # ウィンドウテキスト（表示文字列）
        text = elem.window_text() if hasattr(elem, 'window_text') else ''

        # インデント付きで表示
        print("  " * indent + f"- [{control_type}] '{text}' ({class_name})")

        # 子要素も再帰表示
        for child in elem.children():
            print_control_tree(child, indent + 1)

    except Exception as e:
        print("  " * indent + f"(Error accessing element: {e})")


def main(app_title_regex, backend="uia"):
    """
    指定したタイトルを持つウィンドウ群から対象を選択し、
    そのウィンドウのGUI要素ツリーを探索・表示する。

    Args:
        app_title_regex: str。対象ウィンドウのタイトルの正規表現。
        backend: str。pywinautoのバックエンド。'uia' または 'win32'。

    Usage:
        main(".*Tera Term.*", backend="uia")
    """

    # 1. まずDesktopで該当ウィンドウをすべて取得（visible_only=Falseで隠しも含む）
    windows = Desktop(backend=backend).windows(title_re=app_title_regex, visible_only=False)

    if not windows:
        print(f"対象ウィンドウが見つかりませんでした: {app_title_regex}")
        return

    print(f"見つかったウィンドウ数: {len(windows)}")
    for i, w in enumerate(windows):
        print(f"[{i}] タイトル: {w.window_text()}")

    # 2. ユーザーが操作したいウィンドウを番号で選択（ここでは0番を選択）
    #    実際には input() で動的に取得することも可能
    target_index = 0
    target_window = windows[target_index]

    print(f"\n選択されたウィンドウ: [{target_index}] {target_window.window_text()}")

    # 3. Applicationオブジェクトに接続（ハンドル指定で確実）
    app = Application(backend=backend).connect(handle=target_window.handle)
    dlg = app.window(handle=target_window.handle)

    # 4. 再帰的にコントロールツリーを表示
    print("\n=== GUIコントロールツリー ===")
    print_control_tree(dlg)


if __name__ == "__main__":
    # ここを書き換えて対象ウィンドウのタイトルを指定する
    main(app_title_regex=".*Tera Term.*", backend="uia")
