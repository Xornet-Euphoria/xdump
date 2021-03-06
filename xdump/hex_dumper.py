from xdump.hex_data import HexData


class HexDumper:
    def __init__(self, data, byte_num=4, base_addr=0, endian="little"):
        self.__raw_data = data
        self.__byte_num = byte_num
        self.__base_addr = base_addr
        self.__endian = endian
        self.__data = self.__process_data()
        self.__unpackable = self.__byte_num == 4 or self.__byte_num == 8  # 8bit, 16bitに対応するかもしれない


    @property
    def data(self):
        return self.__data


    def __get_hd_by_addr(self, addr):
        current_index = (addr - self.__base_addr) // self.__byte_num
        return self.__data[current_index]


    def get_prev_hd(self, hd):
        prev_addr = hd.addr - self.__base_addr - self.__byte_num
        return self.__get_hd_by_addr(prev_addr)


    def get_next_hd(self, hd):
        next_addr = hd.addr - self.__base_addr + self.__byte_num
        return self.__get_hd_by_addr(next_addr)


    def set_hd_desc_by_function(self, f):
        for hd in self.__data:
            hd.desc = f(hd.raw_data)


    def set_hd_desc_by_list(self, l):
        max_index = len(self.__data)

        for idx, item in enumerate(l):
            if idx < max_index:
                self.__data[idx].desc = item
            else:
                break


    def __process_data(self):
        ret_data = []
        offset = 0
        while offset < len(self.__raw_data):
            if offset + self.__byte_num < len(self.__raw_data):
                word = self.__raw_data[offset:offset+self.__byte_num]
            else:
                word = self.__raw_data[offset:]
                padding = (self.__byte_num - len(word))
                if self.__endian == "little":
                    word += b"\x00" * padding
                else:
                    word = b"\x00" * padding + word

            hd = HexData(word, self.__base_addr + offset, endian=self.__endian)
            ret_data.append(hd)
            offset += self.__byte_num

        return ret_data


# ========== dump functions ==========

    def __get_max_addr(self):
        if self.__data == []:
            return None

        return self.__base_addr + (len(self.__data) - 1) * self.__byte_num


    def __get_addr(self, hd_index):
        return self.__base_addr + hd_index * self.__byte_num


    def dump(self, fmt=None):
        if not self.__unpackable:
            self.raw_dump()
            return

        if fmt is None:
            max_addr = self.__get_max_addr()
            max_byte_length = max_addr.bit_length() // 4 + 1

            not_desc_fmt = f"{{:{max_byte_length}x}}: {{}} -> {{:x}}"
            desc_fmt = f"{{:{max_byte_length}x}}: {{}} -> {{:{self.__byte_num * 2}x}} | {{}}"

        for i, hd in enumerate(self.__data):
            fmt = not_desc_fmt if hd.desc is None else desc_fmt
            addr = self.__get_addr(i)
            print(fmt.format(addr, hd.dump_string, hd.value, hd.desc))


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
