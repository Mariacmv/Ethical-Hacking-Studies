Um ataque DDoS (Distributed Denial of Service) é utilizado para causar perda de disponibilidade de um site, enviando milhares de requisições a um servidor de modo que ele não consiga processar todas. Pode ser lançado em qualquer camada do modelo OSI mas a camada mais comum é aplicação. Quando apenas uma máquina é utilizada para realizar o ataque então chama-se apenas DoS (Denial of Service). Tipos de ataques DoS:

- Slowloris → muitas requisições HTTP para esgotar o servidor.
- Inundação HTTP → muitas requisições HTTP para sobrecarregar o servidor.
- Ignorar cache (cache bypass) → ignorar servidores CDN para entrar em contato com o servidor original diretamente.
- Query grande → força o servidor a processar queries muito grandes.
- Abuso de logins e formulários → sobrecarregar formulários com lógica de autenticação extrapolada e muitas requisições de redefinição de senha.
- Abuso de validação de input defeituosa → explorar inputs com pouca validação.
Esses ataques podem causar diversos problemas a um dono de negócio já que muitos dependem da disponibilidade total de um serviço. Os motivos para um atacante podem ir desde causar danos financeiros, com propósitos sociais, distração para que efetuem outros ataques, competição entre empresas até danos à reputação.
> Investigando
> 
<mark>access.log - arquivo</mark>

Observando as requisições feitas no arquivo access.log, noto 93 requisições repetidas à página de login:

<details>
  <summary>/login</summary>
ubuntu@tryhackme:~/Desktop$ grep "/login" access.log
192.168.1.10 - - [31/Aug/2025:01:57:44 +0000] "GET /login/ HTTP/1.1" 200 293 "-" "Mozilla/5.0 (X11; Linux x86_64; rv:128.0)
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 503 267 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 503 267 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 503 267 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 503 267 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 503 267 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 503 267 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 503 267 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 503 267 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 503 267 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 503 267 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 503 267 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 503 267 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 503 267 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 503 267 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 503 267 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 503 267 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 503 267 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 503 267 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 503 267 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 503 267 "-" "curl/7.88.1"
</details>

Muitas requisições com curl (até mesmo Python-urllib):

<details>
  <summary>Curl</summary>
  ubuntu@tryhackme:~/Desktop$ grep "curl" access.log
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 503 267 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 503 267 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 503 267 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 503 267 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 503 267 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 503 267 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 503 267 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 503 267 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 503 267 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 503 267 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 503 267 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 503 267 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 503 267 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 503 267 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 503 267 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 503 267 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 503 267 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 503 267 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 503 267 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 503 267 "-" "curl/7.88.1"
</details>

Observo 3 endereços IP utilizados: 192.168.1.5, 192.168.1.10, 203.12.23.195. Os dois primeiros pertencem à faixa de endereços IP privados (192.168.0.0/16), normalmente utilizada em redes locais (LAN). Já o endereço 203.12.23.195 é um IP público, roteável na Internet e potencialmente associado a um dispositivo ou servidor acessível externamente.

Muitas requisições em um período muito curto de tempo:

```
03.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 200 519 "-" "curl/7.88.1"
```

(Todas feitas no mesmo segundo)

Muitas requisições com erro de servidor 500-511, indicando que o servidor está com dificuldades o que pode indicar um possível ataque.

<details>
  <summary>Código 503</summary>
  203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 503 267 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 503 267 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 503 267 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 503 267 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 503 267 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 503 267 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 503 267 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 503 267 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 503 267 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 503 267 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 503 267 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 503 267 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 503 267 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 503 267 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 503 267 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 503 267 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 503 267 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 503 267 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 503 267 "-" "curl/7.88.1"
203.12.23.195 - - [31/Aug/2025:01:59:08 +0000] "GET /login HTTP/1.1" 503 267 "-" "curl/7.88.1"
192.168.1.10 - - [31/Aug/2025:01:59:29 +0000] "GET /products/ HTTP/1.1" 503 308 "-" "Mozilla/5.0 (X11; Linux x86_64; rv:128.0)
192.168.1.10 - - [31/Aug/2025:02:00:07 +0000] "GET /products/seat HTTP/1.1" 503 247 "-" "Mozilla/5.0 (X11; Linux x86_64; rv:128.0)
192.168.1.10 - - [31/Aug/2025:02:00:16 +0000] "GET /products/products HTTP/1.1" 503 491 "-" "Mozilla/5.0 (X11; Linux x86_64; rv:128.0)
192.168.1.10 - - [31/Aug/2025:02:00:23 +0000] "GET /products/handle HTTP/1.1" 503 247 "-" "Mozilla/5.0 (X11; Linux x86_64; rv:128.0)
192.168.1.5 - - [31/Aug/2025:02:01:05 +0000] "GET /support/ HTTP/1.1" 503 247 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64)
192.168.1.5 - - [31/Aug/2025:02:01:36 +0000] "GET /support/shipping HTTP/1.1" 503 247 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64)
192.168.1.5 - - [31/Aug/2025:02:01:39 +0000] "GET /support/help HTTP/1.1" 503 246 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64)
192.168.1.5 - - [31/Aug/2025:02:03:28 +0000] "GET /products/ HTTP/1.1" 503 248 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64)
192.168.1.10 - - [31/Aug/2025:02:03:56 +0000] "GET /products/access.log HTTP/1.1" 503 494 "-" "Mozilla/5.0 (X11; Linux x86_64; rv:128.0)
</details>

