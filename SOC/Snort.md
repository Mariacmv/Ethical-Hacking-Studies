link para a sala: https://tryhackme.com/room/snort

É um NIDS/NIPS, ou seja, um Sistema de Detecção e Prevenção de intrusão de rede. Arquivo de configuração base do snort:

Diferença entre Intrusion Detection System (IDS) e Intrusion Prevention System (IPS): 

![arquivo_nota](https://github.com/Mariacmv/Ethical-Hacking-Studies/blob/main/SOC/imagens/configuracaoSnort.txt)
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
A documentação do snort: (https://www.snort.org/)

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

### Rodando no modo sniffer (farejador)
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

### Rodando no modo registro de pacotes
Para capturar os pacotes, o Snort necessita de permissão administrativa. Portanto, é necessário executar “sudo chown username file” e, para aplicar de forma recursiva, “sudo chown username -R directory”. 

O snort permite a captura e armazenamento do tráfego em arquivos log no formato binário através da flag -l, como em: “snort.log.1640048004”. Os resultados gerados com a flag -K ASCII são duas pastas, uma para o endereço de origem e outra para o de destino, e o conteúdo foi gerado em ASCII, ou seja, legível para humanos (não está em binário).

```
ubuntu@ip-10-64-181-40:~/Desktop/Task-Exercises/Exercise-Files/TASK-6$  sudo snort -dev -K ASCII -l.
Running in packet logging mode

        --== Initializing Snort ==--

ubuntu@ip-10-64-181-40:~/Desktop/Task-Exercises/Exercise-Files/TASK-6$ ls
10.64.181.40  10.64.78.188  PACKET_NONIP  snort.log.1640048004
```
Depois, posso ler os pacotes já capturados utilizando a flag “-r”, como em “sudo snort -r snort.log.1638459842”, também sendo possível abri no wireshark ou tcpdump.
O parâmetro “-r” também permite aplicar filtros BPF (Berkeley Packet Filter) para visualizar apenas determinados tipos de pacotes, como ICMP, TCP ou UDP. Além disso, é possível limitar o número de pacotes processados usando o parâmetro “-n”, por exemplo para analisar apenas os primeiros 10 pacotes de um log.

(https://en.wikipedia.org/wiki/Berkeley_Packet_Filter)
(https://biot.com/capstats/bpf.html)
(https://www.tcpdump.org/manpages/tcpdump.1.html)
Para ver mais informações sobre a captura e os pacotes basta utilizar a flag “-X”. A sintaxe é:
```
sudo snort -r snort.log.1640048004 -X
```

### Rodando no modo IDS/IPS
-N não gera logs → desativa a geração de logs

-D adiciona informações, assim como permite adicionar parâmetros. O programa roda em segundo plano, sendo analisável com “ps aux”:

```
root        1778  0.0  3.7 570680 151572 ?       Ssl  03:24   0:00 snort -c /etc
```
-A oferece diversos modos de alerta, como: console (que disponibiliza em tempo real), cmg (informações básicas do cabeçalho em hexadecimal e em string), full (todas as informações), fast mode (modo rápido que mostra data, endereços e payload), none (desabilita o alerta). Porém não gera log.

-A console gera alertas rápidos no console.

Snort IPS mode is activated with the -Q-- daq afpacket parameters. ????

-A cmg: providencia informações mais completas sobre o cabeçalho dos pacotes. É possível identificar a ordem de aplicação da regra: activation->dynamic->pass->drop->sdrop->reject->alert->log, além da captura de 127 pacotes todos por TCP e os pacotes que utilizaram HTTP foram 45 ao total.

-A fast: modo rápido que disponibiliza mensagens de alertas, endereços IP de origem e destino e timestamps, mas disponíveis apenas após a execução.

-A full: retorna todas as informações sobre os pacotes. Exemplo de retorno sobre os protocolos utilizados:
```
Breakdown by protocol (includes rebuilt packets):
        Eth:          477 (100.000%)
       VLAN:            0 (  0.000%)
        IP4:          477 (100.000%)
       Frag:            0 (  0.000%)
       ICMP:            0 (  0.000%)
        UDP:            2 (  0.419%)
        TCP:          411 ( 86.164%)
        IP6:            0 (  0.000%)
    IP6 Ext:            0 (  0.000%)
   IP6 Opts:            0 (  0.000%)
      Frag6:            0 (  0.000%)
      ICMP6:            0 (  0.000%)
       UDP6:            0 (  0.000%)
       TCP6:            0 (  0.000%)
     Teredo:            0 (  0.000%)
    ICMP-IP:            0 (  0.000%)
    IP4/IP4:            0 (  0.000%)
    IP4/IP6:            0 (  0.000%)
    IP6/IP4:            0 (  0.000%)
    IP6/IP6:            0 (  0.000%)
        GRE:            0 (  0.000%)
    GRE Eth:            0 (  0.000%)
   GRE VLAN:            0 (  0.000%)
    GRE IP4:            0 (  0.000%)
    GRE IP6:            0 (  0.000%)
GRE IP6 Ext:            0 (  0.000%)
   GRE PPTP:            0 (  0.000%)
    GRE ARP:            0 (  0.000%)
    GRE IPX:            0 (  0.000%)
   GRE Loop:            0 (  0.000%)
       MPLS:            0 (  0.000%)
        ARP:            0 (  0.000%)
        IPX:            0 (  0.000%)
   Eth Loop:            0 (  0.000%)
   Eth Disc:            0 (  0.000%)
   IP4 Disc:           64 ( 13.417%)
   IP6 Disc:            0 (  0.000%)
   TCP Disc:            0 (  0.000%)
   UDP Disc:            0 (  0.000%)
  ICMP Disc:            0 (  0.000%)
All Discard:           64 ( 13.417%)
      Other:            0 (  0.000%)
Bad Chk Sum:          143 ( 29.979%)
    Bad TTL:            0 (  0.000%)
     S5 G 1:            0 (  0.000%)
     S5 G 2:            1 (  0.210%)
      Total:          477
```
-A none: não gera alertas.

É possível rodar apenas as regras, sem o arquivo de configurações, principalmente para testar regras criadas. A sintaxe é:
```
sudo snort -c /etc/snort/rules/local.rules -A console
```
O modo IPS é ativado por:  -Q --daq afpacket; o módulo de aquisição de dados é feito por: -i eth0:eth1 

> Analisando o tráfego
Rodando tráfego HTTP e analisando os pacotes, percebo a presença de 2 requisições GET, utilizando o comando:
```
sudo snort -c /etc/snort/snort.conf -A full -l .
```

### Regras do snort
Seguem a seguinte estrutura:

```
ação protocolo end. IP origem porta de origem direção end. IP destino porta de destino opções
Podem ser:
drop,   TCP         any            any          <>         any              any         msg
alert,  UDP       específico    específica              específico       específico    reference
reject  ICMP                                                                             sid
                                                                                         rev
```
Para visualizar as regras, basta acessar:

```
sudo gedit /etc/snort/rules/local.rules
```
O snort começa no modo IDS, passivo, e para utilizar o modo IPS é necessário iniciar o modo in line.

As ações podem ser:

- alert → gera um alerta e o registra
- drop → bloqueia o pacote e registra
- log → log de pacotes
- reject → bloqueia o pacote, registra e termina a sessão do mesmo

O snort só filtra quatro protocolos IP, TCP, UDP e ICMP, mas é possível utilizar portas para acessar outros serviços, como SSH com a porta 22.

Exemplo:
```
alert icmp 192.168.1.56 any <> any any  (msg: "ICMP Packet From "; sid: 100001; rev:1;
```
<mark>alerta de mensagens ICMP partindo do IP 192.168.1.56</mark>
É possível filtrar por um endereço de subnet, como: 192.168.1.0/24; por um intervalo de endereços, utilizando chaves, como: [192.168.1.0/24, 10.1.1.0/24]; excluir um endereço ou uma subnet, como: !192.168.1.0/24; a porta filtrada é indicada após os endereços de origem e destino, como: any <> any 21 (para excluir uma porta basta adicionar “!” antes); para filtrar um intervalo de portas basta adicionar “:” ou “[,]”, como: 1:1024 e [21,23].

A direção do tráfego é indicado por dois operadores: -> (origem para destino) ou <>(bidirecional).

Há também 3 tipos de regras: 

- Geral:
    - msg → mensagem que aparece quando a regra é utilizada
    - sid → identificador único da regra. Pode ser: menor que 100 - regras reservadas; 100-999,999 - regras já criadas; 1.000.000 ou maior que - regras criadas pelo usuário
    - reference → informação adicional que ajuda a identificar o incidente, como um identificador CVE
    - rev → indica a quantidade de revisões que aquela regra já passou.
- Payload: ajudam a investigar payloads
    - content → indica os dados do payload, para filtrar conteúdo ASCII e/ou HEX, como: alert tcp any any <> any 80  (msg: "GET Request Found"; content:"GET"; sid: 100001; rev:1;) ou alert tcp any any <> any 80  (msg: "GET Request Found"; content:"|47 45 54|"; sid: 100001; rev:1;). É case sensitive
    - nocase → desativa case sensitive. Exemplo: alert tcp any any <> any 80  (msg: "GET Request Found"; content:"GET"; nocase; sid: 100001; rev:1;)
    - fast_pattern → é utilizado quando há vários “content” na regra para indicar qual deve ser priorizado. Exemplo: alert tcp any any <> any 80  (msg: "GET Request Found"; content:"GET"; fast_pattern; content:"www";  sid:100001; rev:1;) → nesse caso, o content procurado é “GET”
- Non-payload: utilizado para dados que não são payloads.
    - ID → filtra o ID do IP. Exemplo: alert tcp any any <> any any (msg: "ID TEST"; id:123456; sid: 100001; rev:1;)
    - flags → filtra as flags do TCP, podem ser: F (FIN), S (SYN), R (RST), P (PSH), A (ACK), U (URG). Exemplo: alert tcp any any <> any any (msg: "FLAG TEST"; flags:S;  sid: 100001; rev:1;)
    - Dsize → filtra pelo tamanho do pacote. Pode ser: dsize:min<>max; dsize:>100; dsize:<100. Exemplo: alert ip any any <> any any (msg: "SEQ TEST"; dsize:100<>300;  sid: 100001; rev:1;)
    - Sameip → verifica se o IP foi duplicado. Exemplo: alert ip any any <> any any (msg: "SAME-IP TEST";  sameip; sid: 100001; rev:1;)

> Praticando
Possuo um arquivo contendo tráfego capturado e quero descobrir o request do pacote que possui o seguinte ID "35369”. Para isso, posso utilizar o seguinte comando e crio a regra:
```
snort -c local.rules -A full -l . -r task9.pcap
alert ip any any -> any any (msg:"IP ID 35369 detectado"; id:35369; sid:1000001; rev:1;)
```
<mark>defino que as regras utilizadas serão local.rules; faço um scan completo</mark>
O retorno é:
```
#Analisando o arquivo "alert" gerado:
[**] [1:1000001:1] IP ID 35369 detectado [**]
[Priority: 0]
03/03-20:00:32.042975 192.168.121.2 -> 192.168.120.1
ICMP TTL:255 TOS:0x0 ID:35369 IpLen:20 DgmLen:40
Type:13  Code:0  ID: 7  Seq: 6  TIMESTAMP REQUEST
#descubro que o nome do request é "TIMESTAMP REQUEST"
```
O número de pacotes SYN são: 1 E verifico através da regra: 
```
alert tcp any any -> any any (msg:"Pacote SYN"; flags:S; ack:0; sid:1000001; rev:1;)
```
<mark>defino a flag S de SYN e determino que não é pra retornar pacotes ack</mark>

A saída foi:
```
[**] [1:1000001:1] Pacote SYN [**]
[Priority: 0]
03/03-20:02:09.464106 2003:51:6012:110::b15:22:60892 -> 2003:51:6012:121::2:22
TCP TTL:62 TOS:0x0 ID:0 IpLen:40 DgmLen:80
******S* Seq: 0xB82637E7  Ack: 0x0  Win: 0x7080  TcpLen: 40
TCP Options (5) => MSS: 1440 SackOK TS: 166450886 0 NOP WS: 7
```
<mark>Ou seja, um pacote retornado</mark>

O número de pacotes PSH-ACK é: 2 E verifico através da regra: 
```
alert tcp any any -> any any (msg:"Pacote PSH-ACK"; flags:P,A; sid:1000001; rev:1;)
```
E filtro o resultado com:
```
grep -o "PSH-ACK" alert | wc -l
#que retorna
216
```
Quero filtrar os pacotes UDP que possuem o mesmo endereço IP de origem e de destino, então utilizo a seguinte regra:
```
alert udp any any -> any any (msg: "Pacotes com o mesmo endereço UDP de origem e destino"; sameip; sid: 100001; rev:1;)
```
E filtro o resultado com:
```
grep -o "Pacotes com o mesmo endereço UDP de origem e destino" alert| wc -l
#que retorna
7
```
Os Módulos de Aquisição de Dados (DAQs) são bibliotecas especializadas usadas para entrada e saída de pacotes, oferecendo flexibilidade no processamento de pacotes. É possível selecionar o tipo e o modo do DAQ para diferentes finalidades.

Há seis módulos DAQ disponíveis no Snort:

- PCAP: modo padrão, conhecido como modo Sniffer.
- Afpacket: modo inline, conhecido como modo IPS.
- Ipq: modo inline no Linux usando Netfilter. Ele substitui o patch snort_inline.
- Nfq: modo inline no Linux.
- Ipfw: modo inline no OpenBSD e FreeBSD usando divert sockets, com os firewalls pf e ipfw.
- Dump: modo de teste para inline e normalização.

Os modos mais populares são o padrão (pcap) e o inline/IPS (Afpacket).
