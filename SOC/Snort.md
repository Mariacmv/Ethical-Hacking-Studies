link para a sala: https://tryhackme.com/room/snort

É um NIDS/NIPS, ou seja, um Sistema de Detecção e Prevenção de intrusão de rede. Arquivo de configuração base do snort:

Diferença entre Intrusion Detection System (IDS) e Intrusion Prevention System (IPS): 
![arquivo_nota]()
- IDS é um sistema que monitora e detecta um sistema para identificar comportamentos anormais e violações de políticas que são determinados por uma lista de alertas.
    - Network Intrusion Detection System (NIDS): é um sistema de detecção baseado na rede, ou seja, monitora a rede como um todo.
    - Host-based Intrusion Detection System (HIDS): é um sistema de detecção baseado em cada host de uma rede.
- IPS é um sistema que monitora um sistema e age contra comportamentos suspeitos, seja terminando ou prevenindo os processos.
    - Network Intrusion Prevention System (NIPS): é um sistema especializado em monitorar e agir em redes como um todo, não apenas detecta, como também prevê o comportamento e toma medidas de proteção.
    - Network Behaviour Analysis (NBA): é um sistema que monitora partes do sistema e também encerra ações suspeitas.
        - A diferença entre NIPS e NBA é que esse precisa aprender o comportamento do sistema durante a execução a fim de reconhecer atividades suspeitas e atividades normais, esse período é determinado como “baselining”.
    - Wireless Intrusion Prevention System (WIPS): é um sistema que monitora e age contra ações em uma rede sem fio.
    - Host-based Intrusion Prevention System (HIPS): é similar ao HIDS, com a diferença de que quando uma assinatura é identificada, é capaz de agir contra eliminando processos anômalos.

