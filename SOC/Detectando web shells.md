Empresas costumam armazenar arquivos em bancos de dados, mas também em diretórios de servidores web e web shells costumam ficar em: /var/www/html (apache) e /usr/share/nginx/html (nginx). Outros diretórios que podem ser explorados são: /uploads/, /images/, /admin/ e /temp/. Web shells são programas maliciosos que visam web servidores para executar comandos remotamente.

É importante procurar por arquivos fora do normal, com nomes estranhos e extensões duplas (ex: image.php.jpg) que servem para esconder a real extensão, como .php ou .jsp. 

Comandos interessantes para buscar informações incluem: find com “newerct” (procurar entre duas datas específicas) e grep com eval para procurar funções específicas. Exemplos:

```
user@tryhackme$ find /var/www -type f -name "*.php" -newerct "2025-07-01" ! -newerct "2025-08-01"
/var/www/html/uploads/awebshell.php          // Web shell created between the dates above.

user@tryhackme$ grep -r "eval(" wp-content
/wp-content/uploads/awebshell2.php :eval(b64_dd($['cmd']));  // Web shell containing eval(
```
Além da análise de logs de sistema, também é interessante analisar logs de rede com wireshark, principalmente. Alguns filtros mais utilizados são: http.request.method == “METHOD”; http.request.uri contains “.php”; http.user_agent

Comandos wireshark: ![https://www.wireshark.org/docs/dfref/h/http.html]
> Investigando
Recebi logs de um servidor apache, localizados em: **/var/log/apache2/access.log** . São logs de rede de acesso a servidores. Pesquisando com **curl** identifico algumas requisições e respostas, como:
```
//redirecionamento para a página de adm para reautenticar com agentes suspeitos "ashadyagent/1.1"
203.0.113.66 - - [17/Jul/2025:05:22:06 +0000] "GET /wordpress/wp-login.php?redirect_to=http%3A%2F%2F192.168.1.9%2Fwordpress%2Fwp-admin%2F&reauth=1 HTTP/1.1" 200 1804 "ashadyagent/1.1"
//após isso vários gets da página wordpress com agentes suspeitos "ashadyagent/1.1"
203.0.113.66 - - [17/Jul/2025:05:22:25 +0000] "GET /wordpress/wp-login.php?redirect_to=http%3A%2F%2F192.168.1.9%2Fwordpress%2Fwp-admin%2F&reauth=1 HTTP/1.1" 200 1804 "ashadyagent/1.1"
203.0.113.66 - - [17/Jul/2025:05:22:26 +0000] "GET /wordpress/wp-admin/ajax.php HTTP/1.1" 404 273 "ashadyagent/1.1"
//um post para a página de uploads 
203.0.113.66 - - [17/Jul/2025:06:09:27 +0000] "POST /wordpress/wp-content/uploads/upload_form.php?file=shadyshell.php HTTP/1.1" 200 204 "curl/8.14.1"
//vários gets para o arquivo shadyshell.php
192.168.1.10 - - [17/Jul/2025:06:16:38 +0000] "GET /wordpress/wp-content/uploads/shadyshell.php?cmd=cat%20/etc/passwd HTTP/1.1" 200 2174 "curl/8.14.1"
203.0.113.66 - - [17/Jul/2025:06:18:39 +0000] "GET /wordpress/wp-content/uploads/shadyshell.php?cmd=cat%20/etc/passwd HTTP/1.1" 200 2174 "curl/8.14.1"
203.0.113.66 - - [17/Jul/2025:06:14:55 +0000] "GET /wordpress/wp-content/uploads/shadyshell.php?cmd=whoami HTTP/1.1" 200 10 "curl/8.14.1"
```
(O endereço IP suspeito é 203.0.113.66, agente suspeito é “ashadyagent/1.1” e o upload suspeito é shadyshell.php, o upload do web shell é feito pelo arquivo “upload_form.php”, o primeiro comando que o atacante roda após o acesso é “whoami”, além de fazer o download do arquivo linpeas.sh)
