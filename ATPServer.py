import threading
import logging
import sys
import socketserver
import ssl

logging.basicConfig(filename="ATPServer.log",
                    level=logging.DEBUG,
                    format='%(name)s: %(message)s',
                    )

EMAIL = "test@test.test"

class ATPRequestHandler(socketserver.BaseRequestHandler):

    def __init__(self, request, client_address, server):
        self.logger = logging.getLogger('ATPRequestHandler')
        self.logger.debug('request %s %s', client_address, server)
        socketserver.BaseRequestHandler.__init__(self, request, client_address, server)
        return

    def handle(self):
        self.logger.debug('handle')
        data = self.request.recv(1072)
        self.logger.debug('recv()->"%s"', data)
        if self.parese_req(data):
            self.resp()
        else:
            self.error_resp()
        self.request.send(self.resp_msg.encode())
        return

    def error_resp(self):
        self.logger.debug('error_response')
        self.resp_msg = "TALK TO THE HAND\nHASTA LA VISTA, BABY!\nYOU HAVE BEEN TERMINATED\n"

    def resp(self):
        self.logger.debug('response')
        self.resp_msg = "TALK TO THE HAND\nNO PROBLEMO\n" + str(EMAIL) + "\nYOU HAVE BEEN TERMINATED\n"

    def parese_req(self, data):
        if data == b'ATP/0.1\nTALK TO THE HAND\nI NEED YOUR CLOTHES YOUR BOOTS AND YOUR MOTORCYCLE\nYOU HAVE BEEN TERMINATED\n':
            return True
        else:
            return False


class ATPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    def __init__(self, server_address, handler_class=ATPRequestHandler):
        self.logger = logging.getLogger('ATPServer')
        self.logger.debug('ATPServer %s', server_address)
        socketserver.TCPServer.__init__(self, server_address, handler_class, False)
        self.socket = ssl.wrap_socket(self.socket, keyfile='keyfile', 
            certfile='certfile', server_side=True, cert_reqs=ssl.CERT_REQUIRED, ssl_version=ssl.PROTOCOL_TLSv1_2, ca_certs='certfile')
        self.server_bind()
        self.server_activate()
        return

if __name__ == '__main__':
    address = ('37.9.171.172', 4115) 
    # address = ('localhost', 4115) 
    server = ATPServer(address, ATPRequestHandler)
    server.serve_forever()

