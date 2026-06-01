link para a sala: https://tryhackme.com/room/dataexfildetection

É o roubo de dados de uma organização para fora dela, sem autorização. Pode acontecer por funcionário mal-intencionado ou por invasores (malware, credenciais roubadas, etc.)

Os motivos para a o roubo de dados podem ser vários como: benefício monetário (para venda de dados ou fraude), espionagem (obtenção de segredos), extorsão (roubo e ameaçar vazar), sabotagem (formas de prejudicar uma empresa) e preparação para ataques futuros.

Os agentes de ameaça alcançam isso através do protocolo HTTP e HTTPS para esconder o tráfego, para enviar comandos através de ataques C2, em uploads para nuvens, até mesmo em ataques ransomware antes de criptografar os dados. 

O ataque inicia com a escolha dos dados alvos, preparação de estratégias e ferramentas. Durante o ataque, ocorre o roubo dos dados que é a transferência via rede, tudo coordenado via C2.

As principais técnicas utilizadas por agentes de ameaça incluem transferência por rede, em que um atacante utiliza meios comuns como HTTPS - que é criptografada o que dificulta a identificação, FTP, SFTP, SCP - que são transferências comuns, porém suspeitas quando ocorrem para fora da rede e DNS tunelling em que o agente de ameaça esconde dados dentro das requisições DNS. Transferência por host, como por processos comuns de shells para baixar os dados com wget, curl, entre outros; processos de compactação de arquivos com zip/rar a fim de não chamar atenção para quantidade de arquivos e, em outros casos, a utilização de mídias removíveis como USB. 

Atualmente um dos meios mais utilizados pelos atacantes é a nuvem já que está em uso em praticamente todas as organizações. Dessa forma, é mais difícil ser identificado com base no comportamento dos usuários, por exemplo. Outra técnica bastante utilizada é a ocultação por encoding, transformando dados em texto normal, por exemplo, esteganografia, uma técnica de ocultar dados em imagens e vídeos, além de transferir dados de forma lenta e em poucas quantidades. Por fim, ferramentas legítimas utilizadas dentro de uma organização em que um comportamento pode não ser considerado suspeito já que pode acontecer no dia-a-dia de uma empresa.

Portanto é necessário questionar a origem dos dados, qual o destino, o volume transferido e a frequência e se é válida a transferência daqueles dados naquele momento e para tal destino.

#Análise de tranferência por DNS
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

#Análise de tranferência por FTP
