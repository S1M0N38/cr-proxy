from cr.protocol import CrProtocol
from cr.client.crypto import CrClientCrypto


class CrClientProtocol(CrClientCrypto, CrProtocol):

    def __init__(self, factory):
        super(CrClientProtocol, self).__init__(factory)
        self.factory.server.client = self
        self.server = self.factory.server
        self.decoder = self.server.decoder
        self.encoder = self.server.encoder

    def connectionMade(self):
        super(CrClientProtocol, self).connectionMade()
        print('connected to {}:{} ...'.format(self.peer.host, self.peer.port))

    def packetDecrypted(self, messageid, version, payload):
        self.decodePacket(messageid, version, payload)
        self.server.sendPacket(messageid, version, payload)

    def connectionLost(self, reason):
        print('connection to {}:{} closed ...'
              .format(self.peer.host, self.peer.port))
        self.server.transport.loseConnection()
