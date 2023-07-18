import ctypes

class DllWrapper:
    """
    DLLを読み込み、関数を実行するためのシングルトンクラスです。
    """
    #pseudo private
    __instance = None  # クラス変数 _instance はインスタンスの一意性を保証するための変数です
    __loaded = False  # クラス変数 _loaded はDLLの読み込み状態を示すフラグです

    def __new__(cls, dll_path):
        """
        If the instance does not exist, create a new one;\n
        if it exists, return the existing instance.
        """
        #print(cls.__instance)
        if not cls.__instance:
            cls.__instance = super().__new__(cls) 
            print("new instance")
        else:
            print("instance is already generated")
        return cls.__instance

    
    def __init__(self, dll_path):
        """初回インスタンス生成時のみDLLパスを設定およびDLLオブジェクトを初期化
        """

        if not self.__loaded:
            self.dll_path = dll_path
            self.dll = None
          

    def load_dll(self):
        """
        Method for loading DLL.\n
        - Load the DLL only during the first call.\n
        - It will not be loaded again from the second call onwards.\n
        Return value\n
        - 0 : Normal responce\n
        - -1: error
        """
        try:
            if not self.__loaded:
                #self.dll = ctypes.WinDLL(self.dll_path)
                self.__loaded = True
                print("DLL loaded successfully.")

            else:
                print("DLL is already loaded.")

            return 0
                
        except Exception as e:
            print(f"Failed to load DLL: {str(e)}")

            return -1
    
    def get_loaded_dll(self):
        """
        Method that returns whether the DLL is loaded\n
        Args:
            none
        Returns:
            True: DLL is already loaded\n
            False:  DLL is not loaded\n
        """
        return self.__loaded


    def execute_intFunction(self, function_name, *args):
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




class SubDllWrapper1(DllWrapper):
    """
    専用のDLLを読み込み、関数を実行するためのサブクラスです。
    """
    #pseudo private
    __instance = None  # クラス変数 _instance はインスタンスの一意性を保証するための変数です
    __loaded = False  # クラス変数 _loaded はDLLの読み込み状態を示すフラグです

    def __new__(cls, dll_path):
        """
        Override the method(__new__) of the parent class.
        If the instance does not exist, create a new one;\n
        if it exists, return the existing instance.
        """
        #print(cls.__instance)
        if not cls.__instance:
            cls.__instance = object.__new__(cls) 
            print("new instance")
        else:
            print("instance is already generated")
        return cls.__instance

    
    def __init__(self, dll_path):
        """
        初回インスタンス生成時のみDLLパスを設定およびDLLオブジェクトを初期化
        """
        if not self.__loaded:
            self.dll_path = dll_path
            self.dll = None



class SubDllWrapper2(DllWrapper):
    """
    専用のDLLを読み込み、関数を実行するためのサブクラスです。
    """



if __name__ == "__main__":
    dll_path = "aaa"#input("Enter DLL path: ")
    dll_path1 = "aaa"#input("Enter DLL path: ")
    dll_path2 = "bbb"#input("Enter DLL path: ")
    dllWrapper = DllWrapper(dll_path)
    subDllWrapper1 = SubDllWrapper1(dll_path1)
    subDllWrapper2 = SubDllWrapper2(dll_path2)
        
    if(0!=subDllWrapper1.load_dll()):
        print("error")


    if subDllWrapper1.get_loaded_dll():
        print('DLL is already loaded')
    else:
        print('DLL is not loaded')
    

    if(0!=subDllWrapper2.load_dll()):
        print("error")

    subDllWrapper2.get_loaded_dll()

    import gc
    #del dll_wrapper
    del DllWrapper
    gc.collect()



    """
    #dll_wrapper.execute_function("function_name", arg1, arg2)
    """