As principais técnicas de prevenção com IDS e IPS são: baseado em assinatura (trata-se de identificar atividades com base em comportamentos específicos, padrões que concordam com regras preestabelecidas), baseado em comportamento (trata-se de identificar comportamentos anômalos não identificados previamente, contribuindo para a lista de regras) e baseado em políticas (identificação baseado em configurações e políticas).
A documentação do snort:![link](https://www.snort.org/)

É um NIDS/NIPS, ou seja, baseado em rede que pode analisar tráfego ao vivo e gerar alertas, detectar ataques, gerar log de pacotes, analisar protocolos, suporte para módulos e plugins. Pode operar em três modos:

1. sniffer: monitora e gerar logs de tráfego ao vivo.
2. registro de pacotes: registra todos os pacotes IP gerados na rede (tanto inbound e outbound).
3. NIDS e NIPS
Investigando com Snort:

Primeiro, verifico se snort está instalado com “snort -V” o que retorna:
```
ubuntu@ip-10-64-181-40:~$ snort -V

   ,,_     -*> Snort! <*-
  o"  )~   Version 2.9.7.0 GRE (Build 149) 
   ''''    By Martin Roesch & The Snort Team: http://www.snort.org/contact#team
           Copyright (C) 2014 Cisco and/or its affiliates. All rights reserved.
           Copyright (C) 1998-2013 Sourcefire, Inc., et al.
           Using libpcap version 1.9.1 (with TPACKET_V3)
           Using PCRE version: 8.39 2016-06-14
           Using ZLIB version: 1.2.11
```

Depois, confiro as configurações utilizando as flags -c que identifica o arquivo de configuração e -T que o testa.
```
ubuntu@ip-10-64-181-40:/etc/snort$ ls
classification.config  community-sid-msg.map  gen-msg.map  reference.config  rules  snort.conf  snort.debian.conf  snortv2.conf  threshold.conf  unicode.map
ubuntu@ip-10-64-181-40:~$ sudo snort -c /etc/snort/snort.conf -T
Running in Test mode

        --== Initializing Snort ==--
...

Snort successfully validated the configuration!
Snort exiting
```
<mark>Posso prevenir a saída do banner com o parâmetro -q</mark>
> O teste previne uma execução falha.

###Rodando no modo sniffer (farejador)
Analisando o tráfego gerado, consigo filtrar tráfego TCP/IP com “-v”, determinando também a interface monitorada com “-i”:
```
Commencing packet processing (pid=2075)
WARNING: No preprocessors configured for policy 0.
03/31-11:51:44.367959 172.31.64.152:9092 -> 10.64.181.40:58778
TCP TTL:252 TOS:0x0 ID:41044 IpLen:20 DgmLen:52 DF
***A**** Seq: 0xD97F4039  Ack: 0xDF95335C  Win: 0xB686  TcpLen: 32
TCP Options (3) => NOP NOP TS: 3738695489 955992298 
=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+

WARNING: No preprocessors configured for policy 0.
03/31-11:51:44.375122 10.64.78.188:58992 -> 10.64.181.40:80
TCP TTL:127 TOS:0x0 ID:32028 IpLen:20 DgmLen:70 DF
***AP*** Seq: 0x740A139B  Ack: 0xE9CF7638  Win: 0x12E9  TcpLen: 32
TCP Options (3) => NOP NOP TS: 3908850729 2377651180 
```
<mark>Posso concluir que o tráfego vem de 10.64.78.188 na porta TCP 58992 e 172.31.64.152 na porta TCP/UDP 9092 que indica serviço KAFKA - mensagens de streaming Também há tráfego HTTP interno - 10.64.181.40:80 com a flag: ***AP*** (ACK + PUSH) o que indica que o usuário está enviando dados na sessão TCP</mark>

Encontrei também a ordem de aplicação das regras:
```Rule application order: activation->dynamic->pass->drop->sdrop->reject->alert->log```

De 1091 pacotes, 967 pacotes foram analisados:
```
Packet I/O Totals:
   Received:         1091
   Analyzed:          967 ( 88.634%)
    Dropped:            0 (  0.000%)
   Filtered:            0 (  0.000%)
Outstanding:          124 ( 11.366%)
   Injected:            0
#todos por IPV4
IP4:          967 (100.000%)
#a maioria por TCP
TCP:          790 ( 81.696%)
```
<mark>Identifico os servicos: internal-k8s-badrserv-badrserv-8675e7e1fd-425959980 e eu-west-1.elb.amazonaws.com que indicam uma possível consulta DNS - 10.64.0.2:53 a um serviço kubernetes via AWS-ELB na região: eu-west-1</mark>

Analisando também o cabeçalho do pacote com -e (combinando o conteúdo do payload -d e header -e):
```
03/31-12:22:07.076219 0A:FF:C9:24:FF:F9 -> 0A:FF:F4:9A:43:41 type:0x800 len:0x62
10.64.78.188:58992 -> 10.64.181.40:80 TCP TTL:127 TOS:0x0 ID:34640 IpLen:20 DgmLen:84 DF
***AP*** Seq: 0x74175BCB  Ack: 0xF8FFB916  Win: 0x12E9  TcpLen: 32
TCP Options (3) => NOP NOP TS: 3910673448 2379473908 
82 8A 40 55 2B 6C B8 55 2B 6C 40 55 2B 6D 41 54  ..@U+l.U+l@U+mAT
82 8A EC 21 D3 32 14 21 D3 32 EC 21 D3 33 ED 20  ...!.2.!.2.!.3.
```
<mark>...!.2.!.2.!.3. ..@U+l.U+l@U+mAT indicam conteúdo binário Também há tráfego local por causa da comunicação via MAC: 0A:FF:C9:24:FF:F9 -> 0A:FF:F4:9A:43:41</mark>

Analisando com -X:
```
03/31-12:27:30.558857 10.64.181.40:43720 -> 172.31.65.81:443
TCP TTL:64 TOS:0x0 ID:51599 IpLen:20 DgmLen:60 DF
******S* Seq: 0xD7B8FFBC  Ack: 0x0  Win: 0xF507  TcpLen: 40
TCP Options (5) => MSS: 8961 SackOK TS: 2198084435 0 NOP WS: 7 
0x0000: 0A FF C9 24 FF F9 0A FF F4 9A 43 41 08 00 45 00  ...$......CA..E.
0x0010: 00 3C C9 8F 40 00 40 06 C4 53 0A 40 B5 28 AC 1F  .<..@.@..S.@.(..
0x0020: 41 51 AA C8 01 BB D7 B8 FF BC 00 00 00 00 A0 02  AQ..............
0x0030: F5 07 AD 07 00 00 02 04 23 01 04 02 08 0A 83 04  ........#.......
0x0040: 1B 53 00 00 00 00 01 03 03 07                    .S........
```
<mark>Identifico uma conexão SYN através de: ******S* e Ack: 0x0, ou seja, a conexão ainda não foi estabelecida. 
host 10.64.181.40 iniciou conexão - destino 172.31.65.81 - porta 443 (HTTPS) - 
primeiro pacote do handshake TCP (SYN) - 
conexão provavelmente com serviço HTTPS dentro de infraestrutura cloud</mark>

#### Conclusão:

- O Snort foi executado em **modo sniffer**, capturando pacotes TCP/IP na interface monitorada.
- O tráfego analisado é predominantemente**TCP (≈81%)**, indicando comunicação típica de aplicações web e serviços de rede.
- Foram observadas**comunicações HTTP internas** na porta 80 entre hosts da rede privada.
- Também foi identificada**resolução DNS**relacionada a serviços hospedados na **AWS (Elastic Load Balancer) associados a um cluster Kubernetes**
- Foi detectada a**inicialização de conexões HTTPS (porta 443)** pelo host monitorado, indicando comunicação com serviços externos ou cloud.
- O tráfego capturado inclui**dados binários no payload**, possivelmente relacionados a protocolos de aplicação ou dados criptografados.
- Nenhuma perda de pacotes foi observada durante a captura.
