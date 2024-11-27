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
compareWithChosenMatches(prefs_dataframe, sub_me, chosen_matches)
    - compares a user, in this case sub_me, with specific other users movie ratings to see which 
    movies they have rated the exact same
    - returns a results dictionary consisting of a dataframe for each comparison user, and 
    each dataframe has the movie the sub_me user and comparision user have rated the same'''
def compareWithChosenMatches(prefs_dataframe, sub_me, chosen_matches):
    comparison_results = {}
    sub_me_ratings = prefs_dataframe.loc[sub_me]
    
    # i want to compare the substitute me with each of the top 5 matches / bottom 5 matches
    for each_user in range(0, 5):

        # get the user and find their preferences from the list
        matching_user = chosen_matches[each_user][1]
        matching_user_ratings = prefs_dataframe.loc[matching_user]

        # i want to pull out the movies they have rated in common, but only the ones actually rated not the NaNs
        same_rating_movies = sub_me_ratings[(sub_me_ratings == matching_user_ratings) & (sub_me_ratings >= 0) & (matching_user_ratings >= 0)]

        # make a dataframe for the movies in common and what rating was given
        if len(same_rating_movies) > 0:
            comparison_df = pd.DataFrame({
                'Movie': same_rating_movies.index,
                'Rating': same_rating_movies.values,
            })
            
            # save the comparison for each match
            comparison_results[matching_user] = comparison_df
            
    return comparison_results


## FIND MOST AND LEAST CORRELATED USERS TO THE SUBSTITUTE ME
prefs, users = myLoadMovieLens()

# turn the movie ratings (prefs) and users into a dataframe to make themm easier to work with
prefs_dataframe = pd.DataFrame.from_dict(prefs, orient = 'index')
users_dataframe = pd.DataFrame.from_dict(users, orient = 'index')

SUB_ME = '711'

top_five_matches = myTopChosenMatches(prefs, SUB_ME, t_or_b = 't', n = 5)
bottom_five_matches = myTopChosenMatches(prefs, SUB_ME, t_or_b = 'b', n = 5)

# comparison to see what movies are in common/how many
top_matches_comparison_results = compareWithChosenMatches(prefs_dataframe, SUB_ME, top_five_matches)
bottom_matches_comparison_results = compareWithChosenMatches(prefs_dataframe, SUB_ME, bottom_five_matches)

# print out nicely
print('The top five matches for most similar critics are: ', top_five_matches, '\n')
for match_user_id, comparison_df in top_matches_comparison_results.items():
    print(f'Movie ratings in common between substitute me and user {match_user_id}:')
    print(comparison_df)
    print('\n')

print('The bottom five matches, so least similar critics, are: ', bottom_five_matches, '\n')
for match_user_id, comparison_df in bottom_matches_comparison_results.items():
    print(f'Movie ratings in common between substitute me and user {match_user_id}:')
    print(comparison_df)
    print('\n')