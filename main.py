import socket # pylint: disable=import-error
import machine # pylint: disable=import-error
import uwebsocket # pylint: disable=import-error
import websocket_helper # pylint: disable=import-error
from netFuncs import Server
from apa import Apa102


BRIGHTNESS = 225
CLK_PIN = 21
DATA_PIN = 17
LED_COUNT = 3
PORT = 8266

LEDS = Apa102(BRIGHTNESS, connectionK_PIN, DATA_PIN, LED_COUNT)

def ws_inc_handler(flag):
    """Handles incoming msg on the WS
    
    Splits incoming msg into RBG values and updates the LEDs
    to coresponding values
    
    Arguments:
        flag {flag?} -- function is called with it when msg
                        recieved
    """
    line = ws.readline().decode()
    print(line)
    if line != "Established":
        red, green, blue = line.split(".")
        LEDS.change_led_colour([int(blue), int(green), int(red)])

def accept_conn(listen_s):
    """Accept socket connection & transform to WS
    
    Acceptes connection, makes it a WS and
    sets ws_inc_handler as the msg handler for the connection
    
    Arguments:
        listen_s {socket} -- The socket that is listened 
                             for connections on
    
    Returns:
        websocket -- The websocket connection
    """
    connection, remote_addr = listen_s.accept()
    print(remote_addr)
    websocket_helper.server_handshake(connection)
    print("Connection: ", connection)
    global ws
    ws = uwebsocket.websocket(connection, True)
    connection.setblocking(False)
    connection.setsockopt(socket.SOL_SOCKET, 20, ws_inc_handler)
    return ws


def setup_conn():
    """Socket setup function
    
    Sets up a listen on 0.0.0.0 and the defined port, 
    configuring accept_conn to be executed when a
    connection is to be established.
    
    Returns:
        socket -- the socket which is listened on
    """
    listen_s = socket.socket()
    listen_s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    addr = socket.getaddrinfo("0.0.0.0", PORT)[0][-1]
    listen_s.bind(addr)
    listen_s.listen(1)
    listen_s.setsockopt(socket.SOL_SOCKET, 20, accept_conn)
    return listen_s


def main():
    while True:
        if machine.Pin(0).value() != 0:
            break
        HTTP_server = Server()
        Access_point = HTTP_server.setup_AP()
        setup_conn()
        break
main()
