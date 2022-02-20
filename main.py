from socket import socket, AF_INET, SOCK_STREAM
from struct import pack, unpack

PORT = 0x2BAD
SERVER = "127.0.0.1"


if __name__ == '__main__':
    with socket(AF_INET, SOCK_STREAM) as sock:
        sock.connect((SERVER, PORT))
        num = unpack('!i', sock.recv(4))[0]
        print(f"You're player {num}")
        while True:
            content = input("P:Pierre, F:Feuille, C:Ciseaux or Q:Quit : ").lower()
            if content == "q":
                break
            elif content in ['p', 'f', 'c']:
                sock.send(pack('?', content == 'p'))
                is_head = unpack('?', sock.recv(1))[0]
                score_num = unpack('!i', sock.recv(4))[0]
                print(f"It was {'HEAD' if is_head else 'TAIL'}, here are the scores :")
                for i in range(1, score_num+1):
                    score = unpack('!i', sock.recv(4))[0]
                    print(f"- Player {i}{' (you)' if i == num else ''} : {score if score>=0 else '-'}")
            else:
                print("Donnez un H ou un T s'il-vous-plait.")
        sock.close()