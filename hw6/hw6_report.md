<h1 align = "center">HW 6 - Creating (good) social bots</h1>

<h3 align = "center">Courtney Maynard</h3>
<h3 align = "center">DATA 440, Fall 2024</h3>
<h3 align = "center">November 19th, 2024</h3>

<h4 align = "center"> The bot can be found at the following link: https://x.com/cbm_data_sci</h4>

## Criteria One: Usefulness
**Consider creating a bot to solve or partly solve a problem you care about --- maybe not poverty or crime or income inequality. In other words create a tool to address a need. Provide an argument in your report for the reason your Twitter bot is useful.**

My Twitter bot serves as a centralized location for statistics regarding volunteer opportunities posted on Twitter and boosted opportunities, making it easier for people interested in volunteering to find ways to give back. I am very passionate about volunteering, and I noticed when I go home, it is harder to find places to volunteer because there is a lack of large-scale communication, unlike the many centralized databases William & Mary and Williamsburg have. Thus, I decided to tackle the problem of lack of information regarding volunteer opportunities. My bot searches through all of the volunteer opportunities posted on Twitter within the last week and month, aggregates them to post helpful statistics, and boosts opportunities. In order to figure out what keywords would yield posts with calls for volunteers, I performed a lot of manual searching. I landed on three key phrases: 'volunteer opportunities', 'volunteers needed', and 'volunteer with us'. I found that many replies would have some combination of these words but not advertise volunteer opportunities - usually, they were sarcastic or rude replies to other tweets. Thus, I decided to filter out all tweets that are replies, working under the assumption that legitimate volunteer postings will be posted as singular tweets, not replies. 

The usefulness of the bot comes from both the ideas communicated through the visualizations and the boosting feature. I performed exploratory data analysis on all of the data I collected in a Jupyter notebook, which helped me decide on two key statistics and three visualizations to focus on. I decided to post two tweets about the top accounts for postings, one from the past week and one from the past month. Twitter users who stay updated with this bot account could then find new users to follow that may get them connected with more opportunities. 

<img src="/hw6/twitterproof/topfiveweek_actual.png" width="400" >

<img src="/hw6/twitterproof/topfivemonth_actual.png" width="400">


Next, I created three visualizations. Each visualization can help users identify when they should log-on to see more volunteer opportunities in their feed, or when they should check for new postings to be the first to sign up. One observation I had while manually searching for volunteer opportunities in order to create the scraper was that some postings would link to sign-up websites, while others would have photos showing more information about the event and the contact information to get connected. I accounted for these two primary ways of telling social media about volunteer opportunities within my scraper, and was interested if there was a correlation between the days opportunities are posted and whether they have links or not. It does not appear that there is a correlation currently, but this could change throughout the months. Users may want to log in on a Tuesday to see more opportunities, as evidenced by the first visualization, or between 3-8 Eastern Standard time, as evidenced by the last visualization. The number of opportunities posted each day has varied greatly (visualization two), but this graphic is not entirely representative of all posts, as twitter has rate limits and the scraper will grab the most recent tweets or most relevant before older or less relevant tweets. 

<img src="/hw6/twitterproof/stacked_actual.png" width="400" >

<img src="/hw6/twitterproof/days_actual.png" width="400" >

<img src="/hw6/twitterproof/times_actual.png" width="400" >

Lastly, I decided to implement boosting of volunteer opportunities, with the goal of the bot being an account people can follow to find more niche opportunities. The bot currently doesn't filter for user's geographic ranges, so it is just reposting any opportunities it finds, but it could certainly be tweaked for certain states/countries/localities. I created a unique hashtag, #BOOSTINGTHISOPPORTUNITY to make all the posts easier to find, and tag the original poster for Twitter users to reference back to for more information. By preserving the sign-up links and other information included about the tweet, users could hopefully find volunteer postings with greater ease. The algorithm could additionally be tweaked to only repost opportunities below a certain number of likes or retweets, but I found that was not necessary from my data exploration - a majority of the tweets scraped had less than ten likes. All of the opportunities that the bot chooses from were posted within the past week, ensuring that the date of volunteering is less likely to have passed so the posts are still relevant. Future iterations of the bot could use NLP techniques to filter posts by type of volunteer activity and for the date in order to post with more specialized hashtags to allow users to filter for what they want to do and when. Below are the ten randomly chosen opportunities that the bot posted. 

<img src="/hw6/twitterproof/boostingone.png" width="400" >

<img src="/hw6/twitterproof/boostingtwo.png" width="400" >

<img src="/hw6/twitterproof/boostingthree.png" width="400" >

<img src="/hw6/twitterproof/boostingfour.png" width="400" >

<img src="/hw6/twitterproof/boostingfive.png" width="400" >

<img src="/hw6/twitterproof/boostingsix.png" width="400" >

