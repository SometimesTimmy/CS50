#include <stdio.h>
#include <cs50.h>

int main(void)
{
    printf("Minutes: ");
    int n = get_int();
    printf("Bottles: %i\n", n*12);
}