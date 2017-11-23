import os


class Replay:

    @staticmethod
    def filepath_by_messageid(messageid):
        replay_directory = os.path.join(os.path.dirname(os.path.dirname(
            os.path.realpath(__file__))), 'replay')
        return os.path.join(replay_directory, str(messageid) + '.bin')

    @staticmethod
    def save(messageid, version, payload):
        with open(Replay.filepath_by_messageid(messageid), 'wb') as f:
            f.write(messageid.to_bytes(2, byteorder='big'))
            f.write(len(payload).to_bytes(3, byteorder='big'))
            f.write(version.to_bytes(2, byteorder='big'))
            f.write(payload)

    @staticmethod
    def read(self, messageid):
        with open(Replay.filepath_by_messageid(messageid), 'rb') as f:
            message = f.read()
        return message