Também é interessante investigar lógicas abusadoras em requisições nas próprias URL, como: **`GET /products?limit=999999`**

Atacantes irão focar em páginas que vão explorar mais do servidor como páginas de login porque as requisições requerem buscas mais custosas no sistema, como banco de dados. Os diretórios mais focados são: /login, /search, /api, /register, /signup, /contact, /feedback, /cart, /checkout

>  Investigando com Splunk
1 - Qual foi a `uri` solicitada com mais frequência? `Acessando o filtro “uri” descubro que a página mais solicitada foi /search`

2 - Qual `clientip` fez o maior número de solicitações para a `uri` alvo? `Filtrando pela uri=”/search” e investigando o ip no filtro “clientip” descubro que o ip que fez mais solicitações foi “203.0.113.7”`

3 - Quantos endereços IP faziam parte da botnet que atacou seu site? `Utilizando o mesmo filtro da pergunta de cima descubro que 60 endereços fizeram parte do ataque.`

4 - Qual useragent foi mais utilizado no ataque? `Analisando o filtro useragent, descubro “Java/1.8.0_181”`

5 - Utilizando o comando timechart para visualizar as requisições, qual foi o maior número de requisições feitas por segundo durante o ataque? `Utilizando o comando `index="main" | timechart span=1s count by request` descubro 207 requisições.`

6 - Qual clientip legítimo (não criminoso) recebeu a primeira resposta 503 pós-ataque? `Utilizando filtro status=503 e a ferramenta de tempo do splunk descubro que o primeiro endereço que recebeu a primeira resposta 503 foi “10.10.0.27”.`

Atacantes exploram falhas para sobrecarregar sistemas, mas existem diversas estratégias para proteger sites e aplicações.

### Defesa em Nível de Aplicação
#### Práticas de Desenvolvimento Seguro
- O código deve ser seguro desde o início.
- Campos de entrada (formulários, buscas) precisam validar dados.
- Sem validação, atacantes podem enviar requisições complexas para sobrecarregar o sistema.

Exemplo: limitar tamanho ou formato de entradas evita abusos.

Desafios: servem para diferenciar humanos de bots.

**Tipos:**

- **CAPTCHA**: usuário resolve um teste simples.
- **Desafios em JavaScript**: verificações automáticas invisíveis ao usuário.

Benefício: bloqueiam ou reduzem tráfego automatizado malicioso.

### Defesa de Rede e Infraestrutura
#### CDN (Content Delivery Network)
- Distribui conteúdo em servidores próximos ao usuário.
- Reduz carga do servidor principal.
- Ajuda a absorver ataques DDoS.

**Vantagens:**

- Cache de conteúdo
- Balanceamento de carga
- Redirecionamento de tráfego
- Monitoramento detalhado (origem, volume, padrões)

Exemplo: ataques grandes podem ser absorvidos pela CDN sem afetar o servidor.

#### WAF (Web Application Firewall)
- Filtra o tráfego com base em regras.
- Permite, desafia ou bloqueia requisições.

**Funcionalidades:**

- Detecta padrões de ataque conhecidos
- Permite criação de regras personalizadas

Exemplo: limitar acessos ao `/login.php` a 5 por minuto por IP.

### Mitigação em Larga Escala
- Empresas como Google e Cloudflare conseguem mitigar ataques massivos.
- Usam redes distribuídas e filtragem avançada.

Exemplos:

- Google: 398 milhões de requisições/segundo
- Cloudflare: 11,5 Tbps

### Técnicas de Evasão por Atacantes
Mesmo com proteção, atacantes tentam burlar sistemas:

- Adicionar parâmetros aleatórios na URL (quebrando cache)
- Alterar user-agent
- Falsificar origem (referrer)
- Usar IPs de diferentes regiões

Objetivo: enganar CDN/WAF e atingir o servidor diretamente.
