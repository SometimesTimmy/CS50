#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

int main(int argc, string argv[])
{
    string k = argv[1];
    if (argc !=2)
    {
        printf("Usage: ./vigenere ./ k\n");
        return 1;
    }
    int m = strlen(k);
    for (int x = 0; x < m; x++) // check if all the characters in the key are letters
    if (!isalpha(k[x]))
    {
        return 1;
    }
    if (argc == 2)
    {
        printf("plaintext:  ");
        string p = get_string(); // p asks for "p"lain text
        printf("ciphertext: ");
        if (p !=NULL)
        {
            int n = strlen(p);
            for (int i = 0; i < n; i++) // sweep the length of P
            {
            int j = i%m; // cycle through the keycode
            int ktemp = k[j];
                if (isupper(k[j]))
                {
                    ktemp=k[j]-65; // normalize the shift value to the letter only, not the uppercase
                }
                if (islower(k[j]))
                {
                    ktemp=k[j]-97; // normalize the shift value to the letter only, not the lowercase
                }
                if (!isalpha(p[i])) // if it is not a letter, re-print as is
                {
                    printf("%c", p[i]);
                }
                if (isupper(p[i]))
                {
                    p[i]=((p[i]-65)+ktemp)%26+65;
                    printf("%c", (char)p[i]);
                }
                if (islower(p[i]))
                {
                    p[i]=((p[i]-97)+ktemp)%26+97;
                    printf("%c", (char)p[i]);
                }
            }
        }
    }
    printf("\n");
    return 0;
}