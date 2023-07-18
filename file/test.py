from dataclasses import dataclass

@dataclass
class Person:
    id: int
    name: str
    age: int
    data: str


person = Person(90, "John", 30, "Data")
print(person.id)   # 1
print(person.name)  # "John"
print(person.age)   # 30
print(person.data)  # "Data"




import struct

struct_format = ">i8si64s"
"""
>:ビッグエンディアン
i   :int
8s  :8バイト文字列
i   :int
64s :64バイト
"""
data=(person.id,person.name.encode(),person.age,person.data.encode())
packed_data = struct.pack(struct_format, *data)
print(packed_data.hex())



with open('d:/Learnning/Python/file/ファイル名.dat', 'wb') as file:
    file.write(packed_data)


    
