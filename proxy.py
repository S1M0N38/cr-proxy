from twisted.internet import reactor
from cr.server.factory import CrServerFactory
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet.endpoints import TCP4ClientEndpoint

# Client
server = 'game.clashroyaleapp.com'
port = 9339

# Server
interface = '0.0.0.0'
port = 9339

if __name__ == "__main__":
    client_endpoint = TCP4ClientEndpoint(reactor, server, port)
    server_endpoint = TCP4ServerEndpoint(reactor, port, interface=interface)
    server_endpoint.listen(CrServerFactory(client_endpoint))

    print("listening on {}:{} ...".format(interface, port))

    reactor.run()
