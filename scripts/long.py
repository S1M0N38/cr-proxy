import sys
import varint
import math


def long2HiLo(long_int):
    return long_int % 256,  (long_int - long_int % 256) >> 8


def HiLo2long(Hi, Lo):
    return (Lo << 8) + Hi


def long2tag(long_):
    tag_char = list('0289PYLQGRJCUV')
    tag = []
    while long_ > 0:
        c_index = math.floor(long_ % len(tag_char))
        tag.insert(0, tag_char[c_index])
        long_ = (long_ - c_index) / len(tag_char)
    return ''.join(tag)


def HiLo2tag(Hi, Lo):
    long2tag(HiLo2long(Hi, Lo))


def tag2long(tag):
    tag_char = list('0289PYLQGRJCUV')
    tag_array = list(tag.upper())
    long_ = 0
    for i, c in enumerate(tag_array):
        try:
            c_index = tag_char.index(c)
        except ValueError:
            print('Wrong Hashtag'), sys.exit()
        long_ = (long_ * 14) + c_index
    return long_


def tag2HiLo(tag):
    long_ = tag2long(tag)
    return long2HiLo(long_)


def print_help():
    print('''
    long.py <long_Dec>
        Outputs:
            long_Dec  |  Hi_Dec  |  Lo_Dec  |  Tag
            long_Dec  |  Hi_Hex  |  Lo_Hex  |  Tag

    long.py <Hi_Dec> <Lo_Dec> (or <0xHi_Hex>, <0xLo_Hex>)
        Outputs:
            Hi_Dec  |  Lo_Dec  |  long_Dec  |  Tag

    long.py <@TAG>
        Outputs:
            #TAG  |  Hi_Dec  |  Lo_Dec
            #TAG  |  long_Dec
    ''')


def main():
    if len(sys.argv) < 2:
        print(sys.argv)
        print_help()
        exit()

    elif len(sys.argv) == 2 and sys.argv[1].startswith('@'):
        Tag = sys.argv[1][1:]
        Hi_Dec, Lo_Dec = tag2HiLo(Tag)
        Long_Dec = tag2long(Tag)
        print('Tag = {}  |  Hi_Dec = {}  |  Lo_Dec = {}'
              .format(Tag, Hi_Dec, Lo_Dec))
        print('Tag = {}  |  Long_Dec = {}'
              .format(Tag, Long_Dec))

    elif len(sys.argv) == 2:
        Long_Dec = int(sys.argv[1])
        Hi_Dec, Lo_Dec = long2HiLo(Long_Dec)
        Hi_Hex, _, _ = varint.decimalToHex(Hi_Dec)
        Lo_Hex, _, _ = varint.decimalToHex(Lo_Dec)
        Tag = long2tag(Long_Dec)
        print('Long_Dec = {}  |  Hi_Dec = {}  |  Lo_Dec = {}  |  Tag = {}'
              .format(Long_Dec, Hi_Dec, Lo_Dec, Tag))
        print('Long_Dec = {}  |  Hi_Hex = {}  |  Lo_Hex = {}  |  Tag = {}'
              .format(Long_Dec, Hi_Hex, Lo_Hex, Tag))

    elif len(sys.argv) == 3:
        Hi_Dec, Lo_Dec = int(sys.argv[1]), int(sys.argv[2])
        if (sys.argv[1].startswith("0x")):
            Hi_Dec, _, _ = varint.hexToDecimal(Hi_Dec)
        if (sys.argv[2].startswith("0x")):
            Lo_Dec, _, _ = varint.hexToDecimal(Lo_Dec)
        Long_Dec = HiLo2long(Hi_Dec, Lo_Dec)
        Tag = long2tag(Long_Dec)
        print('Hi_Dec = {}  |  Lo_Dec = {}  |  Long_Dec = {}  |  Tag = {}'
              .format(Hi_Dec, Lo_Dec, Long_Dec, Tag))


if __name__ == "__main__":
    main()
