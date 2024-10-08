
'''combining all links from the various text files into one file'''

single_files = ['all_tweets_FINAL_america_links.txt', 'all_tweets_FINAL_article_links.txt', 'all_tweets_FINAL_artificialintelligence_links.txt', 'all_tweets_FINAL_baseball_links.txt', 'all_tweets_FINAL_boston_links.txt', 'all_tweets_FINAL_campaign_links.txt', 'all_tweets_FINAL_chatgpt_links.txt', 'all_tweets_FINAL_chemistry_links.txt', 'all_tweets_FINAL_climate_links.txt', 'all_tweets_FINAL_college_links.txt', 'all_tweets_FINAL_covid_links.txt', 'all_tweets_FINAL_crime_links.txt', 'all_tweets_FINAL_datascience_links.txt', 'all_tweets_FINAL_debate_links.txt', 'all_tweets_FINAL_emergency_links.txt', 'all_tweets_FINAL_fashion_links.txt', 'all_tweets_FINAL_flu_links.txt', 'all_tweets_FINAL_generativeai_links.txt', 'all_tweets_FINAL_hiking_links.txt','all_tweets_FINAL_hurricanes_links.txt', 'all_tweets_FINAL_journal_links.txt', 'all_tweets_FINAL_kamala_links.txt', 'all_tweets_FINAL_learn_links.txt', 'all_tweets_FINAL_machinelearning_links.txt', 'all_tweets_FINAL_northcarolina_links.txt', 'all_tweets_FINAL_playoffs_links.txt', 'all_tweets_FINAL_poll_links.txt', 'all_tweets_FINAL_recipe_links.txt','all_tweets_FINAL_register_links.txt', 'all_tweets_FINAL_science_links.txt', 'all_tweets_FINAL_space_links.txt', 'all_tweets_FINAL_stocks_links.txt', 'all_tweets_FINAL_travel_links.txt', 'all_tweets_FINAL_trend_links.txt', 'all_tweets_FINAL_trump_links.txt', 'all_tweets_FINAL_unitedstates_links.txt', 'all_tweets_FINAL_voting_links.txt', 'all_tweets_FINAL_weather_links.txt', 'all_tweets_FINAL_wellness_links.txt' ]
combined_file = 'all_combined_links_FINAL.txt'

with open(combined_file, 'w') as outfile:
    for each_file in single_files:
        with open(each_file, 'r') as infile:
            outfile.write(infile.read())
