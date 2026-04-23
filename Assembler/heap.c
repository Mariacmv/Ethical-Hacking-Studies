#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    char *char_ptr; // Ponteiro do tipo char
    int *int_ptr;   // Ponteiro do tipo inteiro
    int mem_size;
    void error_checkedmalloc(unsigned int size); // protótipo da função de erro para organização de código

    if (argc < 2) // Utilizar 50 como valor padrão caso a quantidade de argumentos seja menor que 2
        mem_size = 50;
    else
        mem_size = atoi(argv[1]); // Caso não, converta o primeiro argumento par inteiro e utilize o valor como memória a ser alocada

    printf("\t[+] alocando %d bytes de memoria na heap para char_ptr\n", mem_size);
    // char_ptr = (char *)malloc(mem_size); // Aloca memória na heap para acomodar 50 bytes, valor definido por mem_size
    char_ptr = (char *)error_checkedmalloc(mem_size);

    // if (char_ptr == NULL)
    // { // Checando se a quantidade de memória alocada é nula, ou seja, se malloc() falhou
    //     fprintf(stderr, "Error: nao foi possivel alocar memoria na heap.\n");
    //     // fprintf() é uma função de formatação de string que escreve a string formatada para um fluxo de saída específico, neste caso, stderr (fluxo de erro padrão). Ele é usado para exibir mensagens de erro para o usuário.
    //     exit(-1); // erro
    // }

    strcpy(char_ptr, "This is memory is located on the heap."); // Copia a string para o local onde char_ptr está apontando, que é a memória alocada na heap
    printf("char_ptr (%p) --> '%s'\n", char_ptr, char_ptr);

    printf("\t[+] alocando 12 bytes de memoria na heap para int_ptr\n"); // agora, alocando memória para o ponteiro do tipo inteiro, int_ptr
    int_ptr = (int *)error_checkedmalloc(12);

    *int_ptr = 31337; // Adiciona o valor 31337 ao endereço de memória apontado por int_ptr
    // utilizo o ponteiro porque o endereço é determinado dinamicamente em tempo de execução
    printf("int_ptr (%p) --> %d\n", int_ptr, *int_ptr);
    printf("\t[-] liberando a memoria alocada para char_ptr...\n");
    free(char_ptr); // Liberando a memória alocada para prevenir vazamentos de memória

    printf("\t[+] alocando 15 bytes para char_ptr\n");
    char_ptr = (char *)error_checkedmalloc(15); // Alocando mais 15 bytes de memória em um novo bloco de memória na heap para char_ptr

    strcpy(char_ptr, "new memory"); // coloco a string "new memory" no endereço que char_ptr aponta, que é o novo bloco de memória alocado na heap
    printf("char_ptr (%p) --> '%s'\n", char_ptr, char_ptr);
    printf("\t[-] liberando a memoria alocada para int_ptr...\n");
    free(int_ptr); // Liberando a memória alocada para prevenir vazamentos de memória
    printf("\t[-] liberando a memoria alocada para char_ptr...\n");
    free(char_ptr); // Liberando o outro bloco de memória alocada na heap
}

void error_checkedmalloc(unsigned int size)
{
    void *ptr;
    ptr = malloc(size); // aloco 12 bytes de memória para int_ptr, o suficiente para armazenar 3 inteiros (4 bytes cada)
    if (ptr == NULL)
    {                                                                         // Checando se a quantidade de memória alocada é nula, ou seja, se malloc() falhou
        fprintf(stderr, "Error: nao foi possivel alocar memoria na heap.\n"); // função de formatação de string com stderr que indica erro na alocação de memória
        exit(-1);
    }
};
