import os
import sys
import varint
import pandas as pd

csv_path = os.path.join(
    os.path.dirname(
        os.path.realpath(__file__)), 'cr-csv', 'assets', 'csv_logic')
scid_to_csv = {
    '5': 'resources.csv',           # Resources
    '16': 'alliance_badges.csv',    # Badge
    # '19': '',                     # 'Chest Type',
    '26': 'spells_characters.csv',  # Troops
    '27': 'spells_buildings.csv',   # Buildings
    '28': 'spells_other.csv',       # Spells
    '54': 'arenas.csv',             # Arena
    '57': 'regions.csv',            # Region
    '60': 'achievements.csv',       # Achievements
    # '65': '',                     # 'Challenge',
    '72': 'game_modes.csv',         # Game Mode
    '83': 'skins.csv'               # King Skin
    }


def hex_to_dec(hex_str):
    hi_hex = hex_str[:2]
    lo_hex = hex_str[2:]
    _, _, hi_dec = varint.hexToDecimal(hi_hex)
    _, _, lo_dec = varint.hexToDecimal(lo_hex)
    return str(hi_dec), str(lo_dec)


def dec_to_scid(hi, lo):
    csv_name = scid_to_csv[hi]
    file_path = os.path.join(csv_path, csv_name)
    df = pd.read_csv(file_path)
    scid_row = df.ix[int(lo) + 1]
    return csv_name, scid_row


def print_help():
    print('''
    scid.py <0xhex_str> (e.g. 0x1a00)
        Outputs
            Hi_Dec  |  Lo_Dec  |  long_Dec  |
            csv_name
            scid_info

    scid.py <Hi_Dec> <Lo_Dec> (not RRSINT32)
        Outputs:
            Hi_Dec  |  Lo_Dec  |  long_Dec  |
            csv_name
            scid_info
    ''')


def main():
    if len(sys.argv) < 2:
        print_help()
        exit()

    else:
        if len(sys.argv) == 2 and sys.argv[1].startswith('0x'):
            hi, lo = hex_to_dec(sys.argv[1][2:])
        elif len(sys.argv) == 3:
            hi, lo = sys.argv[1], sys.argv[2]
        else:
            print('Input Error'), sys.exit()
        long_ = int(hi) * 1000000 + int(lo)
        csv_name, scid_row = dec_to_scid(hi, lo)
        print('File: '.format(csv_name))
        print('Hi_Dec = {}  |  Lo_Dec = {}  |  Long_Dec = {}'
              .format(hi, lo, long_))
        print(scid_row.head())


if __name__ == '__main__':
    main()
