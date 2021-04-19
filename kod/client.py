import socket, pickle
from Huffman import HuffmanWriter


HOST = input("Podaj IP serwera: ")
PORT = 2137

filename = input('Podaj nazwę dla odbieranego pliku: ')

print('Nawiązywanie połączenia.')
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print('Utworzono połączenie z {}:{}'.format(HOST,PORT))
    size = int.from_bytes(s.recv(4096), "big")
    data = b''
    while len(data) != size:
        data += s.recv(4096)
    tree = pickle.loads(data)
    writer = HuffmanWriter(filename, tree)
    
    i = 1
    while data != b'':
        print("Odbieram pakiet nr: {}".format(i), end="\r")
        i += 1
        data = s.recv(4096)
        writer.write(data)
    print('')
    print("odebrano około {}kB danych".format(i*4096/8/1024))
