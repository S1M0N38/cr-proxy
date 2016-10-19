from coc.protocol import CoCProtocol
from coc.client.crypto import CoCClientCrypto


class CoCClientProtocol(CoCClientCrypto, CoCProtocol):

    def __init__(self, factory):
        super(CoCClientProtocol, self).__init__(factory)
        self.factory.server.client = self
        self.server = self.factory.server
        self.decoder = self.server.decoder
        self.encoder = self.server.encoder

    def connectionMade(self):
        super(CoCClientProtocol, self).connectionMade()
        print("connected to {}:{} ...".format(self.peer.host, self.peer.port))

    def packetDecrypted(self, messageid, version, payload):
        self.decodePacket(messageid, version, payload)
        self.server.sendPacket(messageid, version, payload)

    def connectionLost(self, reason):
        print("connection to {}:{} closed ...".format(self.peer.host, self.peer.port))
        self.server.transport.loseConnection()
