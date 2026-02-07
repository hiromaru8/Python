"""
my_toml_tool.py
TOML操作用ユーティリティ
標準ライブラリの tomllib を使用
Author: H.Y.
Created: 2025-08-23
"""

import tomllib
from typing import Any
from datetime import datetime, date, time,timedelta


def load_toml(path: str) -> dict[str, Any]:
    """
    TOMLファイルを読み込み、Pythonの辞書に変換する。
    * 読み込み用の汎用関数
    * ファイルパスを渡すだけで辞書が返る

    Args:
        path (str): 読み込むTOMLファイルのパス

    Raises:
        FileNotFoundError   : 指定されたファイルが見つからない場合
        ValueError          : TOML形式が不正な場合
        RuntimeError        : その他の予期しないエラーが発生した場合

    Returns:
        dict: TOMLファイルの内容を辞書で返す
    """
    try:
        # TOMLファイルはバイナリモードで開く
        with open(path, "rb") as f:
            # # tomllibを使ってTOMLファイルを読み込み、辞書に変換
            return tomllib.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"{path} が見つかりません")
    except tomllib.TOMLDecodeError as e:
        raise ValueError(f"TOML形式エラー: {e}")
    except Exception as e:
        raise RuntimeError(f"予期しないエラー: {e}")

def to_toml_value(value: Any) -> str:
    """Pythonの値をTOML表現に変換する。

    Args:
        value (Any): 変換する値

    Raises:
        TypeError: TOML未対応の型の場合に発生

    Returns:
        str: TOML形式の文字列
    """
    
    # 値が文字列の場合、TOMLの文字列形式で出力（ダブルクォートで囲む）
    if isinstance(value, str):
        return f"\"{value}\""
    # 値がブール値の場合、TOMLのtrue/false形式に変換して出力
    elif isinstance(value, bool):
        return "true" if value else "false"
    # 値が数値の場合、そのまま文字列化して出力
    elif isinstance(value, (int, float)):
        return str(value)
    # 値が日付の場合、ISOフォーマットで出力
    elif isinstance(value, datetime):
        # UTC の場合は Z を末尾に付ける
        if value.tzinfo is not None and value.utcoffset() == timedelta(0):
            return value.isoformat().replace("+00:00", "Z")
        else:
            return value.isoformat()        
    elif isinstance(value, date):
        return value.isoformat()  # 'YYYY-MM-DD'
    elif isinstance(value, time):
        return value.isoformat()  # 'HH:MM:SS'
    # 値がリストの場合、各要素をTOML形式に変換して出力
    elif isinstance(value, list):
        return "[" + ", ".join(to_toml_value(x) for x in value) + "]"
    elif value is None:
        # 将来 Optional[str] 等をサポートしたい場合は null を書き出す
        return "null"
    else:
        raise TypeError(f"TOML未対応の型: {type(value)} : {value}")

