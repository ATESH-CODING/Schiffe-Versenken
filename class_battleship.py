import numpy as np
from os import system as sys


class BattleShip:
    def __init__(self, initINFO):
        """
        initINFO ist das Format für die Schiffe
        {
            'frachter':[pos,ori],
            'kampfschiff':[pos,ori],
            'kreuzer':[pos,ori],
            'u-boot':[pos,ori],
            'zerstoerer':[pos,ori]
         }
         pos ist ein Tuple (zeile num, spalte num), es zeigt die Spitze des Schiffes
            0 bedeutet der Heck das schiffes zeigt richtung osten von der Spitze aus gesehen
            1 bedeutet süden
            2 bedeutet westen
            3 bedeutet norden
        """

        # variable beinhaltet alle möglichen abschuss positionen, wird benutzt um die Platzierung zu überprüfen(Überlappung)
        self.globalHitMap = []

        #zeigt an ob der Host dran ist oder nicht
        self.turn = None

        # Das gegnerische Spielbrett
        self.guessBoard = None

        #importiert die Position jedes Shiffes
        #im Array -> ships 0 für frachter, 1 für kampfschiff -> 2 für Kreuzer -> 3 für U Boot -> 4 für Zerstörer

        self.ships = []
        self.ships.append({'pos': initINFO['frachter'][0],
                           'ori': initINFO['frachter'][1],
                           'leben': 5,
                           'versenkt': False,
                           'hitmap': []})
        self.ships.append({'pos': initINFO['kampfschiff'][0],
                           'ori': initINFO['kampfschiff'][1],
                           'leben': 4,
                           'versenkt': False,
                           'hitmap': []})
        self.ships.append({'pos': initINFO['kreuzer'][0],
                           'ori': initINFO['kreuzer'][1],
                           'leben': 3,
                           'versenkt': False,
                           'hitmap': []})
        self.ships.append({'pos': initINFO['u-boot'][0],
                           'ori': initINFO['u-boot'][1],
                           'leben': 3,
                           'versenkt': False,
                           'hitmap': []})
        self.ships.append({'pos': initINFO['zerstoerer'][0],
                           'ori': initINFO['zerstoerer'][1],
                           'leben': 2,
                           'versenkt': False,
                           'hitmap': []})

        # erzeugt ein leeres Brett
        self.createBoard()
        # erzeugt abschuss position
        self.createHitMap()

    # abschuss Position erzeugen
    def createHitMap(self):
        for i in self.ships:
            i['hitmap'].append(i['pos'])
            pos_temp = list(i['pos'])
            if i['ori'] == 0:
                for j in range(i['leben'] - 1):
                    pos_temp[1] += 1
                    self.placementCheck(pos_temp, i)
            elif i['ori'] == 1:
                for j in range(i['leben'] - 1):
                    pos_temp[0] += 1
                    self.placementCheck(pos_temp, i)
            elif i['ori'] == 2:
                for j in range(i['leben'] - 1):
                    pos_temp[1] -= 1
                    self.placementCheck(pos_temp, i)
            elif i['ori'] == 3:
                for j in range(i['leben'] - 1):
                    pos_temp[0] -= 1
                    self.placementCheck(pos_temp, i)
            else:
                print("ungueltige Richtungsangabe!")
                exit(1)

    #wird in creatHitMap() gerufen. Es ruft indexInRange() und placementOverlap() um die gültigkeit der Platzierung zu überprüfen
    def placementCheck(self, pos_temp, i):
        i['hitmap'].append(tuple(pos_temp))
        #ist die Platzirung korrekt dann füge diesen dem globalHitMap hinzu und fahre fort

        #ist das nicht der Fall error printen und Programm beenden
        if not self.placementOverlap(tuple(pos_temp)) and self.indexInRange(tuple(pos_temp)):
            self.globalHitMap.append(tuple(pos_temp))
        else:
            print("Falsche Platzierung, vergewissere dich, dass die Schiffe nicht ueberlappen oder aus der dem Brett raus schauen")
            exit(1)

    # gibt den Wert true wieder wenn das Schiff ausserhalb der Karte platziert ist
    def indexInRange(self, pos):
        if 0 <= pos[0] <= 7 and 0 <= pos[1] <= 7:
            return True
        return False

    # gibt den Wert true wieder wenn zwei schiffe überlappen
    def placementOverlap(self, pos):
        if pos in self.globalHitMap:
            return True
        return False

    #erzeugt eine 2D numpy array, welcher mit '?' gefuellt ist
    def createBoard(self):
        temp = []
        for i in range(64):
            temp.append('?')
        self.guessBoard = np.reshape(np.array(temp), (-1, 8))

    #aktualisiert die Karte nach dem status und pos
    # cleart die Console bzw. Terminal nach dem status und printet das Brett
    # pos idt ein tupel (row num, col num) und status koennte equivalent zu 0 für miss oder 1 für hit sein
    # '◈' bedeutet hit '◇' bedeutet miss
    def updateBoard(self, pos, status):
        sys("Clear")
        if status == 0:
            self.guessBoard[pos[0]][pos[1]] = '\u25C7'
            print("Ups, du hast verfehlt!")
        else:
            if self.guessBoard[pos[0]][pos[1]] == '?':
                self.guessBoard[pos[0]][pos[1]] = '\u25C8'
                if status == 1:
                    print("Hura!!! Das war ein Treffer")
                else:
                    print("Du hast ein Schiff versenkt!")
        self.printGuessBoard()

    # liefert 0 wenn keinen Treffer, 1 für Treffer und 2 für Treffer und versenkt
    def checkAttack(self, pos):
        for i in self.ships:
            if pos in i['hitmap']:
                i['hitmap'].remove(pos)
                i['leben'] -= 1
                if i['leben'] == 0:
                    if self.defeated():
                        return 3  # Spielverloren
                    print("Oh nein! Der Gegner hat eins deiner Schiffe versenkt")
                    return 2  # Treffer und versenkt
                print("Achtung! wir sind getroffen worden.")
                return 1  # Treffer
        print("Der Feind hat uns verfehlt! wir werden nicht den selben Fehler machen! ")
        return 0  # keinen Treffer

    # liefert den Wert True wenn alle Schiffe versenkt wurden
    def defeated(self):
        for i in self.ships:
            if i['sunk'] is False:
                return False
        return True

    # erzeugt das Spielbrett
    def printGuessBoard(self):
        print("   0 1 2 3 4 5 6 7 ")
        rowIndex = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        for i in range(8):
            line = rowIndex[i] + " |"
            for j in range(8):
                line += self.guessBoard[i][j]
                line += "|"
            print(line)



