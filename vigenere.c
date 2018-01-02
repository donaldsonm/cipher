#include <stdio.h>
#include <ctype.h>
#include <cs50.h>
#include <string.h>

int main(int argc, string argv[])
{
    // print error if 2 arguments are not given
    if (argc != 2)
    {
        printf("Usage: ./vigenere k\n");
        return 1;
    }
    // print error if key contains non-alphabet characters
    string key = argv[1];
    for (int a = 0, b = strlen(key); a < b; a++)
    {
        if (!(isalpha(argv[1][a])))
        {
            printf("Usage: ./vigenere k\n");
            return 1;
        }
    }

    printf("plaintext: ");
    string plain = get_string();
    printf("ciphertext: ");
    int counter = 0;
    for (int i = 0, n = strlen(plain); i < n; i++)
    {
        if isalpha(plain[i])
        {
            int cipher = (toupper(key[counter % strlen(key)]) - 65) + plain[i];
            if (plain[i] >= 65 && plain[i] <= 90)
            {
                while (cipher > 90)
                {
                    cipher -= 26;
                }
            }
            if (plain[i] >= 97 && plain[i] <= 122)
            {
                while (cipher > 122)
                {
                    cipher -= 26;
                }
            }
            printf("%c", cipher);
            counter++;
        }
        else
        {
            printf("%c", plain[i]);
        }

    }
    printf("\n");
    return 0;
}