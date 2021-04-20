from config import *
from bitstring import BitArray

class HuffmanReader:

    # ogólne
    filename = ""
    FILE = None
    
    # Huffmanowe
    tree = []
    dic = {}

    # plikowe
    EOF = False
    buffer = ''


    def __init__(self, filename):
        self.filename = filename
        self.FILE = open(self.filename, 'rb')
        self.__analyze()
        self.__createTree()
        self.__rewriteAsDict()

    def __analyze(self):
        freq = {}
        # zaanalizuj plik bajt po bajcie
        while True:
            byte = self.FILE.read(WORD_SIZE)
            # jeżeli koniec pliku to zakończ
            if not byte: break
            # dopisz / zapisz ilość wystąpień danego byte'u
            if not byte in freq: freq[byte] = 1
            else: freq[byte] += 1
        # posortuj po ilości wystąpień
        freq = dict(sorted(freq.items(), key=lambda item: item[1]))
        # wróć na początek pliku
        self.FILE.seek(0)
        # przepisz słownik frekwencji na listę node'ów
        tmp = []
        i = 0
        for key in freq:
            tmp.append(Node(key, freq[key]))
            tmp[i].leaf = True
            i += 1
        self.tree = tmp

    def __createTree(self):
        if type(self.tree) != list: return
        while len(self.tree) > 1:
            # posortuj listę po freq
            self.tree = sorted(self.tree, key=lambda x : x.freq)

            # weź 2 node'y o najmniejszym freq
            left = self.tree[0]
            right = self.tree[1]
            # utwórz nowy node o wartości freq sumy lewego i prawego
            newNode = Node(b'', left.freq + right.freq, left, right)

            # usuń node'y wykorzystane do zbudowania pod drzewa
            self.tree.remove(left)
            self.tree.remove(right)
            # dodaj poddrzewo do listy
            self.tree.append(newNode)
        # dla wygody przepisz obiekt
        self.tree = self.tree[0]

    def __rewriteAsDict(self, node=None, code=''):
        # jeżeli pierwsze odwołanie, to zacznij od roota
        if node == None: node = self.tree
        
        # jak idziesz w lewo, to dopisz '0'
        if node.left:
            self.__rewriteAsDict(node.left, code + "0")

        # jak idziesz w prawo, to dopisz '1'
        if node.right:
            self.__rewriteAsDict(node.right, code + "1")

        # jak to liść, to zapisz kod w słowniku
        if node.isLeaf():
            self.dic[node.char] = code

    def printDict(self):
        length = 0
        for key in self.dic:
            print("{} -> {}".format(key, self.dic[key]))
    
    def printWeight(self):
        OG = 0 # rozmiar przed kompresją
        after = 0 # rozmiar po kompresji
        while True:
            byte = self.FILE.read(1) # odczytaj bajt
            if not byte: break # jeżeli nie ma, to koniec pliku
            OG += 1 # aktualizuj rozmiar
            after += len(self.dic[byte]) # wyszukaj definicję danego bajtu
        after /= 8 # podziel na 8, bo odczytano ilość bitów
        self.FILE.seek(0) # wróć na początek pliku
        print("{}B -> {}B".format(OG, after))
        print("{}% kompresji".format(round((1-after/OG)*100, 2)))

    def readNext(self):
        to_send = BitArray()
        # okreslenie ile razy ma się wykonać pętla (ilość bitów)
        bits_to_read = PACKET_SIZE
        while len(to_send.bin) != bits_to_read:
            # jeżeli wartość jest pusta to 
            if len(self.buffer) == 0:
                # przypisujemy pierwszy bajt z pliku 
                byte = self.FILE.read(WORD_SIZE)
                # jeżeli nie ma to kończymy
                if not byte:
                    self.EOF = True
                    break
                # przypisujemy wartości definicję  
                self.buffer = self.dic[byte] 
            # dodajemy bit do naszej tablicy
            to_send.bin += self.buffer[0]
            # ucinamy dodany bit
            self.buffer = self.buffer[1:]
        return to_send.tobytes()
    
    def close(self):
        self.FILE.close()

    def isEOF(self):
        return self.EOF

class HuffmanWriter:

    # ogólne
    filename = ""
    FILE = None
    
    # Huffmanowe
    root = None

    # plikowe
    buffer = None

    def __init__(self, filename, tree):
        # otwórz plik do zapisu(w) binarnego(b)
        self.FILE = open(filename, 'wb')
        self.root = tree
        self.buffer = self.root

    def write(self, data):
        # data (bytes) -> BitArray
        data = BitArray(data)
        result = b''
        # przejdź po każdym bicie
        for bit in data.bin:
            # jeżeli napotkany node jest liściem
            if self.buffer.isLeaf():
                # dodaj jego 'char' do wyniku
                result += self.buffer.char
                # wróć do korzenia
                self.buffer = self.root
            # jeżeli bit to '1', przejdź w prawo
            if bit == '1': self.buffer = self.buffer.right 
            # jeżeli bit to '0', przejdź w lewo
            if bit == '0': self.buffer = self.buffer.left
        # zapisz bity do pliku
        self.FILE.write(result)
        # jeżeli nie dokończono jeszcze odczytu jakiegoś bajtu
        # to jest to zapisane w bufforze

    def close(self):
        self.FILE.close()


class Node:

    char = b''
    freq = 0
    left = None
    right = None
    leaf = False

    def __init__(self, char, freq, left=None, right=None):
        self.char  = char
        self.freq  = freq
        self.left  = left
        self.right = right
    
    def isLeaf(self):
        return self.leaf