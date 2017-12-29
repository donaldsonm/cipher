#include <cs50.h>
#include <stdio.h>
#include <math.h>

int main(void)
{
    float change;
    int total = 0;
    do
    {
        printf("How much change is owed?\n");
        change = get_float();
    }
    while (change < 0);
    {
        change = round(change*100);
    }
    while (change >= 25)
    {
        change = change - 25;
        total++;
    }
    while (change >= 10)
    {
        change = change - 10;
        total++;
    }
    while (change >= 5)
    {
        change = change - 5;
        total++;
    }
    while (change >= 1)
    {
        change = change - 1;
        total++;
    }
    printf("%i\n", total);
}