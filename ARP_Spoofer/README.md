# ARP Spoofing Study

Estudo prático sobre ARP Spoofing utilizando Python, Linux e Scapy em ambiente controlado.

## Aviso

Este projeto foi desenvolvido exclusivamente para fins educacionais e laboratoriais.

Não utilize técnicas de spoofing ou interceptação em redes sem autorização explícita.

---

## Objetivo

Compreender o funcionamento do protocolo ARP e estudar como ataques de ARP Spoofing podem ser utilizados para interceptação de tráfego em redes locais.

---

## Conceitos estudados

- ARP (Address Resolution Protocol)
- MAC Address
- ARP Tables
- ARP Requests e Responses
- ARP Spoofing
- MITM (Man-in-the-Middle)
- Packet Forwarding
- Manipulação de pacotes com Scapy
- Automação de ataques em Python

---

## Como o ataque funciona

O ataque de ARP Spoofing ocorre quando um dispositivo envia respostas ARP falsas para a vítima, associando o endereço IP do gateway ao MAC Address do atacante.

Dessa forma, o tráfego da vítima passa primeiro pelo atacante, caracterizando um ataque do tipo Man-in-the-Middle (MITM).

O protocolo ARP possui limitações de segurança:
- aceita respostas ARP sem validação
- não verifica autenticidade das respostas
- permite atualização da tabela ARP sem solicitação prévia

---

## Ferramentas utilizadas

- Python
- Scapy
- Kali Linux
- VirtualBox
- Linux Networking

---

## Estrutura do projeto

```bash
arp_spoofer.py
README.md
```

---

## Funcionalidades estudadas

### Descoberta de MAC Address

Uso de pacotes ARP para descobrir o endereço MAC associado a um IP.

```python
def get_mac(ip):
```

---

### Criação de respostas ARP falsas

Construção manual de pacotes ARP utilizando Scapy.

```python
packet = scapy.ARP(op=2)
```

---

### Envio de pacotes ARP

Envio contínuo de respostas falsas para vítima e gateway.

```python
scapy.send(packet)
```

---

### Encaminhamento de pacotes

Habilitação de IP Forwarding no Linux para permitir o fluxo de tráfego:

```bash
echo 1 > /proc/sys/net/ipv4/ip_forward
```

---

### Tratamento de exceções

Uso de `try-except` para interromper o programa corretamente.

```python
except KeyboardInterrupt:
```

---

## Observações

Este projeto faz parte dos meus estudos em:
- redes
- Linux
- segurança ofensiva
- manipulação de pacotes
- automação em Python

O código e as anotações representam um laboratório de aprendizado em andamento.
