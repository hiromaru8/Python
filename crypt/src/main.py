# 1バイトのデータを表す整数を作成します（例として）
byte_value = 0b11011010  # 2進数表記

# ビットの順序を逆にします
reversed_byte_value = int(format(byte_value, '08b')[::-1], 2)

# 逆順にした1バイトデータを表示します
print(bin(reversed_byte_value))
print(int(format(byte_value, '08b')[::-1], 2))
