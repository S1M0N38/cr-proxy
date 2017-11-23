import sys
from cr.message.decoder import CrMessageDecoder
from cr.replay import Replay


if __name__ == "__main__":
    messageid = sys.argv[1]
    filepath = Replay.filepath_by_messageid(messageid)

    print('found message: '.format(filepath))

    decoder = CrMessageDecoder()
    decoded = decoder.decodeFile(filepath)
    decoder.dump(decoded)
