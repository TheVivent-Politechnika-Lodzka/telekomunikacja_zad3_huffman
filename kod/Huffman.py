

class Huffman:

    filename = ""
    FILE = None
    tree = []

    def __init__(self, filename):
        self.filename = filename
        self.FILE = open(self.filename, 'rb')

    def analyze(self):
        freq = {}
        # zaanalizuj plik bajt po bajcie
        while True:
            byte = self.FILE.read(1)
            # jeżeli koniec pliku to zakończ
            if not byte: break
            # dopisz zapisz ilość wystąpień danego byte'u
            if not byte in freq: freq[byte] = 1
            else: freq[byte] += 1
        # posortuj po ilości wystąpień
        freq = dict(sorted(freq.items(), key=lambda item: item[1]))
        # wróć na początek pliku
        self.FILE.seek(0)
        # przepisz słownik frekwencji na listę node'ów
        tmp = []
        for key in freq:
            tmp.append(Node(key, freq[key]))
        self.tree = tmp

    def createTree(self):
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

    def printTree(self):
        self.__printNodes(self.tree)

    def __printNodes(self, node):
        if node.left:
            self.__printNodes(node.left)
        if node.right:
            self.__printNodes(node.right)

        if not node.left and not node.right:
            print("char: {} -> freq: {}".format(node.char, node.freq))

class Node:

    char = b''
    freq = 0
    left = None
    right = None

    def __init__(self, char, freq, left=None, right=None):
        self.char  = char
        self.freq  = freq
        self.left  = left
        self.right = right
    