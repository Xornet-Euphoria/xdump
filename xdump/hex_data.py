from xdump.util import upk


class HexData:
    def __init__(self, data, addr, endian="little"):
        self.__raw_data = data
        self.__addr = addr  # 廃止予定
        self.__byte_num = len(data)
        self.__unpackable = self.__byte_num == 4 or self.__byte_num == 8  # 8bit, 16bitに対応するかもしれない
        self.__dump_string = self.__make_dump_string()
        self.__value = self.__unpack(endian) if self.__unpackable else None
        self.desc = None  # extended property


    @property
    def raw_data(self):
        return self.__raw_data


    @property
    def addr(self):
        return self.addr


    @property
    def dump_string(self):
        return self.__dump_string


    @property
    def value(self):
        return self.__value


    def __make_dump_string(self):
        dumped = ""
        for c in self.__raw_data:
            if c < 16:
                dumped += "0"
            dumped += hex(c)[2:]

            dumped += " "

        dumped = dumped[:-1]
        return dumped


    def __unpack(self, endian):
        return upk(self.__raw_data, endian=endian)
