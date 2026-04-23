#include <stdio.h>

int main()
{
    unsigned int x = 4294967295;
    printf("%u\n", x);

    for (int i = 0; i < 40; i++)
    {
        x = x + 1;
        printf("%u\n", x);
    }

    return 0;
}