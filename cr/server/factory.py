from twisted.internet.protocol import Factory
from cr.server.protocol import CrServerProtocol
from cr.message.encoder import CrMessageEncoder
from cr.message.decoder import CrMessageDecoder


class CrServerFactory(Factory):
    def __init__(self, client_endpoint):
        self.client_endpoint = client_endpoint
        self.encoder = CrMessageEncoder()
        self.decoder = CrMessageDecoder()

    def buildProtocol(self, endpoint):
        return CrServerProtocol(self)
