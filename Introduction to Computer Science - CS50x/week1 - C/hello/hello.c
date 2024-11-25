#include <stdio.h>
#include <cs50.h>

int main(void)
{
    // What's your name?
    string name = get_string("What's your name? ");
    // Hello, (name)
    printf("hello, %s\n", name);

}