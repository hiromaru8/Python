import ctypes

class DllWrapper:
    """
    DLLを読み込み、関数を実行するためのシングルトンクラスです。
    """
    #private
    __instance = None  # クラス変数 _instance はインスタンスの一意性を保証するための変数です
    __loaded = False  # クラス変数 _loaded はDLLの読み込み状態を示すフラグです

    def __new__(cls, dll_path):
        # インスタンスが
        # 存在しない場合は新規作成し、
        # 存在する場合は既存のインスタンスを返す
        if not cls.__instance:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    
    def __init__(self, dll_path):
        # 初回インスタンス生成時のみ、
        # DLLパスを設定およびDLLオブジェクトを初期化
        if not self.__loaded:
            self.dll_path = dll_path
            self.dll = None
          

    def load_dll(self):
        """
        DLLを読み込むメソッド
        初回の呼び出し時のみDLLを読み込む。
        ２回目以降は読み込まれない。
        """
        try:
            if not self.__loaded:
                self.dll = ctypes.WinDLL(self.dll_path)
                self.__loaded = True
                print("DLL loaded successfully.")

                #下記に関数の引数と戻り値の型を指定する。
                #......

            else:
                print("DLL is already loaded.")
            
            return 0
                
        except Exception as e:
            print(f"Failed to load DLL: {str(e)}")
            return -1
    
    def get_loaded_dll(self):
        return self.__loaded

    def execute_function(self, function_name, *args):
        """
        関数を実行するメソッド
        :param function_name: 実行する関数の名前
        :param args: 関数に渡す引数
        """
        try:
            if self.__loaded:
                # 指定された関数名の関数オブジェクトを取得
                function = getattr(self.dll, function_name)
                # 関数の戻り値の型を ctypes.c_int に設定
                function.restype = ctypes.c_int
                # 関数を引数と共に実行し、結果を取得
                result = function(*args)
                # 関数の実行結果を表示
                print(f"Function '{function_name}' executed successfully. Result: {result}")
            else:
                raise Exception("DLL is not loaded.")
        except Exception as e:
            print(f"Failed to execute function '{function_name}': {str(e)}")
    def __del__(self):
        """
        オブジェクトが破棄される際に呼び出されるデストラクタです。
        DLLを解放する処理を追加します。
        """
        if self.__loaded:
            # DLLの解放処理を追加する
            #ctypes.windll.kernel32.FreeLibrary(self.dll._handle)
            self.__loaded = False
            print("DLL unloaded.")



dll_path = "aaa"#input("Enter DLL path: ")

dll_wrapper = DllWrapper(dll_path)


if dll_wrapper.get_loaded_dll():
    print('DLL is already loaded')
else:
    print('DLL is not loaded')
    
if(0!=dll_wrapper.load_dll()):
    print("error")



if dll_wrapper.get_loaded_dll():
    print('DLL is already loaded')
else:
    print('DLL is not loaded')



"""
dll_wrapper.load_dll()
dll_path = "aaaj"#input("Enter DLL path: ")

dll_wrapper1 = DllWrapper(dll_path)

dll_wrapper1.load_dll()


print(dll_wrapper1.dll_path)



#dll_wrapper.execute_function("function_name", arg1, arg2)
"""