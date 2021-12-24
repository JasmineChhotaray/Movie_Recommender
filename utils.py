from fuzzywuzzy import process
import pandas as pd

# put the movieId into the row index!
ratings = pd.read_csv('./data/ml-latest-small/ratings.csv')
movies = pd.read_csv('./data/ml-latest-small/movies.csv', index_col=0) 
#movie_average_rating = None
movie_item_matrix = None


def lookup_movie(search_query, titles):
    """
    given a search query, uses fuzzy string matching to search for similar 
    strings in a pandas series of movie titles

    returns a list of search results. Each result is a tuple that contains 
    the title, the matching score and the movieId.
    """
    matches = process.extractBests(search_query, titles)
    # [(title, score, movieId), ...]
    return matches


def get_watched_movies(userId):
    """
    It gets the userId and returns the list of movies rated by that particular user.
    (The user has given ratings means he/she has already watched it.)
    """
    watched_movies = ratings.loc[ratings['userId'] == userId]['movieId']
    return list(watched_movies) 

def movie_average_rating():
    # Count no. of ratings for each movie
    count_ratings = ratings.groupby('movieId').count()
    # throw away movies that have been rated by less than 100 users
    more_than_100_ratings = count_ratings.loc[count_ratings['rating'] >= 100]
    filtered_ratings_dataset = ratings[ratings['movieId'].isin(more_than_100_ratings.index)]
    avg_rating = filtered_ratings_dataset.groupby('movieId').mean().sort_values('rating', ascending=False).drop(columns = 'timestamp')

    return avg_rating

def get_movie_ids(movie_names):
    movie_ids = []

    for name in movie_names:
        matches = lookup_movie(name, movies['title'])
        movie_id = matches[0][2]
        movie_ids.append(movie_id)
    return movie_ids

def get_ratings(ratings):
    rating_list = []

    for rating in ratings:
        rating_list.append(int(rating))

    return rating_list

if __name__ == '__main__':
    results = lookup_movie('star wars', movies['title'])
    #print(results)
    user_ratings = get_watched_movies(1)
    #print(user_ratings)
    print(movie_average_rating())

