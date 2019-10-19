"""Net-realated function

Only holds the Server class atm.
"""
import socket
import network # pylint: disable=import-error
import uwebsocket # pylint: disable=import-error, unused-import
import websocket_helper # pylint: disable=import-error, unused-import
from machine import Pin # pylint: disable=import-error
from page import html, html_2


class Server():
    """HTML server

    Used by calling the setup_AP function which after a connection
    will serve the html in the page file to the connected machine.
    """
    def __init__(self):
        """HTML import

        Imports the html into the class
        Sets up the access point
        """
        self.html = html
        self.html_2 = html_2
        self.access_point = network.WLAN(network.AP_IF)
        self.addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
        self.sock = socket.socket()

    def setup_ap(self):
        """Runs a full webserver once

        Sets up WLAN, listens for a connection, accepts and the
        serves the HTML.

        Returns:
            WLAN_AP -- network.WLAN(network.AP_IF) configured
        """
        self.access_point.config(essid='ESP-AP')
        self.access_point.active(True)
        self.listen()
        self.accept_conn()
        return self.access_point

    def listen(self):
        """Listens for connection

        Binds to 0.0.0.0:80

        Returns:
            socket -- configured socket 0.0.0.0:80
        """
        self.sock.bind(self.addr)
        self.sock.listen(1)
        print("Listening on: ", self.addr)
        return self.sock


    def accept_conn(self):
        """Serves HTML

        Accepts the connection, pulls data from pins, generates the
        full html, serves it and closes the connection
        to make ws-connection possible.
        """
        pins = [Pin(i, Pin.IN) for i in (0, 2, 4, 5, 12, 13, 14, 15)]
        connection, addr = self.sock.accept()
        print('client connected from: ', addr)
        cl_file = connection.makefile('rwb', 0)
        while True:
            line = cl_file.readline()
            if not line or line == b'\r\n':
                break
        rows = ['<tr><td>%s</td><td>%d</td></tr>' % (str(p),
                                                     p.value()) for p in pins]
        response = self.html + self.html_2 % '\n'.join(rows)
        connection.send(response)
        connection.close()
        print(cl_file)
