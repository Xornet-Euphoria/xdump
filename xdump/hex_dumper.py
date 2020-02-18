from hex_data import HexData


class HexDumper:
    def __init__(self, data, byte_num=4, base_addr=0, endian="little"):
        self.__raw_data = data
        self.__byte_num = byte_num
        self.__base_addr = base_addr
        self.__endian = endian
        self.__data = self.__process_data()
        self.__unpackable = self.__byte_num == 4 or self.__byte_num == 8  # 8bit, 16bitに対応するかもしれない


    def __get_hd_by_addr(self, addr):
        current_index = (addr - self.__base_addr) // self.__byte_num
        return self.__data[current_index]


    def get_prev_hd(self, hd):
        prev_addr = hd.addr - self.__base_addr - self.__byte_num
        return __get_hd_by_addr(prev_addr)


    def get_next_hd(self, hd):
        next_addr = hd.addr - self.__base_addr + self.__byte_num


    def __process_data(self):
        ret_data = []
        offset = 0
        while offset < len(self.__raw_data):
            if offset + self.__byte_num < len(self.__raw_data):
                word = self.__raw_data[offset:offset+self.__byte_num]
            else:
                # todo: endian
                word = self.__raw_data[offset:]
                while len(word) < self.__byte_num:
                    word += b"\x00"

            hd = HexData(word, self.__base_addr + offset)
            ret_data.append(hd)
            offset += self.__byte_num

        return ret_data


    def __get_max_addr(self):
        if self.__data == []:
            return None

        return self.__base_addr + (len(self.__data) - 1) * self.__byte_num


    def __get_addr(self, hd_index):
        return self.__base_addr + hd_index * self.__byte_num


    # simple dump

    def dump(self, fmt=None):
        if not self.__unpackable:
            self.raw_dump()
            return

        if fmt is None:
            max_addr = self.__get_max_addr()
            max_byte_length = max_addr.bit_length() // 4 + 1

            fmt = f"{{:{max_byte_length}x}}: {{}} -> {{:x}}"

        for i, hd in enumerate(self.__data):
            addr = self.__get_addr(i)
            print(fmt.format(addr, hd.dump_string, hd.value))


    def raw_dump(self, fmt=None):
        if fmt is None:
            max_addr = self.__get_max_addr()
            max_byte_length = max_addr.bit_length() // 4 + 1

            fmt = f"{{:{max_byte_length}x}}: {{}}"

        for i, hd in enumerate(self.__data):
            addr = self.__get_addr(i)
            print(fmt.format(addr, hd.dump_string))


    def string_dump(self, non_char=".", fmt=None):
        if fmt is None:
            max_addr = self.__get_max_addr()
            max_byte_length = max_addr.bit_length() // 4 + 1

            fmt = f"{{:{max_byte_length}x}}: {{}} | {{}}"

        for i, hd in enumerate(self.__data):
            s = ""
            for c in hd.raw_data:
                if c > 0x1f and c < 0x7f:
                    s += chr(c)
                else:
                    s += non_char

            addr = self.__get_addr(i)
            print(fmt.format(addr, hd.dump_string, s))
