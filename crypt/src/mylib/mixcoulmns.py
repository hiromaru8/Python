

class mixcolumns:

    def __init__(self):
        self.__sparam_matrix=[
        [0x2, 0x3, 0x1, 0x1],
        [0x1, 0x2, 0x3, 0x1],
        [0x1, 0x1, 0x2, 0x3],
        [0x3, 0x1, 0x1, 0x2]
    ]

    def xtime(self,b:int):
        result = (b << 1) ^ (0x1b if (b & 0x80) else 0x00)
        return result & 0xff  # 8ビットでクリッピング

    def dot(self,x, y):
        mask = 0x01
        product = 0

        for _ in range(8):  # 8ビット分のループ
            if y & mask:
                product ^= x
            x = self.xtime(x)
            mask <<= 1

        return product

    def mix_columns(self,s):
        result_matrix = [[0 for _ in range(4)] for _ in range(4)]

        for c in range(4):
            result_matrix[0][c] =   self.dot(self.__sparam_matrix[0][0], s[0][c]) ^\
                                    self.dot(self.__sparam_matrix[0][1], s[1][c]) ^\
                                    self.dot(self.__sparam_matrix[0][2], s[2][c]) ^\
                                    self.dot(self.__sparam_matrix[0][3], s[3][c])
            result_matrix[1][c] =   self.dot(self.__sparam_matrix[1][0], s[0][c]) ^\
                                    self.dot(self.__sparam_matrix[1][1], s[1][c]) ^\
                                    self.dot(self.__sparam_matrix[1][2], s[2][c]) ^\
                                    self.dot(self.__sparam_matrix[1][3], s[3][c])
            result_matrix[2][c] =   self.dot(self.__sparam_matrix[2][0], s[0][c]) ^\
                                    self.dot(self.__sparam_matrix[2][1], s[1][c]) ^\
                                    self.dot(self.__sparam_matrix[2][2], s[2][c]) ^\
                                    self.dot(self.__sparam_matrix[2][3], s[3][c])
            result_matrix[3][c] =   self.dot(self.__sparam_matrix[3][0], s[0][c]) ^\
                                    self.dot(self.__sparam_matrix[3][1], s[1][c]) ^\
                                    self.dot(self.__sparam_matrix[3][2], s[2][c]) ^\
                                    self.dot(self.__sparam_matrix[3][3], s[3][c])
        return result_matrix
    

if __name__ == "__main__":

    culc=mixcolumns()
    # a=0x57

    # for i in range(8):
    #     a = culc.xtime(a)
    #     print(hex(a))

    # テスト
    state_matrix = [
        [0x32, 0x88, 0x31, 0xe0],
        [0x43, 0x5a, 0x31, 0x37],
        [0xf6, 0x30, 0x98, 0x07],
        [0xa8, 0x8d, 0xa2, 0x34]
    ]

    result_matrix = culc.mix_columns(state_matrix)

    # 結果を表示
    for row in result_matrix:
        print([hex(element) for element in row])


    v=bytearray(256)

    for i in range(len(v)):
        v[i]=i


    print(    v[1]+v[2])

