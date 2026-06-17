Logs são ferramentas utilizadas por analistas para responder à incidentes, procurar por ameaças e servem como alerta e triagem. No windows, estão armazenados na pasta `C:\Windows\System32\winevt\Logs` e caracterizam logs em categorias específicas, cada um armazenado em um arquivo .evtx, um binário que não pode ser lido em um simples txt.

Para ver os logs em tempo real, basta ir na aplicação “Visualizador de Eventos”.

Os eventos windows mais valiosos para um análise são os de segurança → Successful logon (4624), fáceis de identificar porque são “barulhentos” e Failed logon (4625), facilmente confundidos porque são inconsistentes.

A estrutura de um evento 4624:
![imagem](link_imagem)

Workbook 4624/4625:
<details>
  <summary>Detectar força bruta com RDP</summary>
  1. Abrir logs de segurança e filtrar pelo ID de evento 4625 (failed login attempts)
  2. Procure por eventos de Logon tipo 3 e 10 (rede e login RDP)
    a. Para muitos sistemas modernos, o tipo de logon será 3 (porque NLA está ativo por padrão)
    b. Para sistemas antigos ou desconfigurados, o tipo de logon será 10 (porque NLA não é utilizado)
  3. Todo evento é interessante neste momento, mas o mais importante é:
    a. Muitas tentativas com admin, helpdesk e cctv (indicam password spraying)
    b. Muitas falhas de login em uma única conta, geralmente Administrador (indicam força bruta)
    c. O nome da workstation não corresponde aos padrões corporativos (ex: kali ao invés de THMPC-06)
    d. Endereço IP de origem inesperado (ex: impressora tentando conectar com o servidor windows)
</details>
<details>
  <summary>Analisar logons de RDP</summary>
  1. Abra os logs de segurança e filtre por eventos com ID 4624 (successful logins)
  2. Procure por eventos de logon do tipo 10 (logins RDP)
    a. Se NLA está ativo, todo logon está precedido por outro evento 4624 com logon do tipo 3
    b. Para conseguir um nome de workstations real, você precisa checar o evento anterior do tipo 3
  3. Prestar atenção para possíveis ataques de força bruta ou um endereço IP ou host suspeito 
  4. Se você assumir que o login é realmente malicioso, descubra o que aconteceu depois:
    c. O windows atribui um ID de logon para cada login bem sucedido (ex: 0x5D6AC)
    d. ID de logon é um identificador de sessão único. Salve-o para futura análise.
</details>

> Investigando arquivo Practice-Security.evtx
Começo procurando por indícios de um ataque de força bruta através do visualizador de tarefas, filtro pelo código de erro 4625 e encontro o endereço “10.10.53.248”, o usuário responsável pela invasão foi “Administrator” e o ID de login malicioso por RDP foi: 0x183C36D.

Após a invasão, o atacante criou o usuário “svc_sysrestore” e adicionou-se aos grupos “Backup Operators” e “Remote Desktop Users”

> Investigando arquivo Practice-Sysmon.evtx
Investigando o usuário Sarah, identifico que ela utilizou o Google Chrome para realizar o download do seguinte arquivo: “C:\Users\sarah.miller\Downloads\ckjg.exe” através da URL: “http://gettsveriff.com/bgj3/ckjg.exe” que serviu como um backdoor para o atacante tentar atacar os servidores da empresa.
> Após isso, investigando o histórico de atividade dns, o malware criou o arquivo de persistência: `C:\Users\sarah.miller\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\DeleteApp.url` que serve para se conectar ao servidor CC hospedado em `193.46.217.4:7777` que correspondia ao domínio “hkfasfsafg.click”

Após obter acesso, o atacante executou alguns comandos e consigo investigá-los através do diretório:  `C:\Users<USER>\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadline\ConsoleHost_history.txt` 

esse arquivo grava todos os comandos executados por enter no powershell.

Investigando cada usuário consigo identificar o usuário responsável pela conexão RDP → Administrator, na seguinte data: May 18, 2025.
