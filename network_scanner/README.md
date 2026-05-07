# Network Scanner Study

Estudo prático de descoberta de dispositivos em rede local utilizando ARP Requests e Python.

## Aviso

Projeto desenvolvido exclusivamente para fins educacionais e laboratoriais.

Não utilize ferramentas de varredura em redes sem autorização.

---

## Objetivo

Compreender o funcionamento de descoberta de hosts em redes locais utilizando o protocolo ARP.

O projeto explora:
- ARP Requests
- Broadcast
- Descoberta de dispositivos
- Manipulação de pacotes
- Parsing de respostas
- Estruturas de dados em Python

---

## Conceitos estudados

- ARP
- Broadcast
- MAC Address
- Network Scanning
- Packet Manipulation
- Scapy
- Parsing
- Python Networking

---

## Tecnologias utilizadas

- Python
- Scapy
- Linux
- argparse

---

## Estrutura do projeto

```bash
network_scanner.py
README.md
```

---

## Funcionamento

O scanner:
1. cria uma requisição ARP
2. envia para broadcast
3. recebe respostas dos hosts ativos
4. extrai IP e MAC Address
5. exibe os resultados formatados

---

## Criação da requisição ARP

```python
arp_request = scapy.ARP(pdst=ip)
```

---

## Criação do pacote broadcast

```python
broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
```

---

## Envio e recebimento dos pacotes

```python
answered_list = scapy.srp(
    arp_request_broadcast,
    timeout=1,
    verbose=False
)[0]
```

---

## Parsing das respostas

Extração de IP e MAC Address dos dispositivos encontrados.

```python
client_dict = {
    'ip': item[1].psrc,
    'mac': item[1].hwsrc
}
```

---

## Exemplo de uso

```bash
python network_scanner.py -t 192.168.0.1/24
```

---

## Exemplo de saída

```bash
IP                      MAC ADDRESS
192.168.0.1             xx:xx:xx:xx:xx:xx
192.168.0.15            xx:xx:xx:xx:xx:xx
```

---

## Observações

Este projeto faz parte dos meus estudos em:
- redes
- segurança ofensiva
- Linux
- automação
- manipulação de pacotes
- Python

O código representa um laboratório de aprendizado em andamento.
