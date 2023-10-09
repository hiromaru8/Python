def shift_rows(state):
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

# 1次元のリストを作成
state = [
    0x32, 0x88, 0x31, 0xe0,
    0x43, 0x5a, 0x31, 0x37, 
    0xf6, 0x30, 0x98, 0x07, 
    0xa8, 0x8d, 0xa2, 0x34
    ]

# ShiftRows変換を適用
shifted_state = shift_rows(state)

print(range(len(state)))

print([hex(state[i]) for i in range(16)])
# 結果の表示
print([hex(shifted_state[i]) for i in range(16)])
