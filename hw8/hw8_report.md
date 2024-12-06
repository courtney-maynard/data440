<h1 align = "center">HW 8 - Clustering</h1>

<h3 align = "center">Courtney Maynard</h3>
<h3 align = "center">DATA 440, Fall 2024</h3>
<h3 align = "center">December 5th, 2024</h3>

## Questions
### Q1: Find Popular Twitter Account
Generate a list of 50 popular accounts on Twitter with 10,000+ followers and 5000+ tweets. 

**B: What topics/categories do the accounts belong to? You don't need to specify a grouping for each account, but what general topics/categories will you expect to be revealed by the clustering? Provide this list before generating the cluster.**

### Q2: Create Account-Term Matrix
Create an account-term matrixc for every term in the tweets, but only for the 500 most popular terms that are not stopwords.

#### Code:

**A: Explain the general operation of generate_tweet_vector.py and how the tweets are converted to the account-term matrix.**

**B: Explain in detail the code that you added to filter for the 500 most frequent non-stopword terms.**

**C: Do the 500 most frequent terms make sense based on the accounts that you chose?**

### Q3: Create Dendrogram
Create an ASCII and JPEG Dendrogram using hierarchical clustering to cluster the most similar accounts.

**A: How well did the hierarchical clustering do in grouping similar accounts together? Were there any particularly odd groupings?**

### Q4: Cluster using k-Means
Cluster the accounts using k-Means with k's of 5, 10, and 20. For each value of k, create a file that lists the accounts in each cluster.

**A: Give a brief explanation of how the k-Means algorithm operates on this data. What features is the algorithm considering?**

**B: How many iterations were required for each value of k?**

**C: Which k value created the most reasonable clusters? For that grouping, characterize the accounts that were clustered into each group.**


