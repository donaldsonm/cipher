// Helper functions for music

#include <cs50.h>
#include <math.h>
#include <string.h>
#include <ctype.h>

#include "helpers.h"

// Converts a fraction formatted as X/Y to eighths
int duration(string fraction)
{
    if (fraction != NULL)
    {
        // Convert the X and Y of X/Y to integers, and then multiply by 8
        int m = fraction[0] - '0';
        int n = fraction[2] - '0';
        return (m * 8) / n;
    }
    // If string is NULL then produce an error
    else
    {
        return 1;
    }
}

// Calculates frequency (in Hz) of a note
int frequency(string note)
{
    float hertz = 440.0;
    int j = note[2] - '0';
    int i = note[1] - '0';
    // Code written for 'A' and automatically works for 'A'
    // Series of if statements made to adjust for different letters
    if (note[0] == 'B')
    {
        hertz *= pow(2, 2.0 / 12.0);
    }
    if (note[0] == 'C')
    {
        hertz /= pow(2, 9.0 / 12.0);
    }
    if (note[0] == 'D')
    {
        hertz /= pow(2, 7.0 / 12.0);
    }
    if (note[0] == 'E')
    {
        hertz /= pow(2, 5.0 / 12.0);
    }
    if (note[0] == 'F')
    {
        hertz /= pow(2, 4.0 / 12.0);
    }
    if (note[0] == 'G')
    {
        hertz /= pow(2, 2.0 / 12.0);
    }

    // Everything else after the letters
    // If it has an accidental, then calculate frequency
    if (note[1] == '#' || note[1] == 'b')
    {
        if (note[1] == '#')
        {
            if (j < 4)
            {
                hertz /= pow(2, 4 - j) / pow(2, 1.0 / 12.0);
            }
            if (j >= 4)
            {
                hertz *= pow(2, j - 4) * pow(2, 1.0 / 12.0);
            }
        }
        if (note[1] == 'b')
        {
            if (j <= 4)
            {
                hertz /= pow(2, 4 - j) * pow(2, 1.0 / 12.0);
            }
            if (j > 4)
            {
                hertz *= pow(2, j - 4) / pow(2, 1.0 / 12.0);
            }
        }
    }

    // If it does not have an accidental, calculate frequency
    else
    {
        if (i < 4)
        {
            hertz = hertz / pow(2, (4 - i));
        }
        if (i > 4)
        {
            hertz = hertz * pow(2, (i - 4));
        }
    }
    hertz = round(hertz);
    return hertz;
}

// Determines whether a string represents a rest
bool is_rest(string s)
{
    //Use a string to compare if s is literally an empty string or not
    if (strcmp(s, "") == 0)
    {
        return true;
    }
    else
    {
        return false;
    }
}
