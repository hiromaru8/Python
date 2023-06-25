"""
affine変換(AES SUBBYTES()処理の affine変換)を実施する
    affine変換の式は下記（詳細はFIPS197を参照のこと）
    b'i = b~i xor b~(i+4)mod8   xor b~(i+5)mod8 xor b~(i+6)mod8 xor b~(i+7)mod8 xor ci
        b' : affine変換の結果
        b~ : SubByteへの入力bの乗法逆元
        c  : 定数(0x63)
    行列式は下記
        |b'0|   |1,0,0,0,1,1,1,1| |b~0|   |1|
        |b'1|   |1,1,0,0,0,1,1,1| |b~1|   |1|
        |b'2|   |1,1,1,0,0,0,1,1| |b~2|   |0|
        |b'3| = |1,1,1,1,0,0,0,1| |b~3| + |0|
        |b'4|   |1,1,1,1,1,0,0,0| |b~4|   |0|
        |b'5|   |0,1,1,1,1,1,0,0| |b~5|   |1|
        |b'6|   |0,0,1,1,1,1,1,0| |b~6|   |1|
        |b'7|   |0,0,0,1,1,1,1,1| |b~7|   |0|
Invaffine変換の場合
        |b'0|   |0,0,1,0,0,1,0,1| |b~0|   |1|
        |b'1|   |1,0,0,1,0,0,1,0| |b~1|   |0|
        |b'2|   |0,1,0,0,1,0,0,1| |b~2|   |1|
        |b'3| = |1,0,1,0,0,1,0,0| |b~3| + |0|
        |b'4|   |0,1,0,1,0,0,1,0| |b~4|   |0|
        |b'5|   |0,0,1,0,1,0,0,1| |b~5|   |0|
        |b'6|   |1,0,0,1,0,1,0,0| |b~6|   |0|
        |b'7|   |0,1,0,0,1,0,1,0| |b~7|   |0|
"""
import time
import numpy as np


#aes_affine_transform関数
# FIPS197 SubByteのaffine変換をする関数
# 数式ベースのプログラム
def aes_affine_transform_matharray(Input_Byte):

    #affine変換のための行列の初期化
    matrix = np.array(
                    [[1,0,0,0,1,1,1,1]
                    ,[1,1,0,0,0,1,1,1]
                    ,[1,1,1,0,0,0,1,1]
                    ,[1,1,1,1,0,0,0,1]
                    ,[1,1,1,1,1,0,0,0]
                    ,[0,1,1,1,1,1,0,0]
                    ,[0,0,1,1,1,1,1,0]
                    ,[0,0,0,1,1,1,1,1]
                    ])
    
    #入力バイトをビット配列に変換
    #   向き注意
    #   [b'7 b'~6 ... b'0] → [b~0 b~1 ... b~7]とする。
    little_bits=np.array([(Input_Byte>>i) & 1 for i in range(8)])

    #affine変換を実行
    #   np.dotで行列演算(整数の行列演算のため、%2(剰余計算)で0、1に変換)
    #   行列演算後に0x63とXOR
    transformed_little_bits = np.dot(matrix,little_bits) %2 ^ [1,1,0,0,0,1,1,0]

    #ビット配列をバイトに変換
    #   ビット配列の向き注意（もとに戻す）
    #   [b~0 b~1 ... b~7] → [b'7 b'~6 ... b'0]
    Output_Byte = np.packbits(transformed_little_bits,bitorder='little').astype(np.uint8)[0]
    return Output_Byte

#Inv_aes_affine_transform関数
# FIPS197 SubByteの逆affine変換をする関数
# 数式ベースのプログラム
def Inv_aes_affine_transform_matharray(Input_Byte):

    #affine変換のための行列の初期化
    matrix = np.array(
                    [[0,0,1,0,0,1,0,1] 
                    ,[1,0,0,1,0,0,1,0]
                    ,[0,1,0,0,1,0,0,1]
                    ,[1,0,1,0,0,1,0,0]
                    ,[0,1,0,1,0,0,1,0]
                    ,[0,0,1,0,1,0,0,1]
                    ,[1,0,0,1,0,1,0,0]
                    ,[0,1,0,0,1,0,1,0]
                    ])

    #入力バイトをビット配列に変換
    #   向き注意
    #   [b'7 b'~6 ... b'0] → [b~0 b~1 ... b~7]とする。
    little_bits=np.array([(Input_Byte>>i) & 1 for i in range(8)])

    #affine変換を実行
    #   np.dotで行列演算(整数の行列演算のため、%2(剰余計算)で0、1に変換)
    #   行列演算後に0x63とXOR
    transformed_little_bits = np.dot(matrix,little_bits) %2 ^ [1,0,1,0,0,0,0,0]

    #ビット配列をバイトに変換
    #   ビット配列の向き注意（もとに戻す）
    #   [b~0 b~1 ... b~7] → [b'7 b'~6 ... b'0]
    Output_Byte = np.packbits(transformed_little_bits,bitorder='little').astype(np.uint8)[0]
    return Output_Byte


