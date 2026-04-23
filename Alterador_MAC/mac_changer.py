# Codigo que altera o endereco mac de um dispositivo


import subprocess
import optparse
import re

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface que terá o endereço MAC alterado")
    parser.add_option("-m", dest="new_mac", help="Novo endereço MAC")
    (options, arguments) = parser.parse_args()

    if not options.interface:
        #Se não tiver valor para a variável interface
        parser.error("[-] É necessário informar a interface. --help para ajuda")
    elif not options.new_mac:
        #Se não tiver valor para a variável new_mac
        parser.error("[-] É necessário informar um endereço MAC. --help para ajuda")
    return options

def change_mac(interface, new_mac):
    print("[+] Mudando MAC da interface: ",interface, "para " +new_mac)

    subprocess.call(['ifconfig', interface, 'down'])
    subprocess.call(['ifconfig', interface, 'hw', 'ether', new_mac])
    subprocess.call(['ifconfig', interface, 'up'])

def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(['ifconfig', interface], text=True)
    mac_address_search_result = re.search(r"(\w\w:){5}\w\w", ifconfig_result) #busca com regex e determino qual a variável que quero fazer a busca
    if mac_address_search_result:
        #print(mac_address_search_result.group(0)) 
        return mac_address_search_result.group(0) #printo a primeira aparição
    else:
        print("[-] Não consegui ler o endereço MAC")

options = get_arguments() #pega os argumentos passados pelo usuário
current_mac = get_current_mac(options.interface) #pega o mac atual
print("MAC atual = ", current_mac)
change_mac(options.interface, options.new_mac) #altera o mac

current_mac = get_current_mac(options.interface)
if current_mac == options.new_mac:
    print("[+] O endereço MAC foi alterado com sucesso para: ", current_mac)
else:
    print("[-] O endereço MAC não foi alterado")




#Algoritmo para conferir se o endereço foi atualizado:
# -> Executar e ler ifconfig (V)
# -> Ler o endereço MAC da saída (V)
# -> Conferir se o endereço MAC mudou e corresponde ao requisitado pelo usuário 
# -> Printar o resultado