from setting_file.toml import toml_utils

in_toml_path_1 = "./setting_file/toml/test_data/sample1.toml"


print(toml_utils.toml_to_dict(in_toml_path_1))