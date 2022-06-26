import pickle
import socket

import netifaces as ni


class COM:

    #Die IPs sowie Ports werden hier initialisiert
    def __init__(self, OPPip, txport, rxport):
        self.OPPip = OPPip
        self.txport = txport
        self.rxport = rxport
        self.tx = socket.socket()
        self.rx = socket.socket()
        self.ip = self.selfip()
        self.rx.bind((str(self.ip), int(rxport)))

    #Mit dieser Funktion werden die Ports geschlossen
    def stop(self):
        self.rx.close() #recive bzw. empfänger Port wird geschlossen
        self.tx.close() #transmitt also sender Port wird geschlossen

    #Mit dieser Funktion wird die Nachricht verschickt, in ein Byte stream umgewandelt und an den Transmitting übertragen
    def send(self, msg):
        msg_b = pickle.dumps(msg) #Pickle wandelt die nachricht in Bytes
        self.tx.send(msg_b) #umgewandelte Bytes werden an den Transmitting port übergeben

    #Mit dieser Funktion wird die Nachricht empfangen
    def recieve(self):
        msg_b = self.c.recv(1024) #Die Nachricht wird empfangen
        msg = pickle.loads(msg_b) #Die Nachricht wird übersetzt
        return msg

    #Mit dieser Funktion hört der Port auf den empfänger
    def listen(self):
        self.rx.listen()
        print("Listen accepted")

        self.c, self.addr = self.rx.accept()
        print(" socket accepted")

    #Mit dieser Funktion verbindet sich der Spieler mit dem Ip und dem Tramitting Port des gegners
    def connect(self):
        self.tx.connect((str(self.OPPip), int(self.txport)))

    #Selfip erzeugt die IP des spielers auf dem das Programm läuft
    def selfip(self):
        ip = ni.ifaddresses('en0')[ni.AF_INET][0]['addr'] #
        return ip
