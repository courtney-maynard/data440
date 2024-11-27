<h1 align = "center">HW 7 - Recommender System</h1>

<h3 align = "center">Courtney Maynard</h3>
<h3 align = "center">DATA 440, Fall 2024</h3>
<h3 align = "center">November 26th, 2024</h3>


## Q1 
Find three users who are closest to me in terms of age, gender, and occupation.
For each of those 3 users:

- **a: what are their top 3 (favorite) films?**
  
- **b: what are their bottom 3 (least favorite) films**

Based on the movie values in those 6 tables, choose a user that is most like me, the *substitute me*. 

### Code/Outputs
```python
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
```
Parts A and B Answers:

```shell
(base) courtneymaynard@Courtneys-MacBook-Pro-2 homework7 % python3 question1_hw7.py
The top three closest users to me in terms of age (22), gender (F), and occupation (student) are:  ['304', '599', '711']
The users' three favorite movies are:

User 304:
Titanic (1997)          5.0
Jerry Maguire (1996)    5.0
Air Force One (1997)    5.0

User 599:
Truth About Cats & Dogs, The (1996)    5.0
Mirror Has Two Faces, The (1996)       5.0
Fear (1996)                            5.0

User 711:
Wrong Trousers, The (1993)    5.0
Philadelphia (1993)           5.0
Blade Runner (1982)           5.0


The users' three least favorite movies are:

User 304:
English Patient, The (1996)    1.0
George of the Jungle (1997)    1.0
Wishmaster (1997)              2.0

User 599:
Event Horizon (1997)        1.0
Leaving Las Vegas (1995)    2.0
For the Moment (1994)       2.0

User 711:
Happy Gilmore (1996)             1.0
Dragonheart (1996)               1.0
Independence Day (ID4) (1996)    1.0
```

### Commentary
To load in the data, I made minor changes to the loadMovieLens function to include loading in the user datafile and returning a dictionary. I subsetted all of the users by their age, gender, and occupation. There were five movie critics who were also 22-year-old female students, so I chose the first three according to a numerical ordering of their user id. To find their top and bottom movies, I took subsets from a dataframe representation of the prefs dictionary and then sorted their values ascending and descending. I haven't seen any of the top ten movies from either the favorites or least favorites lists for any of the three users, so I looked up some movie summaries and ended up choosing user 711 to be substitute me for the rest of the project. 

## Q2
Based on the ratings that users have given to the movies, answer the following questions:

- **a: which five users are most correlated to the *substitute me*? (i.e. which 5 users rate movies most similarly to the substitute me?)**
- **b: which five users are least correlated (i.e. negative correlation)**

### Code/Outputs
```python
from recommendations import sim_pearson, sim_distance

# FUNCTIONS THAT I CHANGED/REWORKED FROM recommendations.py
'''
myLoadMovieLens(path = '')
    - increased functionality by adding in the loading in of users data from u.user
    returns the preferences and the users, both dictionaries
'''
def myLoadMovieLens(path=''):
    # shown in above code block. for conciseness not shown here.

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
    each dataframe has the movie the sub_me user and comparision user have rated the same
'''
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
```

Part A and B Answers:

```shell
(base) courtneymaynard@Courtneys-MacBook-Pro-2 homework7 % python3 question2_hw7.py
The top five matches for most similar critics are:  [(1.0, '662'), (1.0, '358'), (0.9707253433941485, '732'), (0.9622504486493763, '519'), (0.9613406389911049, '520')] 

Movie ratings in common between substitute me and user 358:
                                               Movie  Rating
0                                        Babe (1995)     5.0
1                                     Contact (1997)     4.0
2                            Schindler's List (1993)     5.0
3  Wallace & Gromit: The Best of Aardman Animatio...     5.0
4                 What's Eating Gilbert Grape (1993)     4.0
5                         Room with a View, A (1986)     5.0
6                           Wizard of Oz, The (1939)     5.0
7                                  Piano, The (1993)     5.0


Movie ratings in common between substitute me and user 732:
                    Movie  Rating
0  Full Monty, The (1997)     5.0


Movie ratings in common between substitute me and user 519:
                  Movie  Rating
0  Boogie Nights (1997)     5.0


Movie ratings in common between substitute me and user 520:
                                    Movie  Rating
0                    Birdcage, The (1996)     4.0
1                  Full Monty, The (1997)     5.0
2  Beavis and Butt-head Do America (1996)     1.0
3                        Apt Pupil (1998)     4.0
4                             Emma (1996)     4.0


The bottom five matches, so least similar critics, are:  [(-1.0, '36'), (-1.0, '431'), (-1.0, '812'), (-1.0, '824'), (-0.9449111825230686, '309')] 

Movie ratings in common between substitute me and user 431:
                         Movie  Rating
0  English Patient, The (1996)     4.0


Movie ratings in common between substitute me and user 309:
                         Movie  Rating
0  English Patient, The (1996)     4.0
```

