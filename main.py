import platform
import random
from os import system as sys

from class_COM import COM
from class_battleship import BattleShip
from class_setup import Setup


def main():

    # Die Inputs für die IP und Sockets des Gegners werden gesammelt
    sys("clear")

    input("Willkommen zum Schiffeversenken.\n")

    OPPip = input("Gebe die IP des gegners ein:\n")
    txport = input("Welcher Port uebertraegt die Befehle?\n")
    rxport = input("Welcher Port empfaengt die Befehle?\n")
    host = input("Sind Sie der Host? (j/n) \n")
    # Sockets und das Spielbrett Initzialisieren
    sockets = COM(OPPip, txport, rxport)

    while True:
        try:
            boarddict = initBoard()
            board = BattleShip(boarddict)
            break
        except KeyboardInterrupt:
            print("Interrupted")
            exit(1)

    # Spieler Identifizieren -> Ob Host oder nicht
    if (host == "j"):
        print("Warten auf Spieler zwei..\n")

        # Auf den Socket hören und für Spieler 2 blockieren
        sockets.listen()
        connectedmsg = sockets.recieve()
        print("Spieler 2 ist ... " + connectedmsg)

        # wenn Spieler 1 zu erst dran ist
        if (random.randint(1, 2) == 1): #die Mathode erzeugt die Zahl "eins" damit der erste spieler dran ist

            # Verbindet sich mit dem socket und initialisiert den ersten Abschuss
            sockets.connect()
            attacksocket(board, sockets)
            board.turn = False
            game(board, sockets)

        #Falls spieler 2 zur erst dran ist
        else:
            # verbindet die sockets und informiert den 2ten Spieler, dass der Erste Spieler als zweiter am Zug ist
            sockets.connect()
            sockets.send("s")
            # überprüft ob der Abschuss erfolgreich war und aktualisiert das Brett
            recieveAttack(board, sockets)
            board.turn = True
            game(board, sockets)

    # Wenn der Spieler 1 nicht der Host ist
    else:
        print("Connecting to Host..\n")
        # Sockets verbinden und signalisieren dass der Spieler verbunden ist
        sockets.connect()
        sockets.send("Connected")
        #auf die Nachricht hören wer zu erst dran ist
        sockets.listen()
        connectedmsg = sockets.recieve()
        # Als zweiter
        if (connectedmsg != "s"):
            # Check if the attack hit and update the board
            # Überprüft ob der Abschuss erfolgreich war und aktualisiert das Brett
            value = board.checkAttack(connectedmsg)
            sendvalue(value, sockets)
            board.turn = True
            game(board, sockets)

        # Als erster
        elif (connectedmsg == "s"):
            attacksocket(board, sockets)
            game(board, sockets)


def game(board, sockets):
    #Schleife läuft solange bis das Spiel endet bzw. alle Schiffe des Gegners versenkt wurden

    while not board.defeated():
        # wenn Spieler dran ist
        if (board.turn):
            attacksocket(board, sockets)
        # wenn Spieler nicht dran ist
        else:
            recieveAttack(board, sockets)

    sys("clear")
    print("Du hast verloren!")
    sockets.stop()


# Funktion um abzufeuern
def attacksocket(board, sockets):
    # empfängt die coordinaten des Users als(x, y) und setzt turn auf false
    while True:
        attack = input("Du bist dran! Platziere jetzt! bsp. A1 \n")
        tp = TranslateCoordinate(list(attack))
        x, y = tp[0], tp[1]
        if (0 <= x <= 7 or 0 <= y <= 7):
            break
        else:
            print("Bitte gebe eine gültige Koordinate")

    sockets.send(tp)
    board.turn = False
    recievemsg = sockets.recieve()
    if recievemsg == "Treffer!":
        board.updateBoard(tp, 1)
    if recievemsg == "Versenkt!":
        board.updateBoard(tp, 2)
    if recievemsg == "Verfehlt!":
        board.updateBoard(tp, 0)
    if recievemsg == "Verloren":  # Der Spieler hat das Spiel gewonnen, Nachricht wird gedruckt und das Spiel unterbrochen
        sys("clear")
        print("Sie haben gewonnen")
        sockets.stop()
        exit(0)


# Überprüft die Attacke und aktualisiert das Brett
def recieveAttack(board, sockets):
    connectedmsg = sockets.recieve()
    value = board.checkAttack(connectedmsg)
    sendvalue(value, sockets)
    board.turn = True


# initialisiert das Brett und sendet sie an board class
def initBoard():

    # ruft die Klasse Setup um die User inputs abzufragen und generiert eine Überseztzung für die Klasse class_battleship
    setup = Setup()
    return setup.main()


# Diese funktion gibt den Status der abgefeuerten Racketen zurück
def hit(value):
    if value == 0:
        return "Miss!\n"
    if value == 1:
        return "Hit!\n"
    if value == 2:
        return "Hit and Sunk!\n"

#Diese Funktione übernimmt den wert und sendet an den jeweiligen Socket den Status
def sendvalue(value, sockets):
    if value == 0:
        sockets.send("Verfehlt!")
    if value == 1:
        sockets.send("Treffer!")
    if value == 2:
        sockets.send("Versenkt!")
    if value == 3:
        sockets.send("Verloren")

#Diese Funktion übersetzt die Koordinaten der X achse in Zahlen
def TranslateCoordinate(string):
    rowIndex = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7}
    rowLetter = string[0]
    rowNum = rowIndex[rowLetter]
    return tuple([rowNum, int(string[1])])

# hier wird die main methode aufgerufen.
if __name__ == '__main__':
    if platform.system() == 'Windows':
        print("OH, es sieht so aus als ob du Windows benutzt! Bitte führe das Skript auf Linux oder MacOs aus.")
        exit(1)
    else:
        main()
