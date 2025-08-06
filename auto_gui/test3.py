from pywinauto import Desktop

print("win32要素一覧:")
print(Desktop(backend="win32").windows())

print("uia要素一覧:")
print(Desktop(backend="uia").windows())
