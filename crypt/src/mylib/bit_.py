from bitarray import bitarray

year=2023   #5bit
year_1 = year &  0xf
month=12  #4bit
day=4     #5bit
h = 23    #5bit
m = 59    #6bit
s = 59    #6bit
mil = 999 #10
mic = 999 #10
nano =99  #7
print(hex((year_1 << 4)|month))



bits_sync = bitarray()  # 20 bytesに対応するbitarrayを作成
bits_tmp  =  bitarray()
bits_sync.frombytes(year_1.to_bytes(20,byteorder='big'))
bits_sync = bits_sync << 4
bits_tmp.frombytes(month.to_bytes(20,byteorder='big'))






print(bits_sync)
print((bits_sync[0:16]))



# bitarrayをbytesに変換
sync_bytes = bits_sync.tobytes()
print([hex(i) for i in sync_bytes])
