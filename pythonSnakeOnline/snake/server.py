import socket
from _thread import *
from snake.player import Player
import pickle


exited_thread_flag = False
players = [Player(), Player()]


def make_server(ip=socket.gethostname(), port=5000):
    if ip == 'local':
        ip = socket.gethostname()
    server = str(ip)
    port = int(port)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.bind((server, port))
    except socket.error as e:
        str(e)

    s.listen(2)
    print("Waiting for a connection, Server Started")
    print('server:' + str(server))
    print('port:' + str(port))

    global players
    p1 = players[0]
    p2 = players[1]
    p1.player_number = 1
    p2.player_number = 2

    currentPlayer = 0

    global exited_thread_flag
    exited_thread_flag = False

    while True:
        try:
            conn, addr = s.accept()
        except Exception as e:
            print(f"s.accept failed: {str(e)}")
            print('exiting make server function')
            return

        print("Connected to:", addr)

        if currentPlayer == 0:
            p1.connected = True
        if currentPlayer == 1:
            p2.connected = True

        start_new_thread(threaded_client, (conn, currentPlayer, s))
        currentPlayer += 1
        print("current player: " + str(currentPlayer))


def threaded_client(conn, player, s):
    global players
    global exited_thread_flag
    conn.send(pickle.dumps(players[player]))
    reply = ""
    while True:
        if exited_thread_flag:
            print("exited_thread_flag")
            break
        try:
            data = pickle.loads(conn.recv(2048))
            players[player] = data

            if not data:
                print("Disconnected")
                break
            else:
                if player == 1:
                    reply = players[0]
                else:
                    reply = players[1]

                print("Received: ", data)
                print("Sending : ", reply)

            conn.sendall(pickle.dumps(reply))
        except:
            print("Exception, exiting 'threaded_client' function")
            break

    players[player].connected = False
    print(f"player: {player + 1} Lost connection\n")
    conn.close()
    # player -= 1
    s.close()
    exited_thread_flag = True


if __name__ == "__main__":
    make_server()
    print("server script")
