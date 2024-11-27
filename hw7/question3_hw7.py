import pandas as pd 
import numpy as np
from math import sqrt
from recommendations import sim_pearson, sim_distance

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

'''
getRecommendations(prefs, person, t_or_b, similarity)
    - gets recommendations for a person by using a weighted average 
    of every others user's rankings
    - changed to return top or bottom (least recommended) according to parameter t_or_b'''
def getRecommendations(prefs, person, t_or_b, similarity=sim_pearson):
    totals = {}
    simSums = {}
    for other in prefs:
    # Don't compare me to myself
        if other == person:
            continue
        sim = similarity(prefs, person, other)
        # Ignore scores of zero or lower
        if sim <= 0:
            continue
        for item in prefs[other]:
            # Only score movies I haven't seen yet
            if item not in prefs[person] or prefs[person][item] == 0:
                # Similarity * Score
                totals.setdefault(item, 0)
                # The final score is calculated by multiplying each item by the
                #   similarity and adding these products together
                totals[item] += prefs[other][item] * sim
                # Sum of similarities
                simSums.setdefault(item, 0)
                simSums[item] += sim
    # Create the normalized list
    rankings = [(total / simSums[item], item) for (item, total) in
                totals.items()]
    # Return the sorted list, reversed or not according to t_or_b
    rankings.sort()
    if t_or_b == 't':
        rankings.reverse()
    return rankings

## RECOMMEND FILMS FOR SUBSTITUTE ME
prefs, users = myLoadMovieLens()

SUB_ME = '711'

# compute ratings can be done through this function: getRecommendations()
top_five_to_watch = getRecommendations(prefs, SUB_ME, t_or_b = 't')[:5]
bottom_five_dont_watch = getRecommendations(prefs, SUB_ME, t_or_b = 'b')[:5]

#print out nicely
print('\nTop five movies to watch: ')
for rating, movie in top_five_to_watch:
    print(f'{movie} with rating: {rating}')

print('\nFive movies to not watch (bottom): ')
for rating, movie in bottom_five_dont_watch:
    print(f'{movie} with rating: {rating}')