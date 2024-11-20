# GOOD TWITTER BOT  --> VOLUNTEER OPPORTUNITY AGGREGATION, ANALYSIS, AND BOOSTING
# IMPORTS
import json
import gzip
import time

from playwright.sync_api import sync_playwright
from scrape_twitter import get_auth_twitter_pg
from scrape_twitter import get_search_tweets
from util import write_tweets_to_jsonl_file
from datetime import datetime, timedelta

'''
is within_data_range(tweet_date, days)
    inputs: the date of the tweet, the number of days
    - checks to see if the tweet time stamp is within the given day range, in this case 7 or 30'''
def is_within_date_range(tweet_date, days):
    return tweet_date >= (datetime.now() - timedelta(days=days))

'''
collect_tweets()
    - scan for tweets that offer volunteer opportunities using keywords: 'volunteers needed', 'volunteer opportunities', 'volunteer with us'
    - saves the tweets in json files according the the keywords
    '''
def collect_tweets():

    collect_attempts = 3
    sleep_for = 900 # 15 minutes
    keywords = ['volunteers needed', 'volunteer opportunities', 'volunteer with us']

    for each_attempt in range(collect_attempts):
        print('collecting tweets attempt number: ', each_attempt, ' for keyword: ', keywords[each_attempt])
        playwright = sync_playwright().start()
        browser_dets = get_auth_twitter_pg(playwright)

        if len(browser_dets) != 0:
            # collect the tweets 
            all_volunteer_tweets = get_search_tweets(browser_dets, keywords[each_attempt], max_tweets=1000)
            write_tweets_to_jsonl_file(f"bot_all_volunteer_tweets_{each_attempt}.json.gz", all_volunteer_tweets['tweets'])

        playwright.stop()

        # cool down time so twitter will let me scrape again
        time.sleep(sleep_for)

'''
extract_content()
    - collect important data from the tweets:
        - username
        - time of day of the tweet
        - date of the tweet
        - day of week of the tweet
        - text of the tweet
        - sign-up link for the opportunity, or check that it has contact information
        - number of likes
        - number of retweets
    - ensure that the tweet is likely to be a volunteer posting by eliminating replies and checking for sensitive content
    - filter by the past week and the past month
    - save tweet data collected into two json files, one for the past week and one for the past month
    '''
def extract_content():
    tweet_content_week = []  
    tweet_content_month = [] 

    # load in the data from the JSONL file with all tweets
    tweet_files = ['bot_all_volunteer_tweets_0.json.gz', 'bot_all_volunteer_tweets_1.json.gz', 'bot_all_volunteer_tweets_2.json.gz' ]

    for tweet_file in tweet_files:
        with gzip.open(tweet_file, 'rb') as infile:

            for tweet in infile:
                tweet = json.loads(tweet.decode())
                
                if 'created_at' not in tweet:
                    print('skipping tweet due to missing \'created_at\'')
                    continue  # skip this tweet if 'created_at' is missing, meaning it's some kind of messed up tweet collection
                
                tweet_timestamp = datetime.strptime(tweet['created_at'], "%Y-%m-%dT%H:%M:%S.%fZ")

                # collect other relevant tweet data
                tweet_data = {
                    'username': tweet['user']['screen_name'],
                    'time': str(tweet_timestamp.time()),
                    'date': str(tweet_timestamp.date()),
                    'day_of_week': tweet_timestamp.date().strftime('%A'),
                    'is_reply': tweet.get('in_reply_to_status_id_str', None),
                    'possibly_sensitive': tweet.get('possibly_sensitive', None),
                    'num_likes': tweet['favorite_count'],
                    'num_retweets': tweet.get('retweet_count', None),
                    'text': tweet['text'],
                    'links': []
                }

                # check for links in the tweet
                if 'entities' in tweet and 'urls' in tweet['entities']:
                    for link in tweet['entities']['urls']:

                        # exclude links we know are not sign-ups (other media)
                        links_excluded = ['x.com', 'twitter.com', 'youtu.be', 'youtube.com', 'twitch.com', 'soundcloud.com', 'netflix.com', 'spotify.com', 'tiktok']
                        if not any(excluded in link['expanded_url'] for excluded in links_excluded):
                            tweet_data['links'].append(link['expanded_url'])
                
                # if the tweet is a reply, likely not to be a volunteer posting, and don't want anything possibly sensitive
                if tweet_data['is_reply'] is None and tweet_data['possibly_sensitive'] is not True:

                    # ensure that the tweet has a link of some sort to sign-up:
                    if len(tweet_data['links']) > 0 or ('contact' in tweet_data['text']):
                        # filter tweets by date range: last week vs last month
                        if is_within_date_range(tweet_timestamp, 7):  # last 7 days = past week
                            tweet_content_week.append(tweet_data)

                        if is_within_date_range(tweet_timestamp, 30):  # last 30 days = past month
                            tweet_content_month.append(tweet_data)

    print(f'Processed {len(tweet_content_week)} tweets from the past week')
    print(f'Processed {len(tweet_content_month)} tweets from the past month')

    # write tweets content separately for past week and past month
    write_tweets_to_jsonl_file('bot_volunteer_tweets_week.json.gz', tweet_content_week)
    write_tweets_to_jsonl_file('bot_volunteer_tweets_month.json.gz', tweet_content_month)

    return


if __name__ == "__main__":
    collect_tweets()

    print('tweets collected!')

    extract_content()

    print('tweets extracted!')

