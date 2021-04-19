import socket, pickle
from Huffman import HuffmanReader

HOST = '' # pusty string oznacza akceptuj na wszystkich ip/kartach sieciowych
PORT = 2137 # <- identyfikacja procesu nr z obszaru numerów wysokich

# wybierajka pliku do przesłania
reader = HuffmanReader(input("Jaki plik chcesz przesłać: "))
# z obiektu drzewa zrób string
tree_str = pickle.dumps(reader.tree)
print(len(tree_str))

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
            conn.sendall(reader.readNext())
        print('')

print("Obliczam poziom kompresji: ")