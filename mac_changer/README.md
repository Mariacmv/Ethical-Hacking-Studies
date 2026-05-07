# MAC Address Changer Study

Estudo prático sobre alteração de endereço MAC utilizando Python e comandos de rede no Linux.

## Aviso

Projeto desenvolvido exclusivamente para fins educacionais e laboratoriais.

Não utilize técnicas de alteração de identidade de rede em ambientes sem autorização.

---

## Objetivo

Compreender o funcionamento de endereços MAC e automatizar sua alteração utilizando Python.

O projeto também explora:
- automação de comandos Linux
- manipulação de subprocessos
- expressões regulares
- parsing de saída de comandos
- argumentos de linha de comando

---

## Conceitos estudados

- MAC Address
- Interfaces de rede
- Linux Networking
- ifconfig
- subprocess
- regex
- CLI arguments
- optparse
- automação em Python

---

## Tecnologias utilizadas

- Python
- Linux
- Regex
- subprocess
- optparse

---

## Estrutura do projeto

```bash
mac_changer.py
README.md
```

---

## Funcionalidades

### Alteração de endereço MAC

O script desativa a interface de rede, altera o endereço MAC e reativa a interface.

```python
subprocess.call(['ifconfig', interface, 'down'])
```

---

### Leitura automática do MAC atual

Uso de `subprocess.check_output()` para capturar a saída do comando `ifconfig`.

```python
ifconfig_result = subprocess.check_output(['ifconfig', interface], text=True)
```

---

### Extração do endereço MAC utilizando Regex

Busca automática do endereço MAC na saída do terminal.

```python
re.search(r"(\w\w:){5}\w\w", ifconfig_result)
```

---

### Argumentos de linha de comando

O programa permite que o usuário informe:
- interface de rede
- novo endereço MAC

Exemplo:

```bash
python mac_changer.py -i eth0 -m 00:11:22:33:44:55
```

---

### Verificação da alteração

Após modificar o MAC, o programa compara o resultado atual com o valor solicitado.

```python
if current_mac == options.new_mac:
```

---

## Observações

Este projeto faz parte dos meus estudos em:
- Linux
- redes
- automação
- segurança ofensiva
- scripting em Python

O código representa um laboratório de aprendizado em andamento.
