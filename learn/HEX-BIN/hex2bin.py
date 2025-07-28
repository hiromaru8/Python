import time
import numpy as np

# リトルエンディアンの2進数変換
def convert_to_binary_le1(Input_Byte):
    bits = np.array([int(bit) for bit in bin(Input_Byte)[2:].zfill(8)][::-1])
    return bits

#le1より早い
def convert_to_binary_le2(Input_Byte):
    bits = np.array([(Input_Byte>>i) & 1 for i in range(8)])
    return bits

# 処理速度計測
input_byte = 0xAB  # 変換する16進数値

start_time = time.time()
for _ in range(1000000):
    bits1 = convert_to_binary_le1(input_byte)
end_time = time.time()
print("Method 1:", bits1, "Time:", end_time - start_time)

start_time = time.time()
for _ in range(1000000):
    bits2 = convert_to_binary_le2(input_byte)
end_time = time.time()
print("Method 2:", bits2, "Time:", end_time - start_time)
