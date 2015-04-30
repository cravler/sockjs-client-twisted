# SockJS-Client-Twisted

SockJS client for Twisted-Python

## Installation

``` bash
pip install txsockjs_client
```

## Application

``` python
from txsockjs_client import SockJS
from twisted.internet import defer, reactor

@defer.inlineCallbacks
def helloSockJS():
    client = SockJS('/echo', host='127.0.0.1', port=5000)
    yield client.send('Hello SockJS')
    yield client.close()

    if reactor.running:
        reactor.stop()

if __name__ == '__main__':
    helloSockJS()
    reactor.run()
```

## Events

``` python
class SockJSClient(SockJS):
    def onOpen(self):
        print '[OPEN]'

    def onError(self, reason):
        print '[ERROR]: %s' % reason

    def onClose(self, wasClean, code, reason):
        print '[CLOSE]: %s' % reason

    def onMessage(self, message, isBinary):
        print '[MESSAGE]: %s' % message

client = SockJSClient('/echo')
```

## Reconnect

``` python
client.factory.retry()
```

## License

This software is under the MIT license. See the complete license in:

```
LICENSE
```