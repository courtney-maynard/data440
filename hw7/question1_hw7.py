import pandas as pd 
import numpy as np
from math import sqrt

# FUNCTIONS THAT I CHANGED/REWORKED FROM recommendations.py
'''
myLoadMovieLens(path = '')
    - increased functionality by adding in the loading in of users data from u.user
    returns the preferences and the users, both dictionaries
'''
def myLoadMovieLens(path=''):
    # get movie titles
    movies = {}
    for line in open(path + 'u.item', encoding='ISO-8859-1'):
        (id, title) = line.split('|')[0:2]
        movies[id] = title
        
    # load data
    prefs = {}
    for line in open(path + 'u.data'):
        (user, movieid, rating, ts) = line.split('\t')
        prefs.setdefault(user, {})
        prefs[user][movies[movieid]] = float(rating)

    # NEW ADDITION: load in the users data from u.user
    users = {}
    for line in open('u.user'):
        (user, age, gender, occupation, zipcode) = line.split('|')
        users[user] = {
            'age': int(age),
            'gender': gender,
            'occupation': occupation,
            'zipcode': zipcode.strip() # there were some newlines at the end i wanted to get rid of
        }
    return prefs, users

## FIND THE THREE USERS CLOSEST TO ME IN TERMS OF AGE, GENDER, OCCUPATION
prefs, users = myLoadMovieLens()
users_dataframe = pd.DataFrame.from_dict(users, orient = 'index')
users_dataframe.head(2)

closest_to_me = users_dataframe[(users_dataframe['age'] == 22) & (users_dataframe['gender'] == 'F') & (users_dataframe['occupation'] == 'student')]

# there were five that were closest to me, so I chose the top three: users 304, 599, and 711
top_three_closest = closest_to_me.head(3).index.tolist()
print('The top three closest users to me in terms of age (22), gender (F), and occupation (student) are: ', top_three_closest)

## TOP THREE AND BOTTOM THREE FAVORITE FILMS FOR EACH USER

# turn the movie ratings (prefs) into a dataframe to make it easier to work with
prefs_dataframe = pd.DataFrame.from_dict(prefs, orient = 'index')
top_three_prefs_df = prefs_dataframe.loc[top_three_closest] # select out the three users i'm comparing

# create dictionary to store the top three fav and top three least fav movies for each users
top_three_fav = {}
top_three_least_fav = {}

for each_top in top_three_closest:
    # only get the row of ratings for that specific user
    top_ratings = top_three_prefs_df.loc[each_top]

    # sort values of ratings and pick first three
    top_fav = top_ratings.sort_values(ascending=False).head(3)
    top_three_fav[each_top] = top_fav

    # sort values of ratings backwards and pick first three
    top_least_fav = top_ratings.sort_values(ascending=True).head(3)
    top_three_least_fav[each_top] = top_least_fav

# print the output nicely for movies and their ratings
print('The users\' three favorite movies are:')
for user, movies in top_three_fav.items():
    print(f'\nUser {user}:')
    print(top_three_fav[user].to_string(index=True))

print('\n\nThe users\' three least favorite movies are:')
for user, movies in top_three_least_fav.items():
    print(f'\nUser {user}:')
    print(top_three_least_fav[user].to_string(index=True))