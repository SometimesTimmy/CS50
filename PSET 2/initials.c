#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>


int main(void)
{
    string s = get_string();
    if (s !=NULL)
    {
        // If the first characer is not a space, go ahead and print it as upper case
        if (s[0] != ' ')
        {
            printf("%c", toupper(s[0]));
        }
        // Iterate through the string while searching for the first character after a space to capitalize
        // Iteration is through L-1 because char s(L) == '\0'
        for (int i = 0, L = strlen(s); i < L-1; i++)
        {
            if (s[i] == ' ' && s[i+1] != ' ')
            {
                printf("%c", toupper(s[i+1])); 
            }
        }
        printf("\n");
    }
}