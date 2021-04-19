import socket

HOST = 'localhost'
PORT = 2137

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected with: {}'.format(addr))
        while True:
            data = conn.recv(1024)
            print(repr(data))
            if not data:
                break
            conn.sendall(data)