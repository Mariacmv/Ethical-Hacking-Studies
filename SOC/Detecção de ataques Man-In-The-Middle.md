link para a sala: https://tryhackme.com/room/mitmdetection

Um ataque man-in-the-middle se caracteriza pela interceptação do tráfego de um endpoint em que um agente malicioso se posiciona no meio da comunicação, principalmente quando a autenticação é falha, para roubar dados ou injetar código malicioso.

O ataque é feito em dois passos: Interceptação e Manipulação. O agente de ameaça precisa explorar o sistema para encontrar vulnerabilidades ou utilizar técnicas como falsificação ARP, IP ou DNS. Para isso, ele pode utilizar sniffers de pacotes (capturá-los por wifi, principalmente os que não são criptografados), sequestro de sessões em que o agente de ameaça se passa pelo usuário legítimo, SSL stripping que consiste em retirar a criptografia de uma conexão para roubar ou alterar dados, manipular respostas DNS para redirecionar o usuário para websites maliciosos, manipular pacotes IP que parecem legítimos ou criar redes laranjas para interceptar o tráfego.

O ataque Man-in-the-Middle se encaixa principalmente nas fases de Exploração e Instalação da Cyber Kill Chain. O atacante abusa de protocolos como ARP e DNS para interceptar a comunicação, quebrando a confiança da rede e obtendo acesso ao tráfego e depois de se posicionar no meio, ele pode injetar conteúdo malicioso (malware, exploits, RATs) no fluxo de dados para comprometer a vítima.

Detectar um MITM é crítico, pois indica que o ataque já está em andamento e ainda há tempo para interromper antes que o invasor atinja o objetivo final.

Um alerta de monitoramento de rede na Acme Corp identificou padrões de tráfego incomuns, sugerindo a possibilidade de um ataque do tipo Man-in-the-Middle (MITM) dentro da rede corporativa.

Ao longo de vários dias, há indícios de que um possível atacante tenha interceptado comunicações, redirecionado conexões e capturado credenciais de usuários.

Diante desse cenário, a presente investigação assume o papel de um analista de segurança (SOC), com o objetivo de analisar os arquivos de captura de rede e logs fornecidos, buscando identificar evidências de possíveis técnicas de MITM.

# Análise Spoofing ARP

O protocolo ARP é responsável por relacionar endereços IP com endereços MAC. Um agente de ameaça envia requisições ARP para que o sistema alvo o associe a um endereço IP legítimo, geralmente um endereço gateway. Isso é possível porque ARP não possui autenticação, então qualquer dispositivo pode enviar uma solicitação ARP (is-at). 

Indicações de um envenenamento ARP: múltiplos endereços IP associados a um endereço MAC (eth.src), muitas requisições ARP sem solicitações correspondentes (comando para filtrar: arp.isgratuitous), muitas requisições ARP em um pequeno intervalo de tempo, roteamento incomum, redirecionamento para um mesmo gateway, múltiplos ARP probes que são requisições que têm o objetivo de verificar se um IP já está em uso. 

Utilizando o wireshark:

