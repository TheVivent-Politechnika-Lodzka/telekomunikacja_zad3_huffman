import sys
from Huffman import Huffman

huff = Huffman(input("Podaj nazwę pliku: "))

huff.analyze()
huff.createTree()
# print(huff.tree)
# huff.printTree()

print(sys.getsizeof(huff.tree))