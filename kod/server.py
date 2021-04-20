import socket, pickle
from os.path import getsize 
from config import *
from Huffman import HuffmanReader

HOST = '' # pusty string oznacza akceptuj na wszystkich ip/kartach sieciowych

print("Rozmiar słowa w słowniku: {}".format(WORD_SIZE))

# wybierajka pliku do przesłania
filename = input("Jaki plik chcesz przesłać: ")
reader = HuffmanReader(filename)
# z obiektu drzewa zrób string
tree_str = pickle.dumps(reader.tree)

TRANSMITTED_DATA_SIZE = 0

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("Serwer uruchomiono na porcie: {}".format(PORT))
    conn, addr = s.accept()
    with conn:
        print('Nawiązano połączenie z: {}'.format(addr))
        conn.sendall(len(tree_str).to_bytes(8, byteorder='big'))
        while len(tree_str) > 0:
            data = tree_str[0:512]
            conn.sendall(data)
            tree_str = tree_str[512:]
        i = 1
        while not reader.isEOF():
            print("Wysyłam pakiet nr: {}".format(i), end="\r")
            i+=1
            data = reader.readNext()
            TRANSMITTED_DATA_SIZE += len(data)
            conn.sendall(data)
        print('')
        reader.close()

TRANSMITTED_DATA_SIZE = round(TRANSMITTED_DATA_SIZE/1024, 2)
FILE_SIZE = round(getsize(filename)/1024, 2)
COMPRESSION_LEVEL = round((1-TRANSMITTED_DATA_SIZE/FILE_SIZE)*100, 2)

print("Rozmiar przetransmitowanych danych: {}kB".format(TRANSMITTED_DATA_SIZE))
print("Rozmiar pliku przed kompresją:      {}kB".format(FILE_SIZE))
print("Poziom kompresji:                   {}%".format(COMPRESSION_LEVEL))