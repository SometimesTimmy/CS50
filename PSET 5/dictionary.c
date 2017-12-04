/**
 * Implements a dictionary's functionality.
 */
#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#include <stdbool.h>
#include "dictionary.h"

// [https://stackoverflow.com/questions/22741966/how-to-choose-size-of-hash-table]
// A good rule of thumb is to keep the load factor at 75% or less (some will say 70%) to maintain (very close to) O(1) lookup.
// Assuming you have a good hash function.
#define SIZE 200000
// there are 143,091 words in the large dictionary so 200,000 was selected arbitrarily

// define main variables
int word_count = 0; // number of words that will be loaded in the dictioanry
char word[LENGTH + 1]; // where LENGTH is 45 per dictionary.h
int loaded = 1; // change to zero later when dictionary is successfully loaded

// create nodes for linked list
typedef struct node
{
    char word[LENGTH+1];
    struct node* next;
}
node;

// initialize a hash table with null
node* hashtable[SIZE] = {NULL};

// create a hash function
int hash(const char *word)
{
    int hash = 0;
    int n = strlen(word);
    for (int i = 0; i < n; i++)
    {
        hash = (31*hash + word[i])%SIZE;
        // basing hash function on JAVA: hash = (R * hash + s.charAt(i)) % M;
    }
    return hash;
}

/**
 * Returns true if word is in dictionary else false.
 */
bool check(const char *word) // assume all strings passed in will be alphabetical characters and/or apostrophe
{

    char copy[LENGTH + 1];
    int L = strlen(word);

    // take advantage of the fact that the dictionary is all in lower case
    // for ease of comparison, make all of the characters in copy lower case
    for (int i = 0; i < L; i++)
    {
        copy[i] = tolower(word[i]);
    }

    copy[L] = '\0'; // add a null terminator to the end of the string

    int index = hash(copy);

    // make a temporary pointer, and set it to the linked list of the index within the hash table
    node* ptr = hashtable[index];

    // check until the end of the linked list
    while (ptr != NULL)
    {
        if (strcmp(ptr->word, copy) == 0)
        {
            // word is found in the dictionary
            return true;
        }
        else
        {
            // keep checking the next nodes until end is reached
            ptr = ptr->next;
        }
    }
    return false;
}

/**
 * Loads dictionary into memory. Returns true if successful else false.
 */
bool load(const char *dictionary)
{
    // confirm that the dictionary can be opened
    FILE* file = fopen(dictionary, "r"); // in file of pset5 is one of the dictionaries
    if (file == NULL)
    {
        printf("Could not open dictionary.\n");
        return false;
    }

    char word[LENGTH + 1];

    // scan through the dictionary
    while (fscanf(file, "%s", word) != EOF)
    {
        node* new_node = malloc(sizeof(node));

        strcpy(new_node->word, word);

        word_count++;

        // hash the latest word
        int index = hash(word);

        if (hashtable[index] == NULL)
        // if the resulting index is NULL from hashing this particular new_node, it means that it is empty.
    	{
    		hashtable[index] = new_node; // a start of a node for future linked-list
    		new_node->next = NULL; // future linked-list
    	}

    	else
        {
            new_node->next = hashtable[index]; // insert a new node to the beginning of the linked-list
            hashtable[index] = new_node;
        }
    }
    fclose(file);
    loaded = 0;
    return true;
}


/**
 * Returns number of words in dictionary if loaded else 0 if not yet loaded.
 */
unsigned int size(void)
{
    if (loaded == 0)
    {
        return word_count;
    }
    else
    {
        return 0;
    }
}

/**
 * Unloads dictionary from memory. Returns true if successful else false.
 */
bool unload(void)
{
    // start from the 0th array of the hash table
    int index = 0;

    // iterate through entire hashtable array
    while (index < SIZE)
    {
        // if hashtable is empty at index, go to next index
        // we would expect some to be empty as SIZE > word_count and the fact that certain indices contain linked list
        if (hashtable[index] == NULL)
        {
            index++;
        }

        else
        {
            while(hashtable[index] != NULL)
            {
                node* ptr = hashtable[index];
                hashtable[index] = ptr->next;
                free(ptr);
            }

            // once this index within the array is freed, move onto the next index
            index++;
        }
    }
    return true;
}