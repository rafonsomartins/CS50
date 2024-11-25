#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./recover file.raw\n");
        return 1;
    }
    FILE *card = fopen(argv[1], "r");
    if (card == NULL)
    {
        printf("could not open file\n");
        return 1;

    }
    typedef uint8_t byte;
    const int block_size = 512;
    byte c[block_size];
    int count = 0;
    char name[8];
    FILE *file = 0;
    int x = 0;
    while (fread(&c, 1, sizeof(block_size), card) != 0)
    {
        if (c[0] == 255 && c[1] == 216 && c[2] == 255 && c[3] > 223)
        {
            if (x == 1)
            {
                fclose(file);
            }
            x = 1;
            sprintf(name, "%03i.jpg", count);
            count++;
            file = fopen(name, "w");
            fwrite(&c, 1, sizeof(block_size), file);
        }
        else if (x == 1)
        {
            fwrite(&c, 1, sizeof(block_size), file);
        }

    }
    fclose(card);
    fclose(file);
    return 0;
}