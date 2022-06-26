from os import system as sys

import numpy as np



# alle Platzierungen für die Klasse class_battleship anfordern
# nimmt alle Useranfragen engegen die für die Platzierung wichtig sind
class Setup:
    def __init__(self):
        
        self.myBoard = None
        # wird am Ende als initINFO, funktion der class_battleship, zurückgegeben
        self.placement = {}

    def main(self):
        # wird auf true gesetzt wenn alle Eingaben angefordert worden
        done = False

        while not done:
            #reinigt die Console bzw. Terminal
            sys("clear")

            # erzeugt eine leere Karte
            self.createBoard()

            # nimmt die Inputs entgegen
            for i in range(5):
                self.getInput(i)

            # printet das finale Brett und nimmt die Bestätigung entgegen, falls bestätigt,wird die Platzierung zurueck gegeben
            # falls nicht bestätigt, wird das Brett zurueck gesetzt und der User macht erneut seine Eingaben
            sys("clear")
            self.drawBoard()
            confirm = input("Das ist ihr Spielbrett möchten Sie fortfahren ? (j/n) ")
            if confirm.upper() == 'J':
                done = True
            else:
                # reset placement
                self.placement = {}

        # gibt die Platzierung zurück
        return self.placement

    # erzeugt ein leeres Brett
    def createBoard(self):
        temp = []
        for i in range(64):
            temp.append('?')
        self.myBoard = np.reshape(np.array(temp), (-1, 8)) #-1 bedeutet eindimensionales Array welches hier neu geformt wird ohne die Daten zu ändern
        #keine wirkliche Auswirkung

    #hier wird das Brett gezeichnet und die Frage zeichen im Array mit | befüllt
    def drawBoard(self):
        print("   0 1 2 3 4 5 6 7 ")
        rowIndex = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        for i in range(8):
            line = rowIndex[i] + " |"
            for j in range(8):
                line += self.myBoard[i][j]
                line += "|"
            print(line)

    #das Brett wird mit dem neuen Schiff aktuallisiert. Position, Orientierung und Schiffsnummer werden angegeben
    def updatedBoard(self, pos_t, ori, shipNum):
        shipHeath = [5, 4, 3, 3, 2]
        self.myBoard[pos_t[0]][pos_t[1]] = "\u25C9"
        pos_row = pos_t[0]
        pos_col = pos_t[1]

        for i in range(shipHeath[shipNum] - 1):
            if ori == 0:
                pos_col += 1
                self.myBoard[pos_row][pos_col] = "\u25C9"
            elif ori == 1:
                pos_row += 1
                self.myBoard[pos_row][pos_col] = "\u25C9"
            elif ori == 2:
                pos_col -= 1
                self.myBoard[pos_row][pos_col] = "\u25C9"
            elif ori == 3:
                pos_row -= 1
                self.myBoard[pos_row][pos_col] = "\u25C9"

    # ship num range from 0 - 4, 0 being the carrier, 4 being the destroyer
    # Nimmt die Eingabe entgegen
    def getInput(self, shipNum):
        gotValidInput = False

        prompt = ["Gebe die Koordinate und Orientierung fuer den Frachter (5) bsp. A1 3",
                  "Gebe die Koordinate und Orientierung fuer den Kampfschiff (4) bsp. A1 3",
                  "Gebe die Koordinate und Orientierung fuer das U-Boot (3) bsp. A1 3",
                  "Gebe die Koordinate und Orientierung fuer den Kreuzer (3) bsp. A1 3",
                  "Gebe die Koordinate und Orientierung fuer den Zerstoerer (1) bsp. A1 3"]

        ships = ['frachter', 'kampfschiff', 'u-boot', 'kreuzer', 'zerstoerer']


        while not gotValidInput:
            # Console bzw. Terminal reinigen
            sys("clear")

            # Spielbrett zeichnen
            self.drawBoard()

            print("Für die Orentierung des Schiffes geben Sie folgende Zahlen ein:\n")
            print("0 für Osten, 1 für Süden, 2 für Westen, 3 für Norden")

            # Die Eingabe abfangen und bearbeiten
            print(prompt[shipNum])
            placement = input().split()
            pos = placement[0]
            ori = int(placement[1])

            # input überprüfen
            if len(pos) == 2:  # Die Position überprüfen
                rowIndex = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
                if pos[0] in rowIndex and 0 <= int(pos[1]) <= 7:
                    if 0 <= ori <= 3:  # Die Oreintierung ueberprüfen
                        gotValidInput = True

            # wenn die Eingabe incorrect, dann gibt der User alles wieder ein
            if not gotValidInput:
                print("Unglueltige Eingabe, Bitte nochmal versuchen!")
                break
            else:  # Aktualisiert self.placement und updatedBoard wenn Eingabe korrekt
                pos_t = self.translateCoordinate(pos)  # position als ein int tuple
                self.placement[ships[shipNum]] = [pos_t, ori]
                self.updatedBoard(pos_t, ori, shipNum)

    # Diese Methode übersetzt die Eingegebenen Buchstaben in Zahlen damit das Programm versteht um was es sich dabei handelt
    @staticmethod
    def translateCoordinate(string):
        rowIndex = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7}
        rowLetter = string[0]
        rowNum = rowIndex[rowLetter]
        return tuple([rowNum, int(string[1])])
