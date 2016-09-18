#include <stdio.h>

int main(int argc, char **argv)
{
    if (argc == 1)
        printf("hi there, world\n!");
    else {
        printf("hi there");
        for (int i = 1; i < argc; ++i)
            printf(", %s", argv[i]);
        printf("\n");
    }
    return 0;
}
