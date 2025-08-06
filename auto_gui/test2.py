from pywinauto import Desktop

for win in Desktop(backend="uia").windows():
    print(win.window_text())