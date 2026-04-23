#include <stdio.h>

int main() {
    int x = 2147483647; // valor alto

    printf("Antes: %d\n", x);

    x = x + 1;

    printf("Depois: %d\n", x);

    return 0;
}