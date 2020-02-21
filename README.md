# xdump

## description

俺式hexdump

## Install

```bash
python setup.py install
```

## 機能

### 実装済み

- 表示単位を指定可能
- 32bitと64bitのエンディアン指定によるunpack
- 印字可能文字列を表示
- 表示単位毎に説明を加える

## Usage

### In Script

```python
>>> from xdump import *
>>> example_bin = b"\xef\xbe\xad\xde\xbe\xba\xfe\xca"
>>> dumper = HexDumper(example_bin)
>>> dumper.dump()
0: ef be ad de -> deadbeef
4: be ba fe ca -> cafebabe
>>> dumper = HexDumper(example_bin, 8)  # 64bit
>>> dumper.dump()
0: ef be ad de be ba fe ca -> cafebabedeadbeef
>>> dumper.raw_dump()  # dump without unpacking
0: ef be ad de be ba fe ca
>>> example_bin_big = b"\xde\xad\xbe\xef\xca\xfe\xba\xbe"
>>> dumper = HexDumper(example_bin_big, 4, endian="big")  # big endian
>>> dumper.dump()
0: de ad be ef -> deadbeef
4: ca fe ba be -> cafebabe
>>> dumper = HexDumper(example_bin, base_addr=0x1000)  # setting base address
>>> dumper.dump()
1000: ef be ad de -> deadbeef
1004: be ba fe ca -> cafebabe
>>> example_str = b"aaaabbbbccccdddd"
>>> dumper = HexDumper(example_str, 16)
>>> dumper.string_dump()  # simple `strings` command
0: 61 61 61 61 62 62 62 62 63 63 63 63 64 64 64 64 | aaaabbbbccccdddd
>>> example_str_junk = b"\xef\xbe\xad\xdeaaaaqwerasdf"  # with bad chars
>>> dumper = HexDumper(example_str_junk, 16)
>>> dumper.string_dump()  # bad chars displayed as dot (default)
0: ef be ad de 61 61 61 61 71 77 65 72 61 73 64 66 | ....aaaaqwerasdf
>>> dumper.string_dump("?")  # you can specify come chars instead of dot
0: ef be ad de 61 61 61 61 71 77 65 72 61 73 64 66 | ????aaaaqwerasdf
```

## Todo

- コマンドラインツールとして使えるスクリプトを同梱する
- 使い方を書く
