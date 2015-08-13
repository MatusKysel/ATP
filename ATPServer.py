import threading
import logging
import sys
import socketserver
import ssl

logging.basicConfig(filename="ATPServer.log",
                    level=logging.DEBUG,
                    format='%(name)s: %(message)s',
                    )

EMAIL = "robert.szomolanyi@erstegroupit.com"

class ATPRequestHandler(socketserver.BaseRequestHandler):

    def __init__(self, request, client_address, server):
        self.logger = logging.getLogger('ATPRequestHandler')
        self.logger.debug('request %s', client_address)
        socketserver.BaseRequestHandler.__init__(self, request, client_address, server)
        return

    def handle(self):
        self.logger.debug('request handle')
        data = self.request.recv(1072)
        self.logger.debug('recv: %s', data)
        if self.parese_req(data):
            self.resp()
        else:
            self.error_resp()
        self.request.send(self.resp_msg.encode())
        return

    def error_resp(self):
        self.logger.debug('sending error_response')
        self.resp_msg = "ATP/0.1\nTALK TO THE HAND\nHASTA LA VISTA, BABY!\nYOU HAVE BEEN TERMINATED\n"

    def resp(self):
        self.logger.debug('sending response')
        self.resp_msg = "ATP/0.1\nTALK TO THE HAND\nNO PROBLEMO\n" + str(EMAIL) + "\nYOU HAVE BEEN TERMINATED\n"

    def parese_req(self, data):
        if data == b'ATP/0.1\nTALK TO THE HAND\nI NEED YOUR CLOTHES YOUR BOOTS AND YOUR MOTORCYCLE\nYOU HAVE BEEN TERMINATED\n':
            return True
        else:
            return False


class ATPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    def __init__(self, server_address, handler_class=ATPRequestHandler, secure=False):
        self.logger = logging.getLogger('ATPServer')
        self.logger.debug('ATPServer %s', server_address)
        socketserver.TCPServer.__init__(self, server_address, handler_class, False)
        if secure:
            self.socket = ssl.wrap_socket(self.socket, keyfile='keyfile', 
                certfile='certfile', server_side=True, cert_reqs=ssl.CERT_REQUIRED, 
                ssl_version=ssl.PROTOCOL_TLSv1_2, ca_certs='certfile')
        self.server_bind()
        self.server_activate()
        return

if __name__ == '__main__':
    address = ('188.166.28.154', 4115) 
    # address = ('localhost', 4115) 
    server = ATPServer(address, ATPRequestHandler, True)
    server.serve_forever()

