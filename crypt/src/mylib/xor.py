
input_data = bytearray()
for i in range(500):
    tmp = i % 256
    by = tmp.to_bytes(1,byteorder='big')
    input_data.extend(by)


# 入力データを64バイトごとに分割し、0xFFとXOR演算を行う
output_data = bytearray()
for i in range(0, len(input_data), 64):
    block = input_data[i:i+64]
    print(f"input : {block.hex()}")
    xor_result = bytes(byte ^ 0xFF for byte in block)
    output_data.extend(xor_result)

# 結果を表示
for i in range(0, len(output_data), 64):
    block = output_data[i:i+64]
    print(f"output : {block.hex()}")




