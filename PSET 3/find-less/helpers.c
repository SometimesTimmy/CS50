/**
 * helpers.c
 *
 * Helper functions for Problem Set 3.
 */

#include <cs50.h>

#include "helpers.h"

/**
 * Returns true if value is in array of n values, else false.
 */
bool search(int value, int values[], int n)
{
    if (n<0)
    {
        return false;
    }
    int L = 0; //initiate L from the smallest value
    int R = n - 1;  //initiate R from the full length of n-1 index
    while (n > 0)
    {
        int m = (R - L) / 2 + L; // start with the middle
        if (values[m]==value)
        {
            return true;
        }
        else if (values[m]<value) // search right of the middle (of that iteration)
        {
            L = m + 1;
        }
        else if (values[m]>value) // search left of the middle (of that iteration)
        {
            R = m - 1;
        }
        n = R - L + 1;
    }
    return false;
}

/**
 * Sorts array of n values.
 */
void sort(int values[], int n)
{
    // TODO: implement a sorting algorithm
    for (int i = 0; i < n-1; i++)
    {
        int min_index = i; // assume first value is min for now
        for (int j = i+1; j < n; j++) // compare 
        {
            if (values[min_index]>values[j])
            {
            min_index = j; // new index for min found
            }
        }
        if (min_index != i)
        {
        int new_min = values[min_index]; // swap the identified min with i-th index of the iteration
        values[min_index] = values[i];
        values[i] = new_min;
        }
    }
    return;
}
