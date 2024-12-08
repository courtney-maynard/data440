# generate_tweet_vector.py
# MCW
# Based on generatefeedvector.py from 
# https://github.com/arthur-e/Programming-Collective-Intelligence/blob/master/chapter3/generatefeedvector.py

import os
import gzip
from tweet_parser import parse
import re
import json
from os.path import exists
import time

def getwordcounts(browser_dets, screen_name, num_tweets=50):
    '''
    browser_dets: playwright object needed to scrape Twitter
    screen_name: Twitter screen_name
    returns screen_name and dictionary of word counts for a Twitter account
    '''
    print('getwordcounts():', screen_name)
    
    os.makedirs('./tweets-cache/', exist_ok=True)
    cache_filename = f'./tweets-cache/{screen_name}.json.gz'
    
    if( exists(cache_filename) ):
        #read tweets from file
        infile = gzip.open(cache_filename, 'rb')
        d = json.loads(infile.read().decode('utf-8'))
        d['screen_name'] = screen_name
        print(f'\treading cache {cache_filename}')
        
        infile.close()
    else:
        # Parse the Twitter feed
        d = parse(browser_dets, screen_name, num_tweets=50)
        
        if( len(d['tweets']) != 0 ):
            d['screen_name'] = screen_name
            #write tweets to file
            with gzip.open(cache_filename, 'wt') as outfile:
                outfile.write(json.dumps(d, ensure_ascii=False))

            print(f'\tsaving {cache_filename}')
    wc = {}

    # Loop over all the entries
    for tweet in d['tweets']:
        # Extract a list of words
        words = getwords(tweet)
        for word in words:
            wc.setdefault(word, 0)
            wc[word] += 1

    return (d['screen_name'], wc)

def getwords(tweet):
    '''
    returns lowercase list of words after filtering
    '''

    # Remove URLs
    text = re.compile(r'(http://|https://|www\.)([^ \'\"]*)').sub('', tweet)

    # Remove other screen names (start with @)
    text = re.compile(r'(@\w+)').sub('', text)

    # Split words by all non-alpha characters
    words = re.compile(r'[^A-Z^a-z]+').split(text)

    # Filter for words between 4-15 characters, convert to lowercase, and return as a list
    return [word.lower() for word in words if (len(word) >= 4 and len(word) <= 15)]

def writecounts(apcount, sumcounts, wordcounts):
    # write these to files to read in later
    with open('apcount.txt', 'w') as outf:
        json.dump(apcount, outf)
    with open ('sumcounts.txt', 'w') as outf:
        json.dump(sumcounts, outf)
    with open ('wordcounts.txt', 'w') as outf:
        json.dump(wordcounts, outf)

def readcounts():
    # read these files and return the needed variables
    with open ('apcount.txt', 'r') as inf:
        apcount = json.load(inf)
    with open ('sumcounts.txt', 'r') as inf:
        sumcounts = json.load(inf)
    with open ('wordcounts.txt', 'r') as inf:
        wordcounts = json.load(inf)
    return apcount, sumcounts, wordcounts

def write_popular_terms_and_tweet_term_matrix(popularlist, wordcounts):

    # write out popular word list
    with open('popular_terms.txt', 'w') as outf:
        for word in popularlist:
            outf.write(word + '\n')

    # write out account-term matrix
    with open('tweet_term_matrix.txt', 'w') as outf:
        # write header row ("Account", list of words)
        outf.write('Account')
        for word in popularlist:
            outf.write('\t%s' % word)
        outf.write('\n')

        # write each row (screen_name, count for each word)
        for (screen_name, wc) in wordcounts.items():
            outf.write(screen_name)
            for word in popularlist:
                if word in wc:
                    outf.write('\t%d' % wc[word])
                else:
                    outf.write('\t0')
            outf.write('\n')

def main():

    #####
    # MAIN CODE STARTS HERE
    #####

    # set up Twitter scraper
    from playwright.sync_api import sync_playwright
    from scrape_twitter import get_auth_twitter_pg

    playwright = sync_playwright().start()
    browser_dets = get_auth_twitter_pg(playwright)

    apcount = {}      # number of accounts each word appears in
    wordcounts = {}   # words and frequency in each account
    sumcounts = {}    # words and frequency over all accounts (to determine most popular)

    # list of screen names should be in 'accounts.txt', one per line
    accountlist = [line.strip() for line in open('accounts.txt') if line.strip() != '']

    # only request new tweets if the data hasn't previously been written out
    account_count = 1
    if (not exists("apcount.txt") or not exists("sumcounts.txt") or not exists("wordcounts.txt")):
        for screen_name in accountlist:
            print('Scrapping: ', screen_name)
            try:
                # get tweets, filter and count words
                (user, wc) = getwordcounts(browser_dets, screen_name, num_tweets=50)
                wordcounts[user] = wc
            
                # count number of accounts each term appears in
                for (word, count) in wc.items():
                    apcount.setdefault(word, 0)
                    sumcounts.setdefault(word, 0)
                    
                    apcount[word] += 1        # counting accounts with the word
                    sumcounts[word] += count  # summing total counts for the word
            except:
                print ('Failed to parse account %s' % screen_name)

            if account_count%10 == 0:
                time.sleep(900)

            account_count+=1
        # write data out to files
        writecounts(apcount, sumcounts, wordcounts)
    else:
        # read the data from files (instead of requesting new tweets)
        (apcount, sumcounts, wordcounts) = readcounts()

    # remove stopwords ("fake" way)

    wordlist = []
    for (w, ac) in apcount.items():
        # w is the word, ac is the account count (was bc 'blog count' in textbook)
        frac = float(ac) / len(accountlist)
        if frac > 0.1 and frac < 0.5:
            wordlist.append(w)

    # popularlist will hold the 500 most frequent terms over all accounts
    popularlist = []

    #### 
    # BEGIN YOUR CODE BLOCK
    ####

    # Write code that stores the 500 most frequent non-stopword terms over all accounts in the list popularlist

    # Hints:
    # * sumcounts is a dict with the number of times that each word has appeared over all accounts
    #        ex: sumcounts["the"] = 30
    # * wordlist is a list of the non-stopwords

    # keep track of how many times each word appears by making a list of tuples --> word, count
    word_and_each_count = []
    for each_word in wordlist:
        each_count = sumcounts[each_word]
        word_and_each_count.append((each_word, each_count))

    # sort the pairs in reverse order by their count
    word_and_each_count.sort(key=lambda x: x[1], reverse=True)

    # get the top 500 words and their counts, but just append the word to the list
    for each_word in range(500):
        popularlist.append(word_and_each_count[each_word][0])
    

    ####
    # END YOUR CODE BLOCK
    ####
    write_popular_terms_and_tweet_term_matrix(popularlist, wordcounts)

    playwright.stop()

if __name__ == "__main__":
    main()