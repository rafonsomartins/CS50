#include <stdio.h>

int main(int argc, char *word[])
{
    // TODO: Improve this hash function
    int a = 'a';
    int b = word[1][0];
    int c = (b - a);
    int i = c * 26;
    if (word[1][0] == '\'')
    {
        i = 0;
    }
    b = word[1][1];
    c = (b - a);
    int j = c;
    if (word[1][1] == '\'')
    {
        j = 0;
    }
    int l = (i + j);
    printf("%i\n", l);
    return l;
}