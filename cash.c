#include <cs50.h>
#include <stdio.h>
#include <math.h>

int main(void)
{
    float change;
    int total = 0;
    do
    {
        // ask for change
        printf("How much change is owed?\n");
        change = get_float();
    }
    // ensure that they give me a positive number of change
    while (change < 0);
    {
        change = round(change * 100);
    }
    // increase total for varying amounts of denominations of U.S coin currency
    // quarters
    while (change >= 25)
    {
        change -= 25;
        total++;
    }
    // dimes
    while (change >= 10)
    {
        change -= 10;
        total++;
    }
    // nickels
    while (change >= 5)
    {
        change -= 5;
        total++;
    }
    // pennies
    while (change >= 1)
    {
        change -= 1;
        total++;
    }
    printf("%i\n", total);
}