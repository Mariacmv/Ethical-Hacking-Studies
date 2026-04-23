#Código que scaneia uma rede

#Algoritmo escolhido no curso:
#   1º: Criar uma requisição ARP direcionada a broadcast solicitando um IP (v)
#   2º: Enviar o pacote e receber a resposta (v)
#   3º: Parse the response - extrair informação de uma estrutura (v)
#   4º: Mostrar o resultado(v)
#   5º: Criando uma lista de dicionários para melhorar a visualização da saída

import argparse
import scapy.all as scapy 

#adiciona essa função para que o usuário passe o ip desejado de forma mais fácil, porém utilizando o módulo argparse, pois é mais recente
def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--target', dest="target", help="IP alvo/ Faixa de IP")
    options = parser.parse_args()
    return options

def scan(ip):
    arp_request = scapy.ARP(pdst=ip)  
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff") 
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    clients_list = []

    for item in answered_list:
        client_dict = {'ip':item[1].psrc, 'mac':item[1].hwsrc} 
        clients_list.append(client_dict)  
    return clients_list

def print_result(results_list):
    print("--------------------------------------------------------")
    print("IP\t\t\tMAC ADDRESS")
    print("--------------------------------------------------------")
    for client in results_list:
        print(client['ip'] + '\t\t' + client['mac'])

options = get_arguments()
scan_result = scan(options.target)
print_result(scan_result)