# -*- coding: utf-8 -*-

from twisted.internet import defer, reactor
from twisted.internet.protocol import ReconnectingClientFactory
from autobahn.twisted.websocket import protocol, WebSocketClientProtocol, WebSocketClientFactory


class SockJSClientProtocol(WebSocketClientProtocol):

    def onConnect(self, response):
        self.factory.client.onConnect(self, response)

    def onOpen(self):
        self.factory.client.onOpen()

    def onClose(self, wasClean, code, reason):
        self.factory.client.onClose(wasClean, code, reason)

    def onMessage(self, payload, isBinary):
        message = payload
        if not isBinary:
            message = payload.decode('utf8')
        self.factory.client.onMessage(message, isBinary)

    def send(self, message, **options):
        isBinary = False
        if 'isBinary' in options:
            isBinary = options['isBinary']

        if isBinary:
            payload = message
        else:
            payload = message.encode('utf8')

        self.sendMessage(payload, **options)

        return self.state == protocol.WebSocketProtocol.STATE_OPEN


class SockJSClientFactory(WebSocketClientFactory, ReconnectingClientFactory):

    protocol = SockJSClientProtocol

    def clientConnectionFailed(self, connector, reason):
        self.client.onError(reason.getErrorMessage())

    def clientConnectionLost(self, connector, reason):
        self.client.onDisconnect(reason.getErrorMessage())


class SockJS(object):

    def __init__(self, prefix, host='127.0.0.1', port=5000, debug=False, **options):
        self.factory = None
        self.protocol = None

        self.connected = defer.Deferred()
        self.disconnected = defer.Deferred()

        self.host = host
        self.port = port
        self.debug = debug

        self.url = 'ws://%s:%s%s' % (host, port, '/'.join([prefix, 'websocket']))

        autoConnect = True
        if 'autoConnect' in options:
            autoConnect = options['autoConnect']

        if autoConnect:
            self.connect()

    def onOpen(self):
        pass

    def onError(self, reason):
        pass

    def onClose(self, wasClean, code, reason):
        pass

    def onMessage(self, payload, isBinary):
        pass

    def onConnect(self, protocol, response):
        self.protocol = protocol
        self.disconnected = defer.Deferred()
        self.connected.callback(response)

    def onDisconnect(self, reason):
        self.protocol = None
        self.connected = defer.Deferred()
        self.disconnected.callback(reason)

    def connect(self):
        self.factory = SockJSClientFactory(self.url, debug=self.debug)
        self.factory.client = self
        self.factory.connector = reactor.connectTCP(self.host, self.port, self.factory)

        return self.connected

    def close(self, delay=None):
        if self.protocol:
            if delay is not None:
                reactor.callLater(delay, self.protocol.sendClose)
            else:
                self.protocol.sendClose()

        return self.disconnected

    @defer.inlineCallbacks
    def send(self, message, **options):
        yield self.connected
        status = self.protocol.send(message, **options)
        defer.returnValue(status)
