#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

int main (int argc, char *argv[])
{
    // ensure proper usage; if proper usage is not given the print an error
    if (argc != 2)
    {
        fprintf(stderr, "Usage: ./recover image\n");
        return 1;
    }

    char *image = argv[1];
    char filename[8];

    // open up the image given for reading; if it cannot be opened, then print an error
    FILE *raw_file = fopen(image, "r");
    if (raw_file == NULL)
    {
        fprintf(stderr, "Error: cannot open %s.\n", image);
        return 2;
    }

    // define the variables and pointers that will be used in the following code
    typedef uint8_t BYTE;
    BYTE block[512];
    int counter = 0;
    FILE *image_file = NULL;

    // read throughout the blocks of the image file until the end
    while (fread(block, 512, 1, raw_file) == 1)
    {
        // identify whether or not the block represents the beginning of an image
        if (block[0] == 0xff &&
        block[1] == 0xd8 &&
        block[2] == 0xff &&
        (block[3] >= 0xe0 && block[3] <= 0xef))
        {
            sprintf(filename, "%03i.jpg", counter);
            image_file = fopen(filename, "w");
            counter++;

            // if the image file cannot be opened, print an error
            if (image_file == NULL)
            {
                fclose(image_file);
                return 3;
            }
        }

        // write blocks
        if (image_file != NULL)
        {
            fwrite(block, 512, 1, image_file);
        }
    }

    // close everything else
    fclose(raw_file);
    fclose(image_file);
    return 0;
}