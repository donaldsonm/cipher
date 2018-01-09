#include <stdio.h>
#include <stdlib.h>

#include "bmp.h"

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 4)
    {
        fprintf(stderr, "Usage: ./resize # infile outfile\n");
        return 1;
    }

    // remember command line arguments
    int n = atoi(argv[1]);
    char *infile = argv[2];
    char *outfile = argv[3];

    if (n > 100 || argv[1] < 0)
    {
        fprintf(stderr, "# must be positive integer less than 100\n");
        return -1;
    }

    // open input file
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 2;
    }

    // open output file
    FILE *outptr = fopen(outfile, "w");
    if (outptr == NULL)
    {
        fclose(inptr);
        fprintf(stderr, "Could not create %s.\n", outfile);
        return 3;
    }

    // read infile's BITMAPFILEHEADER
    BITMAPFILEHEADER bf;
    fread(&bf, sizeof(BITMAPFILEHEADER), 1, inptr);

    // read infile's BITMAPINFOHEADER
    BITMAPINFOHEADER bi;
    fread(&bi, sizeof(BITMAPINFOHEADER), 1, inptr);

    // ensure infile is (likely) a 24-bit uncompressed BMP 4.0
    if (bf.bfType != 0x4d42 || bf.bfOffBits != 54 || bi.biSize != 40 ||
        bi.biBitCount != 24 || bi.biCompression != 0)
    {
        fclose(outptr);
        fclose(inptr);
        fprintf(stderr, "Unsupported file format.\n");
        return 4;
    }

    // old height, width, and padding of image
    int ibiWidth = bi.biWidth;
    int ibiHeight = bi.biHeight;
    int inpadding = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;

    // new height, width, and padding of image
    bi.biWidth *= n;
    bi.biHeight *= n;
    int outpadding = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;

    bi.biSizeImage = ((sizeof(RGBTRIPLE) * bi.biWidth) + outpadding) * abs(bi.biHeight);
    bf.bfSize = bi.biSizeImage + sizeof(BITMAPFILEHEADER) + sizeof(BITMAPINFOHEADER);

    // write outfile's BITMAPFILEHEADER
    fwrite(&bf, sizeof(BITMAPFILEHEADER), 1, outptr);

    // write outfile's BITMAPINFOHEADER
    fwrite(&bi, sizeof(BITMAPINFOHEADER), 1, outptr);

    // iterate over infile's scanlines
    for (int i = 0, biHeight = abs(ibiHeight); i < biHeight; i++)
    {
        // write each line n times
        for (int r = 0; r < n; r++)
        {
            // iterate over pixels in scanline
            for (int j = 0; j < ibiWidth; j++)
            {
                // write n times
                for (int m = 0; m < n; m++)
                {
                    // temporary storage
                    RGBTRIPLE triple;

                    // read RGB triple from infile
                    fread(&triple, sizeof(RGBTRIPLE), 1, inptr);

                    fwrite(&triple, sizeof(RGBTRIPLE), 1, outptr);

                    if (m != n - 1)
                    {
                        fseek(inptr, -sizeof(RGBTRIPLE), SEEK_CUR);
                    }
                }

            }

            // skip over infile padding, if any
            fseek(inptr, inpadding, SEEK_CUR);

            // write outfile padding, if any
            for (int k = 0; k < outpadding; k++)
            {
                fputc(0x00, outptr);
            }

            if (r != n - 1)
            {
                fseek(inptr, -((sizeof(RGBTRIPLE) * ibiWidth) + inpadding) , SEEK_CUR);
            }
        }
    }
    // close infile
    fclose(inptr);

    // close outfile
    fclose(outptr);

    // success
    return 0;
}