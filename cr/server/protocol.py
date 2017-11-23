from twisted.internet import reactor
from cr.protocol import CrProtocol
from cr.server.crypto import CrServerCrypto
from cr.client.factory import CrClientFactory


class CrServerProtocol(CrServerCrypto, CrProtocol):

    client = None

    def __init__(self, factory):
        super(CrServerProtocol, self).__init__(factory)
        self.factory.server = self
        self.decoder = self.factory.decoder
        self.encoder = self.factory.encoder

    def connectionMade(self):
        super(CrServerProtocol, self).connectionMade()
        print('connection from {}:{} ...'
              .format(self.peer.host, self.peer.port))
        self.factory.client_endpoint.connect(CrClientFactory(self))

    def packetDecrypted(self, messageid, version, payload):
        if not self.client:
            reactor.callLater(0.25, self.packetDecrypted,
                              messageid, version, payload)
            return
        self.decodePacket(messageid, version, payload)
        self.client.sendPacket(messageid, version, payload)

    def connectionLost(self, reason):
        print('connection from {}:{} closed ...'
              .format(self.peer.host, self.peer.port))
        if self.client:
            self.client.transport.loseConnection()
