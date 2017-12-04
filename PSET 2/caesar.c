#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

int main(int argc, string argv[])
{
    string key = argv[1];
    if (argc !=2)
    {
        printf("Usage: ./caesar k\n");
        return 1;
    }
    if (argc == 2)
    {
        int k = atoi(key);
        k = k % 26;
        printf("plaintext:  ");
        string p = get_string(); // p asks for "p"lain text
        printf("ciphertext: ")  ;
        if (p !=NULL)
        {
            int n = strlen(p);
            for (int i = 0; i < n; i++) // sweep the length of P
            {
                if (!isalpha(p[i])) // if it is not a letter, re-print as is
                {
                    printf("%c", p[i]);
                }
                if (isupper(p[i]))
                {
                    p[i]=((p[i]-65)+k)%26+65;
                    printf("%c", (char)p[i]);
                }
                if (islower(p[i]))
                {
                    p[i]=((p[i]-97)+k)%26+97;
                    printf("%c", (char)p[i]);
                }
            }
            printf("\n");
        }
    return 0;
    }
}