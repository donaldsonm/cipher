#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>

int main(int argc, string argv[])
{
    // if ./caesar and key# aren't provided, tell user what to do and shut down code
    if (argc != 2)
    {
        printf("Usage: ./caesar k\n");
        return 1;
    }
        // prompt user for string
        printf("plaintext: ");
        string plain = get_string();
        printf("ciphertext: ");
        for (int i = 0, n = strlen(plain); i < n; i++)
        {
            int key = atoi(argv[1]);
            int letter = (int)plain[i];
            // only change letters and leave spaces, commas, etc. alone
            if isalpha(letter)
            {
                int cipher = letter + key;

                // ensure that z wraps back around to a
                if (letter >= 65 && letter <= 90)
                {
                    while (cipher > 90)
                    {
                        cipher -= 26;
                    }
                }
                if (letter >= 97 && letter <= 122)
                {
                    while (cipher > 122)
                    {
                        cipher -= 26;
                    }
                }
                printf("%c", cipher);
            }
            else
            {
                printf("%c", plain[i]);
            }
        }
        printf("\n");
        return 0;
}