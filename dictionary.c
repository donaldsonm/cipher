// Implements a dictionary's functionality

#include <stdbool.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>
#include "dictionary.h"

// djb2 hash function adapted by Neel Mehta
unsigned int hash_word(const char* word)
{
    unsigned long hash = 5381;

    for (const char* ptr = word; *ptr != '\0'; ptr++)
    {
         hash = ((hash << 5) + hash) + tolower(*ptr);
    }
    return hash % 70000;
}

// A series of global variables that will be used in 2+ functions (node, hashtable, and word_count and load_success for size function)
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

node *hashtable[70000];

int word_count;

bool load_success = false;

// Check - Returns true if word is in dictionary else false
bool check(const char *word)
{
    // Make a copy of the word that can be changed to lowercase letters only
    char lower_word[LENGTH + 1];

    strcpy(lower_word, word);

    for (int i = 0, n = strlen(lower_word); i < n; i++)
    {
        lower_word[i] = tolower(lower_word[i]);
    }

    // Make a node pointer that will point to the first node of the corresponding linked list that the word is in
    int hash_value = hash_word(word);

    node *cursor = hashtable[hash_value];

    // Keep going through each node until the node pointer reaches the end of the linked list, checking along the way if the word is in the linked list dictionary
    while (cursor != NULL)
    {
        int check = strcmp(lower_word, cursor->word);

        if (check == 0)
        {
            return true;
        }

        cursor = cursor->next;
    }
    return false;
}

// Load - Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    char word[LENGTH + 1];

    // Open dictionary for reading, and check if the file is NULL or not
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        printf("Could not open file\n");
        return false;
    }

    // Make the head of each linked list point to NULL
    for (int null = 0; null < 70000; null++)
    {
        hashtable[null] = NULL;
    }

    // Go through the entire dictionary and put them into nodes
    while (fscanf(file, "%s", word) != EOF)
    {
        // Allocate memory for each node and check if memory can be allocated
        node *new_node = malloc(sizeof(node));
        if (new_node == NULL)
        {
            printf("Could not allocate memory\n");
            unload();
            return false;
        }

        // Copy word into string member
        strcpy(new_node->word, word);

        int hash_value = hash_word(new_node->word);

        // If head is pointing to NULL, make the newest node point to null and make the head point to the newest node
        if (hashtable[hash_value] == NULL)
        {
            new_node->next = NULL;
            hashtable[hash_value] = new_node;
        }

        // If head is pointing to a node, make the newest node point to the node that head is pointing at and make head point to the newest node
        else
        {
            new_node->next = hashtable[hash_value];
            hashtable[hash_value] = new_node;
        }

        // Keep count of words for size()
        word_count++;

    }
    load_success = true;

    fclose(file);

    return true;
}

// Size - Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    if (load_success == true)
    {
        return word_count;
    }
    else
    {
        return 0;
    }
}

// Unload - Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    // Go through every single linked list in the hash table and free them from memory
    for (int hash_value = 0; hash_value < 70000; hash_value++)
    {
        node *cursor = hashtable[hash_value];
        while (cursor != NULL)
        {
            node *temp = cursor;
            cursor = cursor->next;
            free(temp);
            if (temp == NULL)
            {
                return false;
            }
        }
    }
    return true;
}
