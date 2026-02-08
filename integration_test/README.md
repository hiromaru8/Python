# Integration Test Template (Standard Library Only)

## 概要

Python標準ライブラリのみで構成された結合試験テンプレート。

- unittestベース
- 試験担当が test_selection.json を編集
- 実行: python run_tests.py
- ログ出力: reports/integration_test.log

## 実行方法

```bash
python run_tests.py
```

## 試験選択

config/test_selection.json の execute に
実行したい TEST_ID を記載する。

## 注意事項

TEST_ID を持たないテストは実行されない

test_selection.json に存在しないIDは警告出力



