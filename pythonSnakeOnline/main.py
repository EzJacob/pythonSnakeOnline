import sys
import threading
from snake.game import Game
from snake.get_ip_port import get_ip_and_port
from snake.menu import menu
from snake.network import Network

from snake.server import make_server


def run_server(ip_and_port):
    make_server(ip=ip_and_port[0], port=ip_and_port[1])


def main(mode, ip_and_port):
    game_num = 1
    n = p = None
    if mode == 2 or mode == 3:
        n = Network(ip=ip_and_port[0], port=ip_and_port[1])
        p = n.getP()
    game = Game(n, p, mode, game_num).game()
    while game:
        if game == -1:  # back to menu
            return -1
        game_num += 1
        game = Game(n, p, mode, game_num).game()

    return 0  # exit game


if __name__ == '__main__':
    status = 1
    ip_and_port = None
    while True:
        flag_server = False
        mode = menu()  # 0 - exit, 1 - offline game, 2 - join server, 3 - make server
        if mode == 0:
            sys.exit()
        if mode == 2 or mode == 3:
            ip_and_port = get_ip_and_port()
            if ip_and_port == -1:
                continue
        if mode == 3:
            server_thread = threading.Thread(target=run_server, args=(ip_and_port, ))
            server_thread.start()
            flag_server = True
        status = main(mode, ip_and_port)
        if flag_server:
            print("killing server...")
        if status == 0:
            sys.exit()
