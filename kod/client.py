import socket, pickle
from os.path import getsize 
from config import *
from Huffman import HuffmanWriter


HOST = input("Podaj IP serwera: ")
TRANSMITTED_DATA_SIZE = 0

filename = input('Podaj nazwę dla odbieranego pliku: ')

print('Nawiązywanie połączenia.')
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print('Utworzono połączenie z {}:{}'.format(HOST,PORT))
    tree_size = int.from_bytes(s.recv(PACKET_SIZE), "big") # odbierz rozmiar drzewa
    # odbierz drzewo
    data = b''
    while len(data) != tree_size:
        data += s.recv(PACKET_SIZE)
    tree = pickle.loads(data)
    # utwórz obiekt Writera
    writer = HuffmanWriter(filename, tree)
    
    # odbierz dane
    i = 1
    while data != b'':
        print("Odbieram pakiet nr: {}".format(i), end="\r")
        i += 1
        data = s.recv(PACKET_SIZE)
        TRANSMITTED_DATA_SIZE += len(data)
        writer.write(data)
    print('')
    # zamknij plik
    writer.close()

TREE_SIZE = round(tree_size/1024, 2)
TRANSMITTED_DATA_SIZE = round(TRANSMITTED_DATA_SIZE/1024, 2)
FILE_SIZE = round(getsize(filename)/1024, 2)
COMPRESSION_LEVEL = round((1-TRANSMITTED_DATA_SIZE/FILE_SIZE)*100, 2)

print("Rozmiar drzewa:                     {}kB".format(TREE_SIZE))
print("Rozmiar przetransmitowanych danych: {}kB".format(TRANSMITTED_DATA_SIZE))
print("Rozmiar pliku po rozpakowaniu:      {}kB".format(FILE_SIZE))
print("Poziom kompresji:                   {}%".format(COMPRESSION_LEVEL))