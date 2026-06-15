Empresas costumam armazenar arquivos em bancos de dados, mas também em diretórios de servidores web e web shells costumam ficar em: /var/www/html (apache) e /usr/share/nginx/html (nginx). Outros diretórios que podem ser explorados são: /uploads/, /images/, /admin/ e /temp/. Web shells são programas maliciosos que visam web servidores para executar comandos remotamente.

É importante procurar por arquivos fora do normal, com nomes estranhos e extensões duplas (ex: image.php.jpg) que servem para esconder a real extensão, como .php ou .jsp. 

Comandos interessantes para buscar informações incluem: find com “newerct” (procurar entre duas datas específicas) e grep com eval para procurar funções específicas. Exemplos:
