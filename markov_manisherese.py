import os

from random import choice

from sys import argv

import twitter


def open_and_read_file(filenames):
    """Takes file path as string; returns text as string.

    Takes a string that is a file path, opens the file, and turns
    the file's contents as one string of text.
    """

    file_data = ""

    for filename in filenames:
        text_file = open(filename)
        file_data = file_data + text_file.read()
        text_file.close()
    return file_data

def make_chains(text_string, n=2):
    """Takes input text as string; returns _dictionary_ of markov chains.

    A chain will be a key that consists of a tuple of (word1, word2)
    and the value would be a list of the word(s) that follow those two
    words in the input text.

    For example:

        >>> make_chains("hi there mary hi there juanita")
        {('hi', 'there'): ['mary', 'juanita'], ('there', 'mary'): ['hi'], ('mary', 'hi': ['there']}
    """

    chains = {}

    word_list = text_string.split()

    for i in range(len(word_list)-n):
        try:
            idx = i
            n_gram = []
            while idx < i+n:
                n_gram.append(word_list[idx])
                idx += 1
            n_gram = tuple(n_gram)
        except KeyError:
            print "error"
        try:
            next_word = word_list[i+n]
        except IndexError:
            next_word = None
        if n_gram not in chains:
            chains[n_gram] = []
        chains[n_gram].append(next_word)
    
    chains.pop(n_gram)
    return chains

def make_text(chains):
    """Takes dictionary of markov chains; returns random text."""

    current_key = choice(chains.keys())
    while not current_key[0].istitle():
        current_key = choice(chains.keys())

    text = " ".join(current_key)

    while True:

        try:
            next_random_word = choice(chains[current_key])
            if len(text) + 1 + len(next_random_word) > 140:
                break
            text += " " + next_random_word
            if text[-1].isalnum() or text[-1] == "," or text[-1] == "-":

                # convert tuple to list to get n-1 items for next key
                current_key_list = [item for item in current_key] # create list
                current_key_list = current_key_list[1:] # slice n-1 items
                current_key_list.append(next_random_word) # add last word
                current_key = tuple(current_key_list) # create new key of tuple with n items

            else:
                break

        except KeyError:
            break

    return text


def tweet(chain_result):
    # Use Python os.environ to get at environmental variables
    # Note: you must run `source secrets.sh` before running this file
    # to make sure these environmental variables are set.
    
    api = twitter.Api(
        consumer_key=os.environ["TWITTER_CONSUMER_KEY"],
        consumer_secret=os.environ["TWITTER_CONSUMER_SECRET"],
        access_token_key=os.environ["TWITTER_ACCESS_TOKEN_KEY"],
        access_token_secret=os.environ["TWITTER_ACCESS_TOKEN_SECRET"])

    # print api.VerifyCredentials()

    status = api.PostUpdate(chain_result)
    print status.text


def user_input():

    while True:

        response = raw_input("Would you like to tweet again? [q to quit] > ")
        if response.lower() == "q":
            break
        else:
            retweet = make_text(chains)
            tweet(retweet)


# Get the filenames from the user through a command line prompt, ex:
# python markov.py green-eggs.txt shakespeare.txt
filenames = argv[1:]

# Open the files and turn them into one long string
input_text = open_and_read_file(filenames)

# Get a Markov chain
chains = make_chains(input_text)

# Produce random text
random_text = make_text(chains)
# print random_text

# Your task is to write a new function tweet, that will take chains as input
tweet(random_text)

user_input()