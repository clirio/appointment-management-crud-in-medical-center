""" udp_server.py:
SERVIDOR UDP:
Servidor de logging de la App Turnera, visualizacion en consola y generacion un archivo log ("registroserver.log")

"""

import logging
import socketserver
import socket
import threading
import socketserver
from pathlib import Path
import os
import sys
import binascii
from datetime import datetime

global PORT


class MyUDPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]

        print("---" * 25)
        print(data.decode("UTF-8"))
        print("---" * 25)
        logging.basicConfig(filename="registroserver.log", level="DEBUG")
        logging.info(data.decode("UTF-8"))
        value2 = "Registro de la información recibida en el servidor"
        socket.sendto(value2.encode("UTF-8"), self.client_address)


if __name__ == "__main__":
    HOST, PORT = "localhost", 9999
    with socketserver.UDPServer((HOST, PORT), MyUDPHandler) as server:
        server.serve_forever()
