from flask import Flask, Response, request, jsonify, render_template, url_for
from utils import movies, lookup_movie, movie_average_rating,get_watched_movies
from recommender import recommend_most_popular, recommend_random, recommend_cosine


movie_item_avg = movie_average_rating()

# here we construct a Flack object and the __name__ sets this script as the root
app = Flask(__name__)

# a python decorator for defining a mapping between a url and a function
@app.route('/')
def homepage():
    return render_template('search.html', title="Movie Recommeneder")



@app.route('/rate')
def ratepage():
    return render_template('rate.html', title="Movie Recommeneder" )

# dynamic parametrized endpoint
@app.route('/movies/<int:movieId>')
def movie_info(movieId):
    try:
        movie=movies.loc[movieId].to_dict()
        return render_template('movie_info.html', movie=movie)
    except KeyError:
        # return Response(status=404)
        return 'movie id does not exist!'


@app.route('/movies/search')
def movie_search():
    # QUERY STRINGS: https://en.wikipedia.org/wiki/Query_string

    # ?q=titanic&q=indiana%20jones&q=star%20wars
    # print(request.args.getlist('q'))
    
    # ?q=titanic
    query = request.args.get('q')
    results = lookup_movie(query, movies['title'])
    return render_template('search.html', results=results)

@app.route('/movies/recommend')
def recommend():
    print(request.args)
    # recommend_most_popular(movie_average_rating)
    queries = request.args.getlist('movie')
    user_ratings = request.args.getlist('rating')

    userId = request.args.get('user_id') 
    movie_ids = []

    for query in queries:
        matches = lookup_movie(query, movies['title'])
        movie_id = matches[0][2]
        movie_ids.append(movie_id)
        
    ratings = [int(rating) for rating in user_ratings]

    # recommended list of movie ids
    recommendations_pop = recommend_most_popular(userId, movie_item_avg) 
    #recommendations = recommend_random(liked_items=movie_ids, k=5) ----
    # recommend_nmf(liked_items, ratings, k=5)
    recommendations_norm = recommend_cosine(queries, ratings, k=5)

    # get movie titles from recommendations
    normal_titles = recommendations_norm['title']
    popular_titles = recommendations_pop['title']

    # here would be a great place to use your recommender function
    # rec = recommend_random([3,45]) then pass rec=rec to recommend.html
    return render_template('rate.html', normaltitles=normal_titles, populartitles=popular_titles)




if __name__ == "__main__":
    # runs app and debug=True ensures that when we make changes the web server restarts
    app.run(debug=True)
