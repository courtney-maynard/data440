# IMPORTS
from playwright.sync_api import sync_playwright
from scrape_twitter import get_auth_twitter_pg
from scrape_twitter import get_search_tweets
from util import write_tweets_to_jsonl_file

import json
import gzip

# FUNCTIONS
'''
collect_tweets()
    inputs: none 
    ouputs: saved compressed json file of tweets
    - uses playright to collect the tweets from twitter according to a specified keyword
    - saves the tweets to a file with the associated keyword in it's name
'''
def collect_tweets():
    
    playwright = sync_playwright().start()
    browser_dets = get_auth_twitter_pg(playwright)

    if( len(browser_dets) != 0 ):
        tweets = get_search_tweets(browser_dets, "fashion", max_tweets=1000)
        write_tweets_to_jsonl_file('all_tweets_FINAL_fashion.json.gz', tweets['tweets'])

    playwright.stop()


'''
extract_links()
    inputs: none
    outputs: text file of all links associated with tweets corresponding to the keyword query
    - loads in JSON file and keeps track of how many tweets were from the keyword search
    - for each tweet, find the url entitity if it exists, and discard all irrelevant primarily
    audio/visual link, keeping all other links found
    - outputs the validity ratio to understand how many links result from every twitter request batch
    - writes and saves all links into a test file'''
def extract_links():

    tweet_content = []

    # load in the data from the jsonl file
    with gzip.open('all_tweets_FINAL_fashion.json.gz', 'rb') as infile:
        counter = 1
        for tweet in infile:
            tweet = json.loads(tweet.decode())
            tweet_content.append(tweet)
            print('reading tweets: ', counter)
            #print('the tweet: ', tweet)
            counter+=1

    print('length of number of tweets before link extraction: ', len(tweet_content))
    tweet_links = []

    for each_tweet in tweet_content:
        if 'entities' in each_tweet and 'urls' in each_tweet.get('entities', []):
            for link in each_tweet['entities']['urls']:

                # if links are from twitter or go to youtube, twitch, soundcloud, netflix, spotify or tiktok, exclude them
                links_excluded = ['x.com', 'twitter.com', 'youtu.be', 'youtube.com', 'twitch.com', 'soundcloud.com', 'netflix.com', 'spotify.com', 'tiktok']

                if any(excluded in link['expanded_url'] for excluded in links_excluded):
                    print('link excluded: ', link['expanded_url']) #ensuring excluded links caught
                else:
                    tweet_links.append(link['expanded_url'])
    
    # trying to determine how many tweets needed to result in 1000 valid and unique links
    print('number of links: ', len(tweet_links))
    print('valid ratio: ', len(tweet_links)/len(tweet_content))

    #print(tweet_links)

    # write links into a text file for use in a shell script to resolve the uris
    with open('all_tweets_FINAL_fashion_links.txt', 'w') as f:
        for link in tweet_links:
            f.write(link + '\n')

    return

if __name__ == "__main__":
    collect_tweets()

    print('tweets collected!')

    extract_links()

    print('tweets extracted!')
