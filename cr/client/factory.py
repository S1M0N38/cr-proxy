from twisted.internet.protocol import ClientFactory
from cr.client.protocol import CrClientProtocol


class CrClientFactory(ClientFactory):

    def __init__(self, server):
        self.server = server

    def buildProtocol(self, addr):
        return CrClientProtocol(self)