### Commentary
I changed the topMatches function to allow the user to input if they want to select top or bottom matches through an additional parameter, t_or_b. This prevented me from making two different functions, one for top items (people or movies) and one for bottom items, and I ended up using this myTopChosenMatches function in a later function. In addition to looking at which critics are most correlated with the substitute me, I was curious about which movies they rated in common, which is a factor in determining the correlation between critics. To investigate, I created a function that compares substitute me with the other users and returns the movie and rating for all movies that the two users rated exactly the same. I was shocked to see that for the most similar user to substitute me, user 662, who had a similarity score of 1.0, there were no movies in common. For the other user with a similarity score of 1.0, user 358, there were eight movies in common. Another shock was that for a critic who correlated -1.0 with substitute me, user 431, there was one movie rated in common. 

## Q3
Computing ratings for all the films that the *substitute me* has not seen.

- **provide a list of the top five recommendations for films that the *substitute me* should see**
- **provide a list of the bottom five recommendations (i.e. films the *substitute me* will likely hate**

### Code/Outputs

```python
from recommendations import sim_pearson, sim_distance

# FUNCTIONS THAT I CHANGED/REWORKED FROM recommendations.py
'''
myLoadMovieLens(path = '')
    - increased functionality by adding in the loading in of users data from u.user
    returns the preferences and the users, both dictionaries
'''
def myLoadMovieLens(path=''):
    # for conciseness not shown here. shown in q1 code blocl
    
'''
getRecommendations(prefs, person, t_or_b, similarity)
    - gets recommendations for a person by using a weighted average 
    of every others user's rankings
    - changed to return top or bottom (least recommended) according to parameter t_or_b
'''
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
```
Lists of the top 5 and bottom 5 recommendations:
```shell
(base) courtneymaynard@Courtneys-MacBook-Pro-2 homework7 % python3 question3_hw7.py

Top five movies to watch: 
Prefontaine (1997) with rating: 5.000000000000001
Entertaining Angels: The Dorothy Day Story (1996) with rating: 5.000000000000001
They Made Me a Criminal (1939) with rating: 5.0
The Deadly Cure (1996) with rating: 5.0
Star Kid (1997) with rating: 5.0

Five movies to not watch (bottom): 
3 Ninjas: High Noon At Mega Mountain (1998) with rating: 1.0
Amityville 1992: It's About Time (1992) with rating: 1.0
Amityville: A New Generation (1993) with rating: 1.0
Amityville: Dollhouse (1996) with rating: 1.0
Babyfever (1994) with rating: 1.0

```

### Commentary
I made small changes to the getRecommendations function to adapt it to return either the top or bottom of the sorted recommendation list, according to what the user inputs for the t_or_b parameter. I incorporated my earlier function, myTopChosenMatches. The function getRecommendations computes all of the ratings for the films that substitute me did not see, which is many films. I have seen the number one recommended movie for substitute me, which is Prefontaine, and I really enjoy that movie. 

## Q4
Choose my favorite and least favorite films from the list.
- **for each film, generate a list of the top five most correlated and bottom five least correlated films (20 in total)**

### Code/Outputs
```python
from recommendations import sim_pearson, sim_distance, transformPrefs

# FUNCTIONS THAT I CHANGED/REWORKED FROM recommendations.py
'''
myLoadMovieLens(path = '')
    - increased functionality by adding in the loading in of users data from u.user
    returns the preferences and the users, both dictionaries
'''
def myLoadMovieLens(path=''):
    # for conciseness, not shown here. shown in Q1 code block

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

print('five most similar movies to my least favorite movie, ', LEAST_FAV_MOVIE, '\n')
for similarity, movie in similar_least_fav:
    print(f'{movie} with similarity score of: {similarity}')
print('-'*100)

print('five least similar movies to my least favorite movie, ', LEAST_FAV_MOVIE, '\n')
for similarity, movie in least_similar_least_fav:
    print(f'{movie} with similarity score of: {similarity}')
print('-'*100)

```
Five most correlated and least correlated films:

```shell
(base) courtneymaynard@Courtneys-MacBook-Pro-2 homework7 % python3 question4_hw7.py

five most similar movies to my favorite movie,  Groundhog Day (1993) 

Wings of Courage (1995) with similarity score of: 1.0
Window to Paris (1994) with similarity score of: 1.0
Wife, The (1995) with similarity score of: 1.0
The Deadly Cure (1996) with similarity score of: 1.0
Someone Else's America (1995) with similarity score of: 1.0
----------------------------------------------------------------------------------------------------
five least similar movies to my favorite movie,  Groundhog Day (1993) 

A Chef in Love (1996) with similarity score of: 0
Aiqing wansui (1994) with similarity score of: 0
American Strays (1996) with similarity score of: 0
August (1996) with similarity score of: 0
B. Monkey (1998) with similarity score of: 0
----------------------------------------------------------------------------------------------------
five most similar movies to my least favorite movie,  Blade Runner (1982) 

Yankee Zulu (1994) with similarity score of: 1.0
Wonderland (1997) with similarity score of: 1.0
Woman in Question, The (1950) with similarity score of: 1.0
Window to Paris (1994) with similarity score of: 1.0
Wend Kuuni (God's Gift) (1982) with similarity score of: 1.0
----------------------------------------------------------------------------------------------------
five least similar movies to my least favorite movie,  Blade Runner (1982) 

American Strays (1996) with similarity score of: 0
August (1996) with similarity score of: 0
B. Monkey (1998) with similarity score of: 0
Babysitter, The (1995) with similarity score of: 0
Ballad of Narayama, The (Narayama Bushiko) (1958) with similarity score of: 0
----------------------------------------------------------------------------------------------------
```
### Commentary
I made changes to the calculateSimilarMovies function to add my parameter t_or_b, which will allow me to return the top or bottom of the similar items (most and least similar). I also simplified the function so that it would only return similar/dissimilar movies for one input movie at a time, rather than iterating through the entire list of movies, which was the functionality originally. I then computed the twenty movies and printed them cleanly. I find it interesting that the movies 'American Strays', 'August', and 'B. Monkey' are dissimilar from my favorite and least favorite movies on the list, and that 'Window to Paris' is similar to both my favorite and least favorite movie. This may indicate that my favorite and least favorite movies are not that different from each other! 

*Q: Based on your knowledge of the resulting films, do I agree with the results? Do I personally like/dislike the resulting films?*

I have never seen a single movie on this list of recommended movies, so I watched all of their trailers. 

**Supposed to Like:** 

*Wings of Courage:* https://www.youtube.com/watch?v=vixfv4tgxqA | I enjoy documentaries, but I don't like anything about war, so this movie would probably be a hit or miss for me.
  
*The Wife:* https://www.youtube.com/watch?v=vs5F7bYgglQ | I couldn't find the actual trailer, so I think this is just a scene from the movie. It is a little slow but the plot seems interesting. I wouldn't pick it as a top contender for movie I would watch.

*The Deadly Cure:* https://www.youtube.com/watch?v=gwl9bfy4qKg | I could not find any movie from 1996 called The Deadly Cure. Upon looking at the dataset, there is no other information given regarding this movie besides the name and release date. The closest I could find was Cure from 1997, which I have linked here. I typically enjoy psychological thrillers, so I do think I would like this movie. 

*Someone Else's America:* I was not able to find a trailer for this movie. Based on the description that it is a comedy-drama, I think I would like it. 

*The Babysitter:* https://www.youtube.com/watch?v=ZGNjF3YXmoo | I am not sure that I would enjoy this movie, it is a little raunchy for my tastes.

*The Ballad of Narayama (Narayama Bushiko):* https://www.youtube.com/watch?v=PCSpol_TJ7k | Though the trailer was not in English and didn't have subtitles, I looked up the movie description. It seems like it will be an emotional and impactful film and one I actually intend on watching. 

I do not agree with the results of the films that I would like, as only two of the movies really stood  out to me, The Ballad of Narayama and Cure, which may or may not be the movie that the dataset includes because I could not find record of The Deadly Cure anywhere.

---

**Supposed to DisLike:**

*A Chef in Love:* https://www.youtube.com/watch?v=InZ933U6Hx0 | I think this is the exact type of movie that I don't like. It's not really the style I enjoy and I don't generally like movies about war/revolution.

*Aiqing wansui:* https://www.youtube.com/watch?v=VqkTGmyXpDI | All of the searches for this movie brought me to a different movie, Vive L'Amour, which I have linked here. I do not think I would like this movie because of it's intimate romantic plot.

*Yankee Zulu:* https://www.youtube.com/watch?v=gUYyFdfBMnw | I think I would have really enjoyed this movie as a kid for it's ridiculous plot.

*Wonderland:* I could not find a trailer for this documentary, but I read some reviews and descriptions. I enjoy documentaries, and since it is described as a 'funny documentary', I think that I would enjoy this movie.

*The Woman In Question:* I couldn't find a trailer, but based on the descriptions, I think I would love this movie. I really enjoy detective movies, especially murder mysteries. 

*Wend Kuuni (God's Gift):* https://www.youtube.com/watch?v=gKkhubPAfm4 | This film seems impactful and interesting. I plan to watch it and think I will enjoy it.

I have mixed feelings about the results of the movies I am supposed to dislike (least similar to my favorite and most similar to my least favorite), as three of the films seem like movies I would enjoy. I was surprised to see no science fiction in these movies, as my least favorite movie from the list, Blade Runner, is a science fiction movie and I strongly dislike science fiction.

---

**Mixed Results on if I am Supposed to Like or Dislike:**

*American Strays:* https://www.youtube.com/watch?v=8TKRgXHmcCo | This movie seems really funny and I think I would enjoy it because I enjoy movies that are parodies/poke fun at stereotypes, like this one does with the American West.
  
*August:* https://www.youtube.com/watch?v=67QgTJDbYO4 | I don't think I would like this movie because I don't like period dramas.

*B. Monkey:* https://www.youtube.com/watch?v=SLfl0RiOvEM | Because I enjoy crime dramas, I think I would like this movie. 

*Window to Paris:* https://www.youtube.com/watch?v=S-fO805VDqI | This comedy film seems very funny and is a unique plot, so I think I would enjoy it.

Overall, I think I would enjoy 3 out of 4 of the films that are simultaneously recommended and not recommended to me.
