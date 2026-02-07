# 要件

## ユースケース

* テストの実行
  * 作成の妥当性
    * 全てのレコードがあるか
      * 指定した数の組み合わせ
      * 指定した数
    * データに誤りがないか
    * データの抽出とファイルへ
  * 検証の妥当性
    * データの書き換え
  * sqliteへの操作
    * データベースの作成
      * 初回
        * テーブルの作成
      * 2回目以降は再利用
      * オプション 
        * 存在すれば初回と同じ
    * レコードの追加
    * レコードの修正（更新）
    * レコードから特定のカラムを抽出
    * レコードからすべてのカラムを抽出

テーブルは下記
CREATE TABLE combination_unit (
    src_id      INTEGER,
    dest_id     INTEGER,
    data1       blob,
    data2       blob,
    PRIMARY KEY (src_id, dest_id);
)
CREATE TABLE single_unit (
    id      INTEGER,
    data1       blob,
    data2       blob,
    PRIMARY KEY (id);
)
