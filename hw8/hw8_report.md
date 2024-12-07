<h1 align = "center">HW 8 - Clustering</h1>

<h3 align = "center">Courtney Maynard</h3>
<h3 align = "center">DATA 440, Fall 2024</h3>
<h3 align = "center">December 5th, 2024</h3>

## Questions
### Q1: Find Popular Twitter Account
Generate a list of 50 popular accounts on Twitter with 10,000+ followers and 5000+ tweets. 

**B: What topics/categories do the accounts belong to? You don't need to specify a grouping for each account, but what general topics/categories will you expect to be revealed by the clustering? Provide this list before generating the cluster.**

I chose five distinct topics in order to search for accounts that fit the criteria. The first ten accounts are all related to running and athletics, the second ten accounts are all university accounts, the third set of ten accounts are all popular musicians' accounts or their official promotional social media accounts, the next ten accounts are accounts that post about technology, and the last group of accounts are all political figures. I expect that the clustering will identify the topical differences between these accounts and cluster them into five distinct categories. However, it is possible that the words of the tweets may reveal connections between the approximately twenty accounts belonging to people and they may cluster together. Additionally, the accounts that share information about technology may cluster with university accounts due to similar themes of education. 

### Q2: Create Account-Term Matrix
Create an account-term matrix for every term in the tweets, but only for the 500 most popular terms that are not stopwords.

#### Code:
```python
word_and_each_count = []
for each_word in wordlist:
  each_count = sumcounts[each_word]
  word_and_each_count.append((each_word, each_count))

# sort the pairs in reverse order by their count
word_and_each_count.sort(key=lambda x: x[1], reverse=True)

# get the top 500 words and their counts, but just append the word to the list
for each_word in range(500):
  popularlist.append(word_and_each_count[each_word][0])
```

I also made some changes to the scraping code in order to introduce a sleep time so that I didn't run into any problems with collecting the tweets.
```python
# only request new tweets if the data hasn't previously been written out
    account_count = 1 #ADDITION
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

            #ADDITION
            if account_count%10 == 0:
                time.sleep(900)

            account_count+=1
```

**A: Explain the general operation of generate_tweet_vector.py and how the tweets are converted to the account-term matrix.**

**B: Explain in detail the code that you added to filter for the 500 most frequent non-stopword terms.**

**C: Do the 500 most frequent terms make sense based on the accounts that you chose?**

### Q3: Create Dendrogram
Create an ASCII and JPEG Dendrogram using hierarchical clustering to cluster the most similar accounts.

<img src="dendogram_twitter_accounts.jpeg" >

**A: How well did the hierarchical clustering do in grouping similar accounts together? Were there any particularly odd groupings?**

### Q4: Cluster using k-Means
Cluster the accounts using k-Means with k's of 5, 10, and 20. For each value of k, create a file that lists the accounts in each cluster.

**A: Give a brief explanation of how the k-Means algorithm operates on this data. What features is the algorithm considering?**

**B: How many iterations were required for each value of k?**

**C: Which k value created the most reasonable clusters? For that grouping, characterize the accounts that were clustered into each group.**


