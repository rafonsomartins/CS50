#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int x;
    // Selecting the Hight
    do
    {
        x = get_int("Hight: ");
    }
    while (x < 1 || x > 8);

    for (int n = 1; n <= x; n++)
    {
        // Spaces
        for (int y = x - n; y > 0; y--)
        {
            printf(" ");
        }
        // Bricks
        for (int i = 1; i <= n; i++)
        {
            printf("#");
        }
        printf("\n");
    }
}