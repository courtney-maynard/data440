import pandas as pd 
import numpy as np
from math import sqrt
from recommendations import sim_pearson, sim_distance, transformPrefs

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
calculateSimilarMovies(prefs, movie, t_or_b, n, similarity)
    - given a specific movie, return the top n most similar movies or bottom n least similar movies, 
    according to the choosing performed in my function myTopChosenMatches which takes the parameter t_or_b
    - a change from the original is that it only calculates for one movie at a time, not for every single movie in the set
'''
def calculateSimilarMovies(prefs, movie, t_or_b, n=5, similarity=sim_distance):
    # Invert the preference matrix to be item-centric
    itemPrefs = transformPrefs(prefs)
    
    # Find the most similar items to this one, using my special function with top or bottom
    similar_movies = myTopChosenMatches(itemPrefs, movie, t_or_b, n=n, similarity=similarity)

    return similar_movies

'''
myTopChosenMatches(prefs, person, t_or_b, n, similarity)
    - Returns the best matches for person from the prefs dictionary
    - Number of results and similarity function are optional params
    - I added an additional parameter t_or_b that either finds the top or bottom (most and least correlated) matches
'''
def myTopChosenMatches(prefs, person, t_or_b, n = 5, similarity=sim_pearson,):
    scores = [(similarity(prefs, person, other), other) for other in prefs if other != person]
    scores.sort()
    if t_or_b == 't':
        scores.reverse()
    return scores[0:n]

# NEW FUNCTIONS THAT AREN'T IN recommendations.py IN ANY CAPACITY
'''
loadMovieOnly(path = '')
    - only loads in the movies and returns them as dictionary
'''
def loadMovieOnly(path=''):
    # get movie titles
    movies = {}
    for line in open(path + 'u.item', encoding='ISO-8859-1'):
        (id, title) = line.split('|')[0:2]
        movies[id] = title
        
    return movies


## GENERATE CORRELATED MOVIES FOR MY PERSONAL FAVORITE AND LEAST FAVORITE
movies = loadMovieOnly()
prefs, users = myLoadMovieLens()

FAV_MOVIE = 'Groundhog Day (1993)'
LEAST_FAV_MOVIE = 'Blade Runner (1982)'

similar_fav = calculateSimilarMovies(prefs, FAV_MOVIE, t_or_b = 't')
least_similar_fav = calculateSimilarMovies(prefs, FAV_MOVIE, t_or_b = 'b')

similar_least_fav = calculateSimilarMovies(prefs, LEAST_FAV_MOVIE, t_or_b = 't')
least_similar_least_fav = calculateSimilarMovies(prefs, LEAST_FAV_MOVIE, t_or_b = 'b')

# print everything out nicely
print('\nfive most similar movies to my favorite movie, ', FAV_MOVIE, '\n')
for similarity, movie in similar_fav:
    print(f'{movie} with similarity score of: {similarity}')
print('-'*100)

print('five least similar movies to my favorite movie, ', FAV_MOVIE, '\n')
for similarity, movie in least_similar_fav:
    print(f'{movie} with similarity score of: {similarity}')
print('-'*100)

print('five most similar movies to my least favorite movie, ', FAV_MOVIE, '\n')
for similarity, movie in similar_fav:
    print(f'{movie} with similarity score of: {similarity}')
print('-'*100)

print('five least similar movies to my least favorite movie, ', LEAST_FAV_MOVIE, '\n')
for similarity, movie in least_similar_fav:
    print(f'{movie} with similarity score of: {similarity}')
print('-'*100)

