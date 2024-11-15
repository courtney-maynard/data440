
# ideas for good social twitter bot:
- combatting misinformation:
  - grabs tweets with keywords relating to certain topics, such as vaccines, climate, or others
  - then pivots to google, searching for journal articles about the topic
  - grabbing the first 5 articles with these certain topics keywords
  - replying to the tweet with these articles, suggesting a read

- for an account that you could interact with, how likely is it that that account is going to provide you with misinformation?
  - first, identify suspicious accounts that are tweeting stuff about hoaxes and whatever
  - go to the account, and scrape ~500 or so tweets and gather their urls
  - make the urls all to final link and then put these links into fact checker websites
  - get the data back about whether it is correct or misinformation
  - keep track of this data
  - create a visualization showing the likelihood of the account to be misinformation
  - then post that visualization as a reply to several tweets on that account, with a caption saying something like 'watch out! this account may be misinforming!' --> make sure there is a certain threshold to limit false positives
 

- image verification --> could solve the problem of people posting images out of context
  - download image and find the original source
  - post original source as a reply to the source
  - analyze how many
 
- volunteer opportunities
  - scans for tweets that offer volunteer opportunities with keywords such as 'volunteers needed'
    - only include tweets that have a link to the actual place where you can sign-up
  - collects the user who is tweeting, the time of day the tweet was tweeted, the location of the tweet, and the text
  - determines the type of volunteering/cause supported/event and the date of event using keyword analysis
  - weekly and monthly trend analysis:
    - accounts that post the most volunteer opportunities
    - geographic map of the volunteer opportunities (visualization)
    - trends in the causes/events supported if any
    - trends in the time of day the tweet was tweeted
  - posts a weekly and monthly volunteer report:
    - includes the tags of top three organizations that post the most frequently
    - posts trend visualizations for geographic map, trends in causes, and trends in times of day with suggestions to followers as to when      to source the best volunteer opportunities and what kind of opportunities are out there
