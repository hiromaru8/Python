def shift_rows_1(state):
    # 1次元リストを4x4の行列に変換
    matrix_state = [[state[i],state[i+4],state[i+8],state[i+12]] for i in range(0, 4)]
    for row in matrix_state:
        print([hex(i) for i in row])   
        
    # 各行に対してShiftRows変換を適用
    for i in range(4):
        matrix_state[i] = matrix_state[i][i:] + matrix_state[i][:i]

    # 4x4の行列を1次元リストに戻す
    flattened_state = [element for row in matrix_state for element in row]
    
    return flattened_state


def shift_rows_2(state:bytes):
    state_out=bytearray(16)
    state_out[0:4]   = [state[0]  , state[5]  , state[10]  , state[15] ]#col 1
    state_out[4:8]   = [state[4]  , state[9]  , state[14]  , state[3] ] #col 2
    state_out[8:12]  = [state[8]  , state[13] , state[2]   , state[7] ] #col 3
    state_out[12:16] = [state[12] , state[1]  , state[6]   , state[11] ]#col 4
    return state_out

if __name__ == "__main__":
    # 例として、4x4のState行列を1次元リストで作成
    state_array = [0x32, 0x88, 0x31, 0xe0, 0x43, 0x5a, 0x31, 0x37, 0xf6, 0x30, 0x98, 0x07, 0xa8, 0x8d, 0xa2, 0x34]

    print([ hex(i) for i in state_array[1:5][1:]])

    # ShiftRows操作を適用
    shifted_state = shift_rows_2(state_array)

    # 結果を表示
    print([ hex(i) for i in shifted_state])
    print(type(shifted_state))


    # # 1次元のリストを作成
    # state = [
    #     0x32, 0x88, 0x31, 0xe0,
    #     0x43, 0x5a, 0x31, 0x37, 
    #     0xf6, 0x30, 0x98, 0x07, 
    #     0xa8, 0x8d, 0xa2, 0x34
    #     ]

    # # ShiftRows変換を適用
    # shifted_state = shift_rows(state)

    # print(range(len(state)))

    # print([hex(state[i]) for i in range(16)])
    # # 結果の表示
    # print([hex(shifted_state[i]) for i in range(16)])
