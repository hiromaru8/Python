import tomllib

toml_path = "./setting_file/toml/config.toml"

with open(toml_path, "rb") as f:
    toml_data = tomllib.load(f)

def print_dict(d, indent=0):
    """ネストされた dict をインデント付きで表示"""
    for key, value in d.items():
        if isinstance(value, dict):
            print("  " * indent + f"[{key}]")
            print_dict(value, indent + 1)
        else:
            print("  " * indent + f"{key}: {value}")



print_dict(toml_data)
