# 🔧 Binary File Tool

バイナリファイルを操作・生成するためのCLIツール。分割、抽出、hexdump表示、ファイル生成（インクリメントデータ／乱数）に対応。

---

## ✅ 特徴

* 任意サイズでのバイナリファイル分割
* 任意オフセットとサイズによるデータ抽出
* Hexdump形式での内容表示
* バイナリファイル生成
  * インクリメントデータによるファイル生成
  * セキュア乱数によるファイル生成
* ワイルドカードによる複数ファイル一括処理対応
* Strategyパターンによる拡張性の高い設計
* 変換
  * hexテキストをバイナリに変換
    * All
    * 行ごとにパース
      * 開始位置と終了位置を指定
      * hexdump相当

## 追加予定

* 変換
  * hexテキストをバイナリに変換
    * 行ごとにパース
      * 開始位置と終了位置を指定
      * hexdump相当
    * 列単位
