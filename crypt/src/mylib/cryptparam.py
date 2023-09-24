import json
from typing import List
import logging
import os


script_path = os.path.abspath(__file__)
file_name = os.path.relpath(script_path)
# module_logger = logging.getLogger('loggingSample.sub_module')
module_logger = logging.getLogger('__main__').getChild(file_name)



class Param2:
    a: List[str]
    b: str

    def __init__(self, a: List[str], b: str) -> None:
        self.validate_param2(a, b)
        self.a = a
        self.b = b

    def validate_param2(self, a: List[str], b: str) -> None:
        if not isinstance(a, list) or not all(isinstance(item, str) for item in a):
            raise ValueError("Invalid value for 'a' in Param2")
        if not isinstance(b, str):
            raise ValueError("Invalid value for 'b' in Param2")

class CryptParam:
    param1: List[List[int]]
    param2: Param2
    param3: List[str]

    def __init__(self, param1: List[List[int]], param2: Param2, param3: List[str]) -> None:

        try :
            module_logger.info('start Class CryptParam ')

            self.validate_param1(param1)
            self.validate_param3(param3)
            self.param1 = param1
            self.param2 = param2
            self.param3 = param3

            [(module_logger.info(f"param1_{index} : {row}")) for index, row in enumerate(self.param1)]
            module_logger.info(f"param2.A : {self.param2.a}")
            module_logger.info(f"param2.B : {self.param2.b}")
            module_logger.info(f"param3   : {self.param3}")
        finally :
            module_logger.info('end Class CryptParam')

    def validate_param1(self, param1: List[List[int]]) -> None:
        if not isinstance(param1, list) or \
           not all(isinstance(row, list) and all(isinstance(item, int) for item in row) for row in param1):
            
            raise ValueError("Invalid value for 'param1' in CryptParam")

    def validate_param3(self, param3: List[str]) -> None:
        # print(type(param3))
        # print(type(param3[0]))
        if not isinstance(param3, list) or \
            not all(isinstance(item, str) for item in param3):
            raise ValueError("Invalid value for 'param3' in CryptParam")
        

if __name__ == "__main__":


    # ロガー（loggingSample）の作成
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # ファイルハンドラーの作成とログレベルの設定
    fh = logging.FileHandler('log\\app.log')
    fh.setLevel(logging.DEBUG)

    # フォーマッターの作成
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)

    # ハンドラーの追加
    logger.addHandler(fh)


    json_file = 'data/param.json'
    try:

        with open(json_file, 'r') as file:
            data = json.load(file)

        cryptparam = CryptParam(
            data.get("param1", []),
            Param2(data["param2"]["A"], data["param2"]["B"]),
            data.get("param3", [])
        )

        [print(f"param1_{index} : {row}") for index, row in enumerate(cryptparam.param1)]
        print(f"param2.A : {cryptparam.param2.a}")
        print(f"param2.B : {cryptparam.param2.b}")
        print(f"param3   : {cryptparam.param3}")



    except FileNotFoundError:
        message = f"Error: File not found: {json_file}"
        logger.error(message)
        print(message)
    except json.JSONDecodeError:
        message = f"Error: JSON decoding failed for file: {json_file}"
        logger.error(message)
        print(message)
    except ValueError as e:
        message = f"Error: {str(e)}"
        logger.error(message)
        print(message)
    except Exception as e:
        message = f"Error: An unexpected error occurred: {str(e)}"
        logger.error(message)
        print(message)
