import ctypes

from DllWrapper import DllWrapper

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

    def DLL_TEST1_Wrapper(self):
        print("==================")
        function_name = "ADD"
        c_value1 = ctypes.c_int(1)
        c_value2 = ctypes.c_int(2)
        if(0 == self.execute_intFunction(function_name,c_value1,c_value2)):
            print("added_value",self.funcReturn)
        else:
            print("error")

        print("==================")
        function_name = "test_ptr"
        c_ptr_value1 = ctypes.pointer(ctypes.c_int())
        self.execute_intFunction(function_name,c_ptr_value1,c_value1)
        print(hex(c_ptr_value1.contents.value))

        print("==================")
        function_name = "test_ptr_ptr"
        c_value3 = ctypes.c_int(100)
        c_ptr_value1 = ctypes.pointer(c_value3)
        c_dptr_value1 = ctypes.pointer(c_ptr_value1)
        print("c_ptr_value1",c_ptr_value1.contents)
        self.execute_intFunction(function_name,c_dptr_value1,c_value1)
        print("c_ptr_value1",c_ptr_value1.contents)
        print("c_dptr_value1",c_dptr_value1.contents.contents)
        print("==================")

        print("==================")
        function_name = "test_ptr_ptr"
        #64bitのメモリのため64bitの範囲で型を定義する。
        c_value3 = ctypes.c_uint64(100)
        c_ptr_value1 = ctypes.pointer(c_value3)
        print("c_ptr_value1",c_ptr_value1.contents)
        self.execute_intFunction(function_name,c_ptr_value1,c_value1)
        print("c_ptr_value1",hex(c_ptr_value1.contents.value))
        #アドレスデータを格納する
        addr_value = c_ptr_value1.contents.value #b'\x01\x02\x03\x04\x01\x02\x03\x04'
        #ctypes.c_void_p()でアドレスデータを初期化
        addr_as_ctypes = ctypes.c_void_p(addr_value) 
        #型を変換し、ポインタ型となる。
        new_ptr = ctypes.cast(addr_as_ctypes, ctypes.POINTER(ctypes.c_uint64))
        #addr_valueのアドレスを指し示す先のデータを取り出せる
        print("new_ptr",new_ptr.contents)

        """        data_type = ctypes.c_uint64(0)
                c_ptr_data = ctypes.cast(addr_as_ctypes,ctypes.pointer(data_type))
                print("c_ptr_data",ctypes.addressof(c_ptr_data))
        """
if __name__ == "__main__":
    dll_path = "D:\\Learnning\\Python\\Dll\\test\\Dll1_for_python.dll"#input("Enter DLL path: ")
    subDllWrapper1 = SubDllWrapper1(dll_path)
        
    if(0!=subDllWrapper1.load_dll()):
        print("error")

    subDllWrapper1.DLL_TEST1_Wrapper()
    



    import gc
    #del dll_wrapper
    del DllWrapper
    gc.collect()



    """
    #dll_wrapper.execute_function("function_name", arg1, arg2)
    """