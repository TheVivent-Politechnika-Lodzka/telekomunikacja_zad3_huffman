from Huffman import HuffmanReader
from Huffman import HuffmanWriter


read = HuffmanReader(input("Podaj nazwę pliku do odczytu: "))
write = HuffmanWriter(input("Podaj nazwę pliku do zapisu: "), read.tree)
read.printWeight()

while not read.isEOF():
    write.write(read.readNext())



# print(sys.getsizeof(huff.tree))