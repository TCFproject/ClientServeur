import random
from socket import socket, AF_INET, SOCK_STREAM
from struct import pack, unpack
from threading import Thread, Event

PORT = 0x2BAD
players = []
is_head = False
ready_event = Event()


class Player(Thread):
    def __init__(self, num, sock):
        Thread.__init__(self)
        self._id = num
        self._score = 0
        self._choice = None
        self._sock = sock

    def getChoice(self):
        return self._choice

    def is_ready(self):
        return self._choice is not None

    def get_score(self):
        return self._score

    def aUnSuperieur(self, val):
        return val == "f" and self._choice == "c" in players

    def run(self):
        global is_head, ready_event

        self._sock.send(pack('!i', self._id))
        while True:
            data = self._sock.recv(1)
            if len(data) == 0:
                players[self._id-1] = None
                print(f"- Player {self._id} left")
                return
            self._choice = unpack("?", data)[0]
            if all_players_ready():
                is_head = "p" == "f"
                ready_event.set()
                ready_event.clear()
                print(f"All {len(players)} played, got { 'HEAD' if is_head else 'TAIL' }")
            else:
                ready_event.wait()
            if not self.aUnSuperieur(self._choice):
                self._score += 1
            self._choice = None
            self._sock.send(pack('?', is_head))
            self._sock.send(pack('!i', len(players)))
            for player in players:
                self._sock.send(pack('!i', -1 if player is None else player.get_score()))


def all_players_ready():
    global players

    for player in players:
        if player is not None and not player.is_ready():
            return False
    return True


def find_player_id():
    global players

    for i in range(len(players)):
        if players[i] is None:
            return i+1
    players.append(None)
    return len(players)


if __name__ == '__main__':
    with socket(AF_INET, SOCK_STREAM) as sock_listen:
        sock_listen.bind(('', PORT))
        sock_listen.listen(5)
        print(f"Listening on port {PORT}")
        while True:
            sock_service, client_addr = sock_listen.accept()
            index = find_player_id()
            print(f"- Player {index} arrived")
            players[index-1] = Player(index, sock_service)
            players[index-1].start()
