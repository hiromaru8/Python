import numpy as np
import bitextraction as be
import bitrotate as br


def test(file :str ):
    
    with open(file ,"rb") as f :
        
        data = f.read()
        

    # 拡張
    data_24 = data.ljust(24,b'\x00')

    # Numpy処理へ
    # numpy のint64bit ビッグエンディアンへ
    # 以降の処理でビット演算等でuintでは処理できないため、intとする。
    sync_np_array = np.frombuffer(data_24, dtype=np.int64).newbyteorder('>')

    # 

    A       = be.mid_1data_int64(sync_np_array[0],0,51)
    A_d     = be.mid_1data_int64(sync_np_array[0],32,19)
    B=be.mid_2data_int64(sync_np_array[0],sync_np_array[1],51,0,51)

    # config
    setA   = np.bitwise_not(A)& 0x7ffffffffffff 

    tmp_a = br.rotate_left_inRrange(A,A_b,51)

    setB = np.bitwise_xor(B,tmp_a)

    set_data0 = be.mid_1data_int64toint32(setA,13,32)


    out=np.zeros(5,dtype=np.int32)
    print(f"out{type(out[0])}")
    
    out[0]=set_data0
    out[1]=set_data0
    out[2]=set_data0
    out[3]=set_data0
    out[4]=set_data0
   
    print([hex(i) for i in out])
    print([hex(i) for i in out.byteswap().tobytes()])
    
    
if __name__ == "__main__":
    
    test("bit//random_file.bin")