def dict_to_toml(d: dict, prefix: str = "") -> str:
    """
    Pythonの辞書（dict）をTOML形式の文字列に変換する再帰関数。

    ネストされた辞書は `[section]` や `[section.subsection]` の形式で表現され、
    文字列、数値、ブール値をTOML形式としてシリアライズします。

    Args:
        d (dict): TOMLに変換する辞書。キーが文字列、値が文字列・数値・ブール値・辞書であること。
        prefix (str, optional): ネストされた辞書のセクション名を連結する際の接頭辞。
                                再帰呼び出し用。通常は空文字列のまま使用。 Defaults to "".
    Returns:
        str: 辞書をTOML形式に変換した文字列
    """
    lines = []  # TOML形式の各行を格納するリストを初期化

    # 辞書のキーと値を順に取り出す
    for key, value in d.items(): 
        # セクション名を作成。prefixがある場合は "prefix.key" としてネストを表現
        section_name = f"{prefix}.{key}" if prefix else key

        # 値が辞書の場合はネストされたセクションとして扱う
        # 通常のセクション
        if isinstance(value, dict):
            # [section_name] の形式でTOMLのセクションを開始
            if not value:
                # 空辞書の場合はセクションのみ出力するか、スキップするか選択
                lines.append(f"\n[{section_name}]  # 空セクション")
            else:
                lines.append(f"\n[{section_name}]")
                # 再帰呼び出しでネストされた辞書を文字列に変換し、linesに追加
                lines.append(dict_to_toml(value, section_name))
        
        # list内がdictの場合はテーブル配列として扱う
        elif isinstance(value, list) and all(isinstance(item, dict) for item in value):
            # 各辞書をTOML形式に変換してlinesに追加
            for item in value:
                if not item:
                    # 空の dict を含む場合も [[table]] のみ出力
                    lines.append(f"\n[[{section_name}]]  # 空テーブル")
                else:
                    lines.append(f"\n[[{section_name}]]")
                    lines.append(dict_to_toml(item, section_name))
                
        # 値が辞書でない場合は key = value の形式で追加
        else:
            # to_toml_valueで値をTOML形式に変換してから追加
            lines.append(f"{key} = {to_toml_value(value)}")
            
    # linesリストの各要素を改行で結合し、1つのTOML形式文字列として返す
    return "\n".join(lines)

def save_toml(data: dict, path: str, encoding="utf-8") -> None:
    """
    Pythonの辞書をTOML形式に変換してファイルに保存する。
    * dict_to_toml をラップした便利関数
    * ファイル書き込みまで一括で行える

    Args:
        data (dict): 保存する辞書
        path (str): 保存先のTOMLファイルパス
        encoding (str, optional): ファイルのエンコーディング。 Defaults to "utf-8".
    """
    # 辞書をTOML形式の文字列に変換
    toml_str = dict_to_toml(data)
    # ファイルに書き込む
    with open(path, "w", encoding=encoding) as f:
        f.write(toml_str)

def concat_toml(*paths: str) -> dict:
    """
    複数のTOMLファイルをマージして1つの辞書にまとめる。

    Args:
        *paths (str): マージするTOMLファイルのパス

    Returns:
        dict: マージ後の辞書
    """
    # 各TOMLファイルを辞書に読み込む
    dicts = [load_toml(path) for path in paths]
    # 辞書をマージして返す
    return concat_toml_dicts(*dicts)


def concat_toml_dicts(*dicts: dict) -> dict:
    """
    複数のTOML辞書を再帰的にマージして1つの辞書にまとめる。
    後ろの辞書のキーで上書きされる。

    Args:
        *dicts (dict): マージする辞書

    Returns:
        dict: マージ後の辞書
    """
    result: dict = {}
    for d in dicts:
        for k, v in d.items():
            if isinstance(v, dict) and k in result and isinstance(result[k], dict):
                result[k] = concat_toml_dicts(result[k], v)
            else:
                result[k] = v
    return result


def has_key_path(d: dict, path: str) -> bool:
    """
    辞書内にネストされたキーのパスが存在するかチェックする。
    パスはドット区切りで指定。

    Args:
        d (dict): チェック対象の辞書
        path (str): "section.subsection.key" の形式

    Returns:
        bool: キーが存在すれば True
    """
    
    # pathをドットで分割してキーのリストを作成
    keys = path.split(".")

    # 現在の辞書を保持する変数
    current = d
    for k in keys:
        # 現在の辞書がdictであり、キーが存在する場合はその値に移動
        if isinstance(current, dict) and k in current:
            # 現在の辞書を更新
            current = current[k]
        else:
            # キーが存在しない場合は False を返す
            return False
        # すべてのキーが存在した場合は True を返す
    return True

