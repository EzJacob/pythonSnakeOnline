import socket
import pickle


class Network:
    def __init__(self, ip=socket.gethostname(), port=5000):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # SOCK.STREAM IS TCP SOCK.DGRAM IS UDP
        if ip == 'local':
            ip = socket.gethostname()
        self.server = str(ip)
        self.port = int(port)
        self.addr = (self.server, self.port)
        self.p = self.connect()

        print(str(ip))
        print(str(port))

    def getP(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)
            return pickle.loads(self.client.recv(2048))
        except:
            return None  # my update

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            self.client.settimeout(1)  # Set a timeout of 1 seconds
            try:
                recv = self.client.recv(2048)
                if recv:
                    return pickle.loads(recv)
                else:
                    return None
            except socket.error as e:
                # Handle network-related errors, log them, and possibly raise or return an error code.
                print(f"Socket error: {e}")
                return None
        except socket.error as e:
            print(f"Socket error: {e}")
            return None  # my update


if __name__ == "__main__":
    n = Network()
    print("network script")
