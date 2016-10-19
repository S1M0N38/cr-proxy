from twisted.internet import protocol
import traceback
import os
from coc.hexdump import hexdump
from coc.proxyconfig import ProxyConfig
from coc.replay import Replay

class CoCPacketReceiver(protocol.Protocol):

    _buffer = b""
    _packet = b""

    def dataReceived(self, data):
        self._buffer += data
        while self._buffer:
            if self._packet:
                payload_length = int.from_bytes(self._packet[2:5], byteorder="big")
                if len(self._buffer) >= payload_length:
                    self._packet += self._buffer[:payload_length]
                    self.packetReceived(self._packet)
                    self._packet = b""
                    self._buffer = self._buffer[payload_length:]
                else:
                    break
            elif len(self._buffer) >= 7:
                self._packet = self._buffer[:7]
                self._buffer = self._buffer[7:]

    def packetReceived(self, packet):
        raise NotImplementedError


class CoCProtocol(CoCPacketReceiver):

    _peer = None
    factory = None
    server = None
    client = None

    def __init__(self, factory):
        self._factory = factory

    @property
    def factory(self):
        return self._factory

    @property
    def peer(self):
        return self._peer

    def connectionMade(self):
        self._peer = self.transport.getPeer()

    def packetReceived(self, packet):
        decrypted = self.decryptPacket(packet)
        if decrypted:
            Replay.save(*decrypted)
            self.packetDecrypted(*decrypted)

    def decodePacket(self, messageid, version, payload):
        try:
            decoded = self.decoder.decode(messageid, version, payload)
            if messageid==24114:
                print(hexdump(messageid.to_bytes(2, byteorder="big") + len(payload).to_bytes(3, byteorder="big") + version.to_bytes(2, byteorder="big") + payload))
                
        except (KeyError, IndexError, NotImplementedError) as e:
            print(messageid, "Error:", e)
            print(messageid, "payload length: {} version: {}".format(len(payload), version))
            print(hexdump(messageid.to_bytes(2, byteorder="big") + len(payload).to_bytes(3, byteorder="big") + version.to_bytes(2, byteorder="big") + payload))
        else:
            self.decoder.dump(decoded)

    def decryptPacket(self, packet):
        raise NotImplementedError

    def packetDecrypted(self, messageid, version, payload):
        raise NotImplementedError

    def sendPacket(self, messageid, unknown, payload):
        encrypted = self.encryptPacket(messageid, unknown, payload)
        if encrypted:
            (messageid, unknown, payload) = encrypted
            packet = (messageid.to_bytes(2, byteorder="big") + len(payload).to_bytes(3, byteorder="big") + unknown.to_bytes(2, byteorder="big") + payload)
            self.transport.write(packet)

    def encryptPacket(self, messageid, unknown, payload):
        raise NotImplementedError
