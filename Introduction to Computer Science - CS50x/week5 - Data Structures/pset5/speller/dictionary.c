// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

int sizes;
bool loaded;

// TODO: Choose number of buckets in hash table
const unsigned int N = 676;

// Hash table
node *table[N];

bool check_word(node *tables, char word[LENGTH + 1]);
bool regist_word(node **tables, char worde[LENGTH + 1]);
bool free_node(node **tables);

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // TODO
    int n = 0;
    char word2[LENGTH + 1] = "";
    while (word[n] != '\0')
    {
        if (islower(word[n]) == 0 && word[n] != '\'')
        {
            word2[n] = tolower(word[n]);
        }
        else
        {
            word2[n] = word[n];
        }
        n++;

    }
    word2[n] = '\0';
    int x = hash(word2);
    bool cw = check_word(table[x], word2);
    return cw;
}

bool check_word(node *tables, char word[LENGTH + 1])
{
    if (!strcmp(tables->word, word))
    {
        return true;
    }
    else if (tables->next == NULL)
    {
        return false;
    }
    return check_word(tables->next, word);
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // TODO
    for (int i = 0; i < N; i++)
    {
        table[i] = NULL;
    }
    loaded = true;
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        loaded = false;
        fclose(file);
        return false;
    }
    char c = '\0';
    int index = 0;
    sizes = 0;
    char worde[LENGTH + 1] = "";
    while (fread(&c, sizeof(char), 1, (file)))
    {
        if (c != '\n')
        {
            worde[index] = c;
            index++;
        }
        else
        {
            worde[index] = '\0';
            int x = hash(worde);
            if (regist_word(&table[x], worde))
            {
                index = 0;
                sizes++;
            }
            else
            {
                loaded = false;
                fclose(file);
                return false;
            }
        }
    }
    fclose(file);
    return true;
}

bool regist_word(node **tables, char worde[LENGTH + 1])
{
    if (tables == NULL)
    {
        return false;
    }
    if (*tables == NULL)
    {
        *tables = (node *) malloc(sizeof(node));
        if (tables == NULL)
        {
            return false;
        }
        strcpy((*tables)->word, worde);
        (*tables)->next = NULL;
        return true;
    }
    else
    {
        return regist_word(&(*tables)->next, worde);
    }
}
// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    if (!loaded)
    {
        return 0;
    }
    else
    {
        return sizes;
    }
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO
    for (int i = 0; i < N; i++)
    {
       bool unloaded = free_node(&table[i]);
       if (!unloaded)
        {
            return unloaded;
        }
    }
    return true;
}

bool free_node(node **tables)
{
    if (*tables != NULL)
    {
        free_node(&(*tables)->next);
    }
    free(*tables);
    return true;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO: Improve this hash function
    if (strlen(word) < 3)
    {
       return (((int)word[0] - 97) * 26);
    }
    int i = ((int)word[0] - 97) * 26 + ((int)word[1] - 97);
    return i;
}