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
    size = int.from_bytes(s.recv(PACKET_SIZE), "big")
    data = b''
    while len(data) != size:
        data += s.recv(PACKET_SIZE)
    tree = pickle.loads(data)
    writer = HuffmanWriter(filename, tree)
    
    i = 1
    while data != b'':
        print("Odbieram pakiet nr: {}".format(i), end="\r")
        i += 1
        data = s.recv(PACKET_SIZE)
        TRANSMITTED_DATA_SIZE += len(data)
        writer.write(data)
    print('')
    writer.close()

TRANSMITTED_DATA_SIZE = round(TRANSMITTED_DATA_SIZE/1024, 2)
FILE_SIZE = round(getsize(filename)/1024, 2)
COMPRESSION_LEVEL = round((1-TRANSMITTED_DATA_SIZE/FILE_SIZE)*100, 2)

print("Rozmiar przetransmitowanych danych: {}kB".format(TRANSMITTED_DATA_SIZE))
print("Rozmiar pliku po rozpakowaniu:      {}kB".format(FILE_SIZE))
print("Poziom kompresji:                   {}%".format(COMPRESSION_LEVEL))