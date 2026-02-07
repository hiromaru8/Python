

def print_dict(d:dict, indent: int=0)->None:
    """ネストされた dict をインデント付きで表示"""
    for key, value in d.items():
        if isinstance(value, dict):
            print("  " * indent + f"[{key}]")
            print_dict(value, indent + 1)
        else:
            print("  " * indent + f"{key}: {value}")
