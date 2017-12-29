#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int height;
    do
    {
        printf("Height: ");
        height = get_int();
    }
    while (height < 0 || height > 23);
    {
        for (int rows = 0; rows < height; rows++)
        {
            for (int space = height - rows; space - 1 > 0; space--)
            {
                printf(" ");
            }
            for (int hash = height - rows; hash - 2 < height; hash++)
            {
                printf("#");
            }
            printf("\n");
        }
    }
}