#aes_affine_transform関数
# FIPS197 SubByteのaffine変換をする関数
# hardベースのプログラム
# matharrayよりも高速
def aes_affine_transform_hardarray(Input_Byte):
    #入力バイトをビット配列に変換
    #   向き注意
    #   [b'7 b'~6 ... b'0] → [b~0 b~1 ... b~7]とする。
    little_bits=np.array([(Input_Byte>>i) & 1 for i in range(8)])

    #affine変換を実行
    #   行列演算を固定化
    #   行列演算後に0x63とXOR
    transformed_little_bits=[0]*8
    transformed_little_bits[0] = (little_bits[0] ^ little_bits[4] ^ little_bits[5] ^ little_bits[6] ^ little_bits[7]) ^ 1
    transformed_little_bits[1] = (little_bits[0] ^ little_bits[1] ^ little_bits[5] ^ little_bits[6] ^ little_bits[7]) ^ 1
    transformed_little_bits[2] = (little_bits[0] ^ little_bits[1] ^ little_bits[2] ^ little_bits[6] ^ little_bits[7])
    transformed_little_bits[3] = (little_bits[0] ^ little_bits[1] ^ little_bits[2] ^ little_bits[3] ^ little_bits[7])
    transformed_little_bits[4] = (little_bits[0] ^ little_bits[1] ^ little_bits[2] ^ little_bits[3] ^ little_bits[4])
    transformed_little_bits[5] = (little_bits[1] ^ little_bits[2] ^ little_bits[3] ^ little_bits[4] ^ little_bits[5]) ^ 1
    transformed_little_bits[6] = (little_bits[2] ^ little_bits[3] ^ little_bits[4] ^ little_bits[5] ^ little_bits[6]) ^ 1
    transformed_little_bits[7] = (little_bits[3] ^ little_bits[4] ^ little_bits[5] ^ little_bits[6] ^ little_bits[7])

    #ビット配列をバイトに変換
    #   ビット配列の向き注意（もとに戻す）
    #   [b~0 b~1 ... b~7] → [b'7 b'~6 ... b'0]
    Output_Byte = np.packbits(transformed_little_bits,bitorder='little').astype(np.uint8)[0]

    return Output_Byte

#Inv_aes_affine_transform関数
# FIPS197 SubByteのaffine変換をする関数
# hardベースのプログラム
# matharrayよりも高速

def Inv_aes_affine_transform_hardarray(Input_Byte):
    #入力バイトをビット配列に変換
    #   向き注意
    #   [b'7 b'~6 ... b'0] → [b~0 b~1 ... b~7]とする。
    little_bits=np.array([(Input_Byte>>i) & 1 for i in range(8)])

    #affine変換を実行
    #   行列演算を固定化
    #   行列演算後に0x05とXOR
    transformed_little_bits=[0]*8
    transformed_little_bits[0] = (little_bits[2] ^ little_bits[5] ^ little_bits[7]) ^ 1
    transformed_little_bits[1] = (little_bits[0] ^ little_bits[3] ^ little_bits[6])
    transformed_little_bits[2] = (little_bits[1] ^ little_bits[4] ^ little_bits[7]) ^ 1
    transformed_little_bits[3] = (little_bits[0] ^ little_bits[2] ^ little_bits[5])
    transformed_little_bits[4] = (little_bits[1] ^ little_bits[3] ^ little_bits[6])
    transformed_little_bits[5] = (little_bits[2] ^ little_bits[4] ^ little_bits[7])
    transformed_little_bits[6] = (little_bits[0] ^ little_bits[3] ^ little_bits[5])
    transformed_little_bits[7] = (little_bits[1] ^ little_bits[4] ^ little_bits[6])

    #ビット配列をバイトに変換
    #   ビット配列の向き注意（もとに戻す）
    #   [b~0 b~1 ... b~7] → [b'7 b'~6 ... b'0]
    Output_Byte = np.packbits(transformed_little_bits,bitorder='little').astype(np.uint8)[0]

    return Output_Byte

# スクリプトが直接実行された場合にのみ実行されるコード
if __name__ == '__main__':
    # ここから必要な処理を記述する
    byte_array = bytes([0x3A, 0x2B, 0x1C,0x00])
    """
    for i in range(len(byte_array)):
        output = aes_affine_transform_matharray(byte_array[i])
        print(i," : ",hex(output))
        output2 = Inv_aes_affine_transform_matharray(output)
        print(i," : ",hex(output2))
    """

    for i in range(len(byte_array)):
        output = aes_affine_transform_hardarray(byte_array[i])
        print(i," : ",hex(output))
        output2 = Inv_aes_affine_transform_hardarray(output)
        print(i," : ",hex(output2))

"""
    start_time = time.time()
    for _ in range(1000000):
        output = hex(aes_affine_transform_matharray(byte_array[0]))
    end_time = time.time()
    print("Method math:", output, "Time:", end_time - start_time)

    start_time = time.time()
    for _ in range(1000000):
        output = hex(aes_affine_transform_hardarray(byte_array[0]))
    end_time = time.time()
    print("Method hard:", output, "Time:", end_time - start_time)
"""



    