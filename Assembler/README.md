# Assembly

Estudos práticos sobre memória, ponteiros, comportamento de inteiros e conceitos de baixo nível utilizando C e Linux.

Grande parte dos exercícios foi baseada em laboratórios e estudos relacionados à exploração de memória e funcionamento interno de programas.

## Aviso

Todo o conteúdo deste diretório foi desenvolvido exclusivamente para fins educacionais e laboratoriais.

---

## Objetivo

Compreender conceitos fundamentais relacionados a:
- memória
- heap
- ponteiros
- integer overflow
- gerenciamento de memória
- funcionamento interno de programas em C

---

## Conceitos estudados

- Heap Allocation
- malloc() e free()
- Ponteiros
- Integer Overflow
- Signed vs Unsigned Integers
- Gerenciamento de memória
- Limites de tipos numéricos
- Estruturas de memória em C

---

## Tecnologias utilizadas

- C
- GCC
- Linux
- GDB

---

## Estrutura

```bash
heap.c
overflow.c
semvalorfixo.c
```

---

# heap.c

Estudo sobre alocação dinâmica de memória utilizando `malloc()` e liberação de memória com `free()`.

## Conceitos explorados

- Heap Memory
- Ponteiros
- Alocação dinâmica
- Verificação de erros de alocação
- Manipulação de strings em memória
- Memory leaks

## Destaques

### Alocação dinâmica

```c
char_ptr = (char *)error_checkedmalloc(mem_size);
```

### Liberação de memória

```c
free(char_ptr);
```

### Validação de falha de alocação

```c
if (ptr == NULL)
```

---

# overflow.c

Estudo simples sobre integer overflow utilizando inteiros com sinal (`signed int`).

## Objetivo

Demonstrar o comportamento de overflow ao ultrapassar o limite máximo representável por um inteiro de 32 bits.

## Exemplo

```c
int x = 2147483647;
x = x + 1;
```

O valor ultrapassa o limite máximo do tipo `int`, causando overflow.

---

# semvalorfixo.c

Estudo sobre comportamento de inteiros sem sinal (`unsigned int`) e wrap-around.

## Objetivo

Observar como variáveis unsigned retornam ao início da faixa de valores após atingir o limite máximo.

## Exemplo

```c
unsigned int x = 4294967295;
x = x + 1;
```

Após atingir o valor máximo, o inteiro reinicia em `0`.

---

## Observações

Este diretório faz parte dos meus estudos em:
- segurança ofensiva
- exploração de memória
- programação de baixo nível
- arquitetura de computadores
- comportamento interno de programas

Os códigos representam laboratórios de aprendizado em andamento.
