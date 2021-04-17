import collections
import operator

class Huffman:

    filename = ""
    FILE = None
    freq = {}

    def __init__(self, filename):
        self.filename = filename
        self.FILE = open(self.filename, 'rb')

    def analyze(self):
        # zaanalizuj plik bajt po bajcie
        while True:
            byte = self.FILE.read(1)
            # jeżeli koniec pliku to zakończ
            if not byte: break
            # dopisz zapisz ilość wystąpień danego byte'u
            if not byte in self.freq: self.freq[byte] = 1
            else: self.freq[byte] += 1
        # posortuj po ilości wystąpień
        self.freq = dict(sorted(self.freq.items(), key=lambda item: item[1]))
        # wróć na początek pliku
        self.FILE.seek(0)