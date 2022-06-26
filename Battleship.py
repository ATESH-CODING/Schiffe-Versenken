import os

#Numpy und netifaces müssen importiert werden um das Spiel zu Spielen
#Beim Starten vom Terminal wird das Erfordert.
try:
    import numpy
except ImportError:
    os.system("pip install numpy")

try:
    import netifaces
except ImportError:
    os.system("pip install netifaces")

os.system("python main.py")