<img src="/hw6/twitterproof/boostingseven.png" width="400" >

<img src="/hw6/twitterproof/boostingeight.png" width="400" >

<img src="/hw6/twitterproof/boostingnine.png" width="400" >

<img src="/hw6/twitterproof/boostingten.png" width="400" >

Overall, my Twitter bot serves the social good of helping Twitter users find more ways to volunteer and give back in their communities.

## Criteria Two: Originality/Innovation
**Express yourself, be creative. Alternatively, consider improving a pre-existing solution or tool. Provide an argument in your report for the reason your Twitter bot is original or innovative.**

My twitter bot is original because it combines scraping from and posting to twitter, utilizing the collected data from scraped tweets within the posts. To run the bot, I ran both files 'good_twitter_bot.py' and 'good_twitter_bot_analysis_post.py'. The first file will gather the volunteer opportunities from twitter and extract the data, saving it to then be read in during execution of the second file. The second file creates all of the tweet messages and visualizations, as well as posts them. This bot could be set up to run on a weekly basis, continuing to update followers with relevant opportunities and provide more summary data. I improved my twitter scraping code from our earlier projects in order to incorporate the fifteen minute cool down period, meaning that I did not have to manually rescrape for each keyword and the bot truly acts as a scraping, analysis, and posting bot. To my knowledge, a bot like this does not yet exist, so the idea itself, as well as the code to execute, is original. Additionally, I adapted the scraping twitter code in order to post images, not just text, so that the bot could tweet the visualizations. The different types of tweets that my bot posts allows for a greater chance of interaction by users, as it appeals to people who are interested in data visualizations and statistics, as well as people interested in volunteering. I love creating visualizations, so it was important to me to have a creative component of the posted tweets, providing a more original spin on the overall project goal of posting tweets. The visualizations can be found above. 

