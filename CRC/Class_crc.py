class CRC:
    def __init__(self, polynomial):
        self.polynomial = polynomial
        self.table = self.generate_crc_table()

    def generate_crc_table(self):
        table = []
        for i in range(256):
            crc = i
            for _ in range(8):
                if crc & 1:
                    crc = (crc >> 1) ^ self.polynomial
                else:
                    crc >>= 1
            table.append(crc)
        return table

    def calculate_crc(self, data):
        crc = self.initial_value
        for byte in data:
            crc = (crc >> 8) ^ self.table[(crc & 0xFF) ^ byte]
        return crc ^ self.final_xor_value


class CRC32(CRC):
    def __init__(self):
        super().__init__(0xEDB88320)
        self.initial_value = 0xFFFFFFFF
        self.final_xor_value = 0xFFFFFFFF

    def calculate(self, data):
        return self.calculate_crc(data)


class CRC32C(CRC):
    def __init__(self):
        super().__init__(0x82F63B78)
        self.initial_value = 0xFFFFFFFF
        self.final_xor_value = 0xFFFFFFFF

    def calculate(self, data):
        return self.calculate_crc(data)


class CRC32K(CRC):
    def __init__(self):
        super().__init__(0xEB31D82E)
        self.initial_value = 0xFFFFFFFF
        self.final_xor_value = 0xFFFFFFFF

    def calculate(self, data):
        return self.calculate_crc(data)


# 使用例:

data = b'Hello, world!'
print(data,":",data.hex())
crc32 = CRC32()
crc32_result = crc32.calculate(data)
print(f"CRC-32: {hex(crc32_result)}")

crc32c = CRC32C()
crc32c_result = crc32c.calculate(data)
print(f"CRC-32C: {hex(crc32c_result)}")

crc32k = CRC32K()
crc32k_result = crc32k.calculate(data)
print(f"CRC-32K: {hex(crc32k_result)}")
