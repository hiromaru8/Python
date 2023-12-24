import numpy as np

def test1():
    byte_data = bytes([1,2,3,4,10,255])
    
    print([hex(i) for i in byte_data])

    np_data = np.frombuffer(byte_data, dtype=np.uint8)

    print([hex(i) for i in np_data])
    
    print(type(np_data.dtype))
    

def test2():
    """エンディアンについて確認する。
    実行例
        littleエンディアンのCPUで確認。
            基本は、littelで変換される。
            Bigエンディアンにするには、「.newbyteorder('>')」で変換する。
    """
    
    byte_data = bytes(range(0,256))
    
    np_data_uint8 = np.frombuffer(byte_data, dtype=np.uint8)
    # ['0x0', '0x1', '0x2', ...]
    print([hex(i) for i in np_data_uint8])
    
    print("--CPUのエンディアンに依存しているであろうことを確認")
    np_data_uint64_def = np.frombuffer(byte_data, dtype=np.uint64)
    # CPU　littleの場合下記となる。
    # HEX ['0x706050403020100', '0xf0e0d0c0b0a0908',...] 
    # Dec [  506097522914230528  1084818905618843912...] 
    print([hex(i) for i in np_data_uint64_def[:2]])
    print(np_data_uint64_def[:2])
    
    print("--dtypeを現在のエンディアンから反対側のエンディアンにスワップ")
    np_data_uint64_S = np.frombuffer(byte_data, dtype=np.uint64).newbyteorder('S')
    # CPU　littleの場合下記となる。
    # HEX ['0x1020304050607', '0x8090a0b0c0d0e0f', ...]
    # Dec [   283686952306183 579005069656919567, ...]
    print([hex(i) for i in np_data_uint64_S[:2]])
    print(np_data_uint64_S[:2])
    
    print("--Littelに強制")
    np_data_uint64_l = np.frombuffer(byte_data, dtype=np.uint64).newbyteorder('<')
    # HEX ['0x706050403020100', '0xf0e0d0c0b0a0908',...] 
    # Dec [  506097522914230528  1084818905618843912...] 
    print([hex(i) for i in np_data_uint64_l[:2]])
    print(np_data_uint64_l[:2])
    print("--BIGに強制")
    np_data_uint64_big = np.frombuffer(byte_data, dtype=np.uint64).newbyteorder('>')
    # HEX ['0x1020304050607', '0x8090a0b0c0d0e0f', ...]
    # Dec [   283686952306183 579005069656919567, ...]
    print([hex(i) for i in np_data_uint64_big[:2]])
    print(np_data_uint64_big[:2])
    
    print("--nativeに強制")
    np_data_uint64_n = np.frombuffer(np_data_uint64_big, dtype=np.uint64).newbyteorder('=')
    # CPU　littleの場合下記となる。
    # big エンディアンだったものがlittleに戻る
    # HEX ['0x706050403020100', '0xf0e0d0c0b0a0908',...] 
    # Dec [  506097522914230528  1084818905618843912...] 
    print([hex(i) for i in np_data_uint64_n[:2]])
    print(np_data_uint64_n[:2])
    
    print("--ignore ")
    np_data_uint64_i = np.frombuffer(np_data_uint64_big, dtype=np.uint64).newbyteorder('|')
    # CPU　littleの場合下記となる。
    # big エンディアンだったものがlittleに戻る
    # HEX ['0x706050403020100', '0xf0e0d0c0b0a0908',...] 
    # Dec [  506097522914230528  1084818905618843912...] 
    print([hex(i) for i in np_data_uint64_i[:2]])
    print(np_data_uint64_i[:2])
    
    
def test3():
    """test2のエンディアンの確認において
        np.uint8からの変換においても確認してみる
        結果は一緒
    """
    byte_data = bytes(range(0,256))
    
    np_data_uint8 = np.frombuffer(byte_data, dtype=np.uint8)
    
    print("--CPUのエンディアンに依存しているであろうことを確認")
    np_data_uint64_lit = np.frombuffer(np_data_uint8, dtype=np.uint64)
    # littleの場合下記となる。
    # HEX ['0x706050403020100', '0xf0e0d0c0b0a0908',...] 
    # Dec [  506097522914230528  1084818905618843912...] 
    print([hex(i) for i in np_data_uint64_lit[:2]])
    print(np_data_uint64_lit[:2])
    
    print("--dtypeを現在のエンディアンから反対側のエンディアンにスワップ")
    np_data_uint64_big = np.frombuffer(np_data_uint8, dtype=np.uint64).newbyteorder('S')
    # CPU　littleの場合下記となる。
    # HEX ['0x1020304050607', '0x8090a0b0c0d0e0f', ...]
    # Dec [   283686952306183 579005069656919567, ...]
    print([hex(i) for i in np_data_uint64_big[:2]])
    print(np_data_uint64_big[:2])


if __name__ == "__main__":

    test2()