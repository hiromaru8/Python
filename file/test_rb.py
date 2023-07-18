
import struct


with open('d:/Learnning/Python/file/ファイル名.dat', 'rb') as file:
    binary_data = file.read()



struct_format = ">i8si64s"
"""
>:ビッグエンディアン
i   :int
8s  :8バイト文字列
i   :int
64s :64バイト
"""

print(binary_data.hex())

unpacked_data = struct.unpack(struct_format, binary_data)


for i in range(len(unpacked_data)):
    print(unpacked_data[i])


print(unpacked_data[1].decode('utf-8'))
print(unpacked_data[3].decode('utf-8'))









