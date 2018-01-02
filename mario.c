#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int height;
    do
    {
        // ask for height
        printf("Height: ");
        height = get_int();
    }
    // ensure that the height is only between 0 and 23
    while (height < 0 || height > 23);
    {
        for (int rows = 0; rows < height; rows++)
        {
            // print out varying amounts of spaces for each row
            for (int space = height - rows; space - 1 > 0; space--)
            {
                printf(" ");
            }
            // print out varying amounts of hashes for each row
            for (int hash = height - rows; hash - 2 < height; hash++)
            {
                printf("#");
            }
            printf("\n");
        }
    }
}

