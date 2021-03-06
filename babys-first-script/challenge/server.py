#!/usr/bin/env python3

from pwn import *

import socket
import threading
import socketserver

# Custom for challenge
import string
import random

N = 64
FLAG = 'flag{is_th3r3_an_ech0_in_h3r3}'

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        payload = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))
        tube = remote('localhost', 0, sock=self.request)
        tube.sendline(payload)
        recvd = tube.readline().strip().decode('utf-8')
        if recvd == payload:
            tube.sendline(FLAG)
        else:
            tube.sendline('Nope.')


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


if __name__ == '__main__':
    HOST, PORT = '0.0.0.0', 9000

    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    with server:
        server.serve_forever()