## Code:
### 'good_twitter_bot.py': gathering tweets and extracting data
```python
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


```
### 'good_twitter_bot_analysis_post.py': analyzing tweet data and posting
```python
# GOOD TWITTER BOT  --> VOLUNTEER OPPORTUNITY AGGREGATION, ANALYSIS, AND REACH OUT(?)
# IMPORTS
import json
import gzip
import time
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import random

from playwright.sync_api import sync_playwright
from scrape_twitter import get_auth_twitter_pg
from scrape_twitter import get_search_tweets
from scrape_twitter import post_tweet
from util import write_tweets_to_jsonl_file
from datetime import datetime, timedelta

'''
tweets_per_weekday_vis(all_month_opportunities)
    - takes the dataframe of all volunteer postings found over the past month and creates a visualization
    of the number of tweets posted per each day of the week, with different colors to show the porportion of
    tweets that have sign-up links vs those that don't (they have contact information)
    - saves this visualization as stacked_day_of_week.png
'''
def tweets_per_weekday_vis(all_month_opportunities):
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    # grouping by day and setting up the stacks for links and no links
    all_month_opportunities['has_links'] = all_month_opportunities['links'].apply(lambda x: 'Has Links' if len(x) > 0 else 'No Links')
    all_month_grouped = all_month_opportunities.groupby(['day_of_week', 'has_links']).size().unstack(fill_value=0)
    all_month_grouped = all_month_grouped.reindex(day_order)

    all_month_grouped.plot(kind='bar', stacked=True, color=['#784B84', '#B284BE'], figsize=(10, 6))

    # plotting
    plt.title('Distribution of Tweets by Day of the Week (Stacked: Has Links vs No Links)', fontsize=16)
    plt.xlabel('Day of the Week', fontsize=12)
    plt.ylabel('Number of Tweets', fontsize=12)

    plt.legend(title='Links')

    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('stacked_day_of_week.png')


'''
tweets_per_month_day_vis(all_month_opportunities)
    - takes the dataframe of all volunteer postings found over the past month and creates a visualization
    of the number of tweets posted each day, with a line across the vis for the average number of postings
    - saves this visualization as month_post_freq.png
'''
def tweets_per_month_day_vis(all_month_opportunities):
    fig,ax = plt.subplots(figsize=(10, 6))

    # sorting opportunities by the day of the month
    days_of_month_opp = all_month_opportunities['date'].value_counts().sort_index()
    avg_opp_per_day = days_of_month_opp.mean()

    # plotting
    ax.plot(days_of_month_opp.index, days_of_month_opp.values, 'o', markeredgewidth=2, linestyle='--', color='purple')

    # average number of opportunities
    ax.axhline(y=avg_opp_per_day, color='navy', linestyle='-', label=f'Average Number of Opportunities Per Day: {avg_opp_per_day:.2f}')

    ax.set_title('Number of Posted Volunteer Opportunities per Day Over The Last Month', fontsize = 16)
    ax.set_xlabel('Date', fontsize = 14)
    ax.set_ylabel('Number of Opportunities', fontsize = 14)
    ax.legend()

    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('month_post_freq.png')

'''
tweets_per_time_of_day_vis(all_month_opportunities)
    - takes the dataframe of all volunteer postings found over the past month and creates a visualization
    of the hour of the day distribution of when tweets are posted
    - saves this visualization as time_of_day_posts.png
'''
def tweets_per_time_of_day_vis(all_month_opportunities):
    # extracting the hour from the datetime information
    all_month_opportunities['time'] = pd.to_datetime(all_month_opportunities['time'])
    all_month_opportunities['hour'] = all_month_opportunities['time'].dt.hour

    # plotting
    plt.figure(figsize=(10, 6))
    plt.hist(all_month_opportunities['hour'], bins=24, range=(0, 24), edgecolor='#524F81', color='#D8BFD8')

    plt.xlabel('Hour of the Day', fontsize = 14)
    plt.ylabel('Number of Tweets', fontsize = 14)
    plt.title('Distribution of Volunteer Opportunity Tweets by Time of Day, EST', fontsize = 16)

    plt.xticks(range(0, 24))
    plt.grid(True)
    plt.savefig('time_of_day_posts.png')

'''
data_analysis()
    - reads in the json files that were the output of running good_twitter_bot.py
    - with the dataframe, calls functions to create and save visualizations
    - creates the text to be posted in both textual categories of post:
        1) top five accounts with the most number of postings over the past week and month 
        2) ten random tweets over the past week that are reposted with the hashtag #BOOSTINGTHISOPPORTUNITY
    - returns the texts to be posted in tweets as top_5_week_tweet (a string), top_5_month_tweet (a string), boosting_tweet_dict (a dictionary)
'''
def data_analysis():

    # load in all of the week and month opportunities collected from the twitter scrape pass
    week_opportunities = pd.read_json('bot_volunteer_tweets_week.json.gz', compression='gzip', orient='records', lines=True)
    all_week_opportunities = week_opportunities.drop_duplicates(subset=['username', 'text'])

    month_opportunities = pd.read_json('bot_volunteer_tweets_month.json.gz', compression='gzip', orient='records', lines=True)
    all_month_opportunities = month_opportunities.drop_duplicates(subset=['username', 'text'])


    # VISUALIZATIONS
    # formatting specifics
    plt.rcParams.update({'font.family': 'DejaVu Serif', 'font.size': 12, 'text.color': 'black', 'axes.labelcolor': 'black', 'xtick.color': 'black', 'ytick.color': 'black'})

    # 1) Distribution of tweets on each day of the week
    tweets_per_weekday_vis(all_month_opportunities)

    # 2) Number of tweets posted each day of the past month
    tweets_per_month_day_vis(all_month_opportunities)

    # 3) Number of tweets posted each hour of the day during the past month aggregated
    tweets_per_time_of_day_vis(all_month_opportunities)


    # POSTING TWEETS TEXTS

    # 1) Top Five Accounts of the Week
    top_5_posters_week = all_week_opportunities['username'].value_counts().head(5)
    top_5_week_tweet = "The top five volunteer posters this week are:\n" + "\n".join(
        f"@{username} with {count} posts" for username, count in top_5_posters_week.items()
    ) + "\n\nFollow these accounts for volunteer opportunities!"

    # 2) Top Ten Accounts of the Month
    top_5_posters_month = all_month_opportunities['username'].value_counts().head(5)
    top_5_month_tweet = "The top five volunteer posters this month are:\n" + "\n".join(
        f"@{username} with {count} posts" for username, count in top_5_posters_month.items()
    ) + "\n\nFollow these accounts for volunteer opportunities!"

    # 3) Boosting Opportunities
    # choosing 10 random tweets of recent opportunities from the weekand boosting
    week_opp_list = all_week_opportunities[['text', 'username']].to_dict(orient='records')

    # ensure all the chosen tweets will meet the character limit, so less than 230 bc my pre-message will add up to 50
    filtered_week_opp_list = [tweet for tweet in week_opp_list if len(tweet['text']) < 230]

    boosting_tweets = random.sample(filtered_week_opp_list, 10) if len(filtered_week_opp_list) >= 10 else filtered_week_opp_list
    boosting_tweet_dict = {f"tweet_{i+1}": tweet for i, tweet in enumerate(boosting_tweets)}


    # dictionary with selected tweets, adding the hashtag to the tweet content and tag the original poster
    for i, tweet in enumerate(boosting_tweets, 1):
        tweet_key = f'tweet_{i}'  # keys are in format 'tweet_1', 'tweet_2', etc.
        
        tweet_text = tweet['text']
        tweet_username = tweet['username']
        
        # make sure the tweet to be posted has the hashtag and the username
        tweet_hash_user= f"#BOOSTINGTHISOPPORTUNITY from @{tweet_username}\n{tweet_text}"
        
        boosting_tweet_dict[tweet_key] = tweet_hash_user

    #for key, tweet in boosting_tweet_dict.items():
        #print(f'{key.upper()}: {tweet}\n')
    
    return top_5_week_tweet, top_5_month_tweet, boosting_tweet_dict

'''
posting_visualizations()
    - posts all three visualizations and their text message
    - incorporates adding images to the post
    - sleeps in between posts and prints the status after posting
'''
def posting_visualizations():
    with sync_playwright() as playwright:
        browser_dets = get_auth_twitter_pg(playwright)
        if( len(browser_dets) != 0):
            get_new_tweet_link = True
            twitter_account = 'cbm_data_sci'
            reply_to_link = ''

            message_stacked_week = '#datavisualization of the weekday frequency of twitter posts advertising volunteer opportunities over the past month'
            message_month_posts = '#datavisualization of the day frequency of twitter posts advertising volunteer opportunities over the past month'
            message_time_day = '#datavisualization of the time of day frequency of twitter posts advertising volunteer opportunities over the past month'

            # ensure i can add images to the tweet, changes in scrape_twitter.py
            image_path_stacked_week = 'stacked_day_of_week.png' 
            image_path_month_posts = 'month_post_freq.png' 
            image_path_time_day = 'time_of_day_posts.png' 

            post_status_stacked_week = post_tweet(browser_dets, message_stacked_week, twitter_account = twitter_account, get_new_tweet_link = get_new_tweet_link, reply_to_link = reply_to_link, image_path=image_path_stacked_week)
            print('post status stacked week:', post_status_stacked_week)

            time.sleep(60)

            post_status_month_posts = post_tweet(browser_dets, message_month_posts, twitter_account = twitter_account, get_new_tweet_link = get_new_tweet_link, reply_to_link = reply_to_link, image_path = image_path_month_posts)
            print('post status month posts:', post_status_month_posts)

            time.sleep(60)

            post_status_time_day = post_tweet(browser_dets, message_time_day, twitter_account = twitter_account, get_new_tweet_link = get_new_tweet_link, reply_to_link = reply_to_link, image_path = image_path_time_day)
            print('post status time of day:', post_status_time_day)
            
'''
posting_top_accounts(top_5_week_tweet, top_5_month_tweet)
    - takes as input the two text strings for the top five accounts and posts them, sleeping in between
'''
def posting_top_accounts(top_5_week_tweet, top_5_month_tweet):
    with sync_playwright() as playwright:
        browser_dets = get_auth_twitter_pg(playwright)
        if( len(browser_dets) != 0):
            get_new_tweet_link = True
            twitter_account = 'cbm_data_sci'
            reply_to_link = ''

            message_week = top_5_week_tweet
            message_month = top_5_month_tweet

            post_status_week = post_tweet(browser_dets, message_week, twitter_account = twitter_account, get_new_tweet_link = get_new_tweet_link, reply_to_link = reply_to_link)
            print('post status week:', post_status_week)

            time.sleep(60)

            post_status_month = post_tweet(browser_dets, message_month, twitter_account = twitter_account, get_new_tweet_link = get_new_tweet_link, reply_to_link = reply_to_link)
            print('post status month:', post_status_month)

'''
posting_boosted(boosting_tweet_dict)
    - takes as input the boosted tweet dictionary
    - for each tweet in the dictionary, the corresponding message is posted
'''
def posting_boosted(boosting_tweet_dict):
    with sync_playwright() as playwright:
        browser_dets = get_auth_twitter_pg(playwright)
        if( len(browser_dets) != 0):
            get_new_tweet_link = True
            twitter_account = 'cbm_data_sci'
            reply_to_link = ''

            for key,tweet in boosting_tweet_dict.items():
                message_boosted = tweet
                post_status_boosted = post_tweet(browser_dets, message_boosted, twitter_account = twitter_account, get_new_tweet_link = get_new_tweet_link, reply_to_link = reply_to_link)
                print('post status week:', post_status_boosted)

                time.sleep(30)


if __name__ == "__main__":
    top_5_week_tweet, top_5_month_tweet, boosting_tweet_dict = data_analysis()

    posting_top_accounts(top_5_week_tweet, top_5_month_tweet)

    time.sleep(60)

    posting_boosted(boosting_tweet_dict)

    time.sleep(60)

    posting_visualizations()
```

## changes to 'scrape_twitter.py' to incorporate posting visualizations:
```python

image_path = kwargs.get('image_path', None)

if image_path and Path(image_path).exists():
        # Upload the image by setting the file input field
        file_input_selector = 'input[type="file"]'
        browser_dets['page'].set_input_files(file_input_selector, image_path)
        time.sleep(1)  # Wait for the image upload to be ready
```
