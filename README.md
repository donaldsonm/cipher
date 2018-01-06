# Questions

## What's `stdint.h`?

It is a header file that defines new integer types that allow a person to make integers of custom sizes that are preferable to the program that one is making.

## What's the point of using `uint8_t`, `uint32_t`, `int32_t`, and `uint16_t` in a program?

It allows one to fill up the exact amount of space that one wants to fill in a file.

## How many bytes is a `BYTE`, a `DWORD`, a `LONG`, and a `WORD`, respectively?

A 'BYTE' is 1 byte.
A 'DWORD' is 4 bytes.
A 'LONG' is 4 bytes.
A 'WORD' is 2 bytes.

## What (in ASCII, decimal, or hexadecimal) must the first two bytes of any BMP file be? Leading bytes used to identify file formats (with high probability) are generally called "magic numbers."

IN ASCII, they must be 'B' and 'M'.

## What's the difference between `bfSize` and `biSize`?

'bfSize' is the total number of bytes in the file.
'biSize' is the number of bytes in the info header.

## What does it mean if `biHeight` is negative?

It means that the bitmap starts from top to bottom with the origin of the file at the top-left corner.

## What field in `BITMAPINFOHEADER` specifies the BMP's color depth (i.e., bits per pixel)?

It is specified by 'biBitCount'.

## Why might `fopen` return `NULL` in lines 24 and 32 of `copy.c`?

It may return 'NULL' if 'fopen' cannot find the file that needs to be opened.

## Why is the third argument to `fread` always `1` in our code?

The third argument represents how many elements are necessary to read. It is always '1' because we are only reading one struct.

## What value does line 65 of `copy.c` assign to `padding` if `bi.biWidth` is `3`?

If 'bi.biWidth' is '3', then it would be 3 pixels with 3 bytes per pixel. That would be 9 bytes. To make it a multiple of 12, a
value of '3' padding would be needed to make it a multiple of 4.

## What does `fseek` do?

'fseek' moves to a specific location in a file.

## What is `SEEK_CUR`?

It is an integer constant that moves a file position to a given location.
