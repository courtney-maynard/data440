
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
