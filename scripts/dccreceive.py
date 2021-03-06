#! /usr/bin/env python
#
# Example program using irc.client.
#
# This program is free without restrictions; do anything you like with
# it.
#
# Joel Rosdahl <joel@rosdahl.net>

from __future__ import print_function

import irc.client
import os
import struct
import sys

class DCCReceive(irc.client.SimpleIRCClient):
    def __init__(self):
        irc.client.SimpleIRCClient.__init__(self)
        self.received_bytes = 0

    def on_ctcp(self, connection, event):
        args = event.arguments[1].split()
        if args[0] != "SEND":
            return
        self.filename = os.path.basename(args[1])
        if os.path.exists(self.filename):
            print("A file named", self.filename,)
            print("already exists. Refusing to save it.")
            self.connection.quit()
        self.file = open(self.filename, "wb")
        peeraddress = irc.client.ip_numstr_to_quad(args[2])
        peerport = int(args[3])
        self.dcc = self.dcc_connect(peeraddress, peerport, "raw")

    def on_dccmsg(self, connection, event):
        data = event.arguments[0]
        self.file.write(data)
        self.received_bytes = self.received_bytes + len(data)
        self.dcc.privmsg(struct.pack("!I", self.received_bytes))

    def on_dcc_disconnect(self, connection, event):
        self.file.close()
        print("Received file %s (%d bytes)." % (self.filename,
                                                self.received_bytes))
        self.connection.quit()

    def on_disconnect(self, connection, event):
        sys.exit(0)

def main():
    if len(sys.argv) != 3:
        print("Usage: dccreceive <server[:port]> <nickname>")
        print("\nReceives one file via DCC and then exits.  The file is stored in the")
        print("current directory.")
        sys.exit(1)

    s = sys.argv[1].split(":", 1)
    server = s[0]
    if len(s) == 2:
        try:
            port = int(s[1])
        except ValueError:
            print("Error: Erroneous port.")
            sys.exit(1)
    else:
        port = 6667
    nickname = sys.argv[2]

    c = DCCReceive()
    try:
        c.connect(server, port, nickname)
    except irc.client.ServerConnectionError as x:
        print(x)
        sys.exit(1)
    c.start()

if __name__ == "__main__":
    main()