Verificando o arquivo capturado, é possível identificar muitas solicitações broadcast, tanto de solicitação de IP quanto solicitações gratuitas em intervalos consistentes o que pode indicar persistência do estado de envenenamento. Muitas solicitações e respostas para um mesmo broadcast e múltiplos ARP probes que não foram requisitados.
```
125	87020.481438	02:bb:cc:6c:c9:90	Broadcast	ARP	42	Gratuitous ARP for 192.168.10.52 (Reply)
132	93143.682694	02:aa:bb:c0:20:0d	Broadcast	ARP	42	Who has 192.168.10.16? Tell 192.168.10.19

829	661919.565327	02:bb:cc:82:0b:a4	Broadcast	ARP	42	Gratuitous ARP for 192.168.10.51 (Reply)
832	664698.994028	02:aa:bb:c0:20:0d	Broadcast	ARP	42	Who has 192.168.10.12? Tell 192.168.10.19
840	670166.509025	02:aa:bb:b2:0b:59	Broadcast	ARP	42	Who has 192.168.10.18? Tell 192.168.10.17
851	682318.488910	02:aa:bb:c0:20:0d	Broadcast	ARP	42	Gratuitous ARP for 192.168.10.19 (Reply)

796	639693.180214	02:aa:bb:d2:45:42	Broadcast	ARP	42	Who has 192.168.10.12? Tell 192.168.10.11
797	640395.712127	02:aa:bb:fc:87:62	Broadcast	ARP	42	Who has 192.168.10.10? Tell 192.168.10.12
811	647126.399575	02:bb:cc:1f:8e:68	Broadcast	ARP	42	Who has 192.168.10.15? Tell 192.168.10.54
827	660066.985591	02:aa:bb:88:b1:96	Broadcast	ARP	42	Who has 192.168.10.18? Tell 192.168.10.16
828	661298.360363	02:aa:bb:5f:9e:4e	Broadcast	ARP	42	Who has 192.168.10.13? Tell 192.168.10.14

6	161.800677	02:fe:fe:fe:55:55	02:aa:bb:88:b1:96	ARP	42	192.168.10.55 is at 02:fe:fe:fe:55:55
7	234.209841	02:aa:bb:cc:00:01	02:aa:bb:14:b6:8b	ARP	42	192.168.10.1 is at 02:aa:bb:cc:00:01
8	261.419166	02:aa:bb:cc:00:01	02:aa:bb:da:78:34	ARP	42	192.168.10.1 is at 02:aa:bb:cc:00:01
9	265.005469	02:aa:bb:cc:00:01	02:aa:bb:5f:9e:4e	ARP	42	192.168.10.1 is at 02:aa:bb:cc:00:01
```
[Um endereço muito requisitado é 192.168.10.1]
Filtrando por gateway, também é possível identificar o gateway utilizado de forma duplicada: 02:aa:bb:14:b6:8b. Investigando mais profundamente utilizando o endereço identificado é com o comando: _ws.col.info contains "192.168.10.1 is at” é possível verificar que o endereço IP duplicado é: 192.168.10.1 que utiliza tanto 02:fe:fe:fe:55:55 e 02:aa:bb:cc:00:01:
`Duplicate IP address detected for 192.168.10.1 (02:fe:fe:fe:55:55) - also in use by 02:aa:bb:cc:00:01 (frame 124)`
Quantas respostas ARP Gratuitous foram observadas para 192.168.10.1?
`arp.opcode == 2 && arp.isgratuitous == 1 && arp.dst.proto_ipv4 == 192.168.10.1
resposta: 10`
Quantos pacotes falsificados foram observados?
`arp.duplicate-address-detected || arp.duplicate-address-frame`

# Análise Spoofing DNS
Trata-se de falsificação do endereço IP associado a um domínio. Um agente de ameaça se coloca entre as requisições, identifica uma requisição de um site que ele falsificou e envia uma resposta no lugar do servidor oficial de tal site, enviando um site idêntico ao solicitado, porém associado ao ip do criminoso. Quando a vítima digita informações sensíveis, quem recebe é o servidor do atacante.

Indicações de um envenenamento DNS: múltiplas respostas a uma única solicitação; resposta vinda de um servidor com IP desconhecido (diferente de 8.8.8.8 ou o especificado); valores baixos de TTLs de pacotes; resposta DNS recebida sem que uma solicitação tenha sido feita. 

Utilizando o wireshark:

Começando a investigação, posso investigar requisições e respostas legítimas com: dns.flags.response == 1 && ip.src == 8.8.8.8, em que o endereço IP 8.8.8.8 indica o servidor da google. As respostas são todas legítimas:
![imagem_dns](SOC/imagens/imagem_dns.png)

Pesquisando por respostas que não vieram desse mesmo endereço com dns.flags.response == 1 && ip.src != 8.8.8.8, consigo identificar o endereço IP 192.168.10.55. Incluindo um domínio específico para conferir a atividade, não há nada alarmante: dns.flags.response == 1 && ip.src == 8.8.8.8 && dns.qry.name == "corp-login.acme-corp.local", o que indica a falsificação do endereço DNS já que foi redirecionado a outro endereço IP que não 8.8.8.8:
![imagem_flags](SOC/imagens/imagem_flags.png)
