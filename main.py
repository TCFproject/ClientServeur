import socket

def deroulement(d):
    if d == 0:
        print("Pierre")
    elif d == 1:
        print("papier")
    elif d == 2:
        print("ciseaux")

def request(verb, url, value):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect(("127.0.0.1", 5000))
        sock.send(f"{verb} /{url} HTTP/1.1\r\n".encode())
        sock.send("Content-Type: text/plain\r\n".encode())
        sock.send(f"Content-Length: {len(value)}\r\n\r\n".encode())
        sock.send(f"{value}\r\n".encode())
        while True:
            s = sock.recv(4096).decode('utf-8')
            if s == '':
                break;
            deroulement(s)
        sock.close()

if __name__ == '__main__':
    while True:
        content = input("Key/Text (Q to quit) :")
        if content == ("Q" or "q"):
            break
        else:
            items = content.split('/')
            if len(items) > 1:
                request("POST", items[0], items[1])
                request("GET", "", "")