def get_key_path(d: dict, path: str, default=None):
    """
    ネストされた辞書からキーの値を取得する。

    この関数は、辞書内のキー階層をドット区切りで指定してアクセスできるようにする。
    例えば {"a": {"b": {"c": 1}}} に対して "a.b.c" を指定すると 1 を返す。

    Args:
        d (dict): 辞書データ
        path (str): ドット区切りのキー (例: "section.subsection.key")
        default: キーが存在しない場合の返り値

    Returns:
        Any: キーが存在すればその値、存在しなければ default
    """
    # ドットで分割してキーのリストを作成
    keys = path.split(".")
    # 現在の辞書を保持する変数
    current = d

    # キーのリストを順にたどる
    for k in keys:
        # 現在の辞書がdictであり、キーが存在する場合はその値に移動
        if isinstance(current, dict) and k in current:
            # 現在の辞書を更新
            current = current[k]
        else:
            # キーが存在しない場合は default を返す
            return default
        # 現在の辞書が空でない場合はその値を返す
    return current

def get_value_path(d: dict, path: str, default=None):
    """
    ネストされた辞書から「最終的な値のみ」を取得する。

    get_key_path との違い:
        - get_key_path: 辞書の階層をたどって最終的に dict でも返す
        - get_value_path: 最終結果が dict の場合は「値ではない」として default を返す

    つまり、設定値やスカラー値を安全に取得したい場合に使う。

    Args:
        d (dict): 辞書データ
        path (str): ドット区切りのキー (例: "section.subsection.key")
        default: キーが存在しない場合、または dict が返った場合の返り値

    Returns:
        Any: スカラー値 (str, int, float, bool など) または default
    """
    # まずは get_key_path で値を取得    
    data = get_key_path(d, path, default=default)
    
    # 辞書が返ってきた場合は default を返す
    if isinstance(data, dict):
        return default

    # 辞書でない（スカラー値など）値を返す
    return data


def print_toml_readable(data: dict) -> None:
    """
    辞書をTOML形式として標準出力する。

    Args:
        data (dict): 出力したい辞書
    """
    print(dict_to_toml(data))
    
    
def print_toml(data: dict, prefix=""):
    """TOMLを再帰的に辿って、キー・値・型を表示"""
    if isinstance(data, dict):
        for key, value in data.items():
            full_key = f"{prefix}.{key}" if prefix else key
            if isinstance(value, dict):
                print(f"[{full_key}] (table)")
                print_toml(value, full_key)
            elif isinstance(value, list):
                print(f"{full_key} = {value} (list[{len(value)}])")
                for i, item in enumerate(value):
                    print(f"    {full_key}[{i}] -> {item!r} ({type(item).__name__})")
            else:
                print(f"{full_key} = {value!r} ({type(value).__name__})")
    else:
        print(f"{prefix} = {data!r} ({type(data).__name__})")




if __name__ == "__main__":
    import os
    in_toml_path_1 = "./setting_file/toml/test_data/sample1.toml"
    in_toml_path_2 = "./setting_file/toml/test_data/sample2.toml"
    out_toml_path = os.path.join(os.path.abspath(os.path.dirname(in_toml_path_1)), "out.toml")


    # 複数のTOMLファイルをマージ
    dict_toml_data = concat_toml(in_toml_path_1, in_toml_path_2)

    # 辞書をTOML形式の文字列に変換
    toml_data: str = dict_to_toml(dict_toml_data)

    # TOML文字列をファイルに書き込む
    save_toml(dict_toml_data, out_toml_path)

    # 書き込んだTOMLファイルを再読み込み
    loaded: dict = load_toml(out_toml_path)

    # 再読み込みした内容をTOML形式として出力
    print_toml_readable(loaded)

    print("---- key path check ----")
    print(has_key_path(loaded, "database.server"))
    print(has_key_path(loaded, "servers.alpha.ip"))
    
    print("---- get key path ----")
    print(get_key_path(loaded, "servers.alpha.ip"))
    print(get_key_path(loaded, "servers.alpha.role"))

    print("---- get value path ----")
    print(get_value_path(loaded, "title", default= False))
    print(get_value_path(loaded, "servers.alpha.t", default= False))
    print(get_value_path(loaded, "servers.alpha.ip", default= False))
    
    import pprint
    import json
    pprint.pprint(loaded)

    # JSON形式で出力
    print(json.dumps(loaded, indent=4, default=str, ensure_ascii=False))

