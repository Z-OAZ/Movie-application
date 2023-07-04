import sqlite3
from flask import Flask, render_template, request, url_for, redirect
import objecttier

# Command functions
def Gen(dbConn):
    num_movies = objecttier.num_movies(dbConn)
    num_reviews = objecttier.num_reviews(dbConn)
    stats = []
    stats.append(num_movies)
    stats.append(num_reviews)
    return stats
def cmnd1(dbConn):
    name = input("\nEnter movie name (wildcards _ and % supported): ")
    movies = objecttier.get_movies(dbConn, name)
    movie_list = []
    for m in movies:
        movie_list.append([m.Movie_ID, m.Title, m.Release_Year])
    return movie_list

def cmnd2(dbConn):
    movie_id = input('\nEnter movie id: ')
    MD = objecttier.get_movie_details(dbConn, movie_id)
    if MD is None:
        return None
    movie_details = []
    movie_details.append([str(MD.Movie_ID), MD.Title])
    movie_details.append(['Release date', MD.Release_Date])
    movie_details.append(['Runtime', str(MD.Runtime) + ' (mins)'])
    movie_details.append(['Orig language', MD.Original_Language])
    movie_details.append(['Budget', '$' + '{:,}'.format(MD.Budget) + ' (USD)'])
    movie_details.append(['Revenue', '$' + '{:,}'.format(MD.Revenue) + ' (USD)'])
    movie_details.append(['Num reviews', str(MD.Num_Reviews)])
    movie_details.append(['Avg rating', '{:.2f}'.format(MD.Avg_Rating) + ' (0..10)'])
    movie_details.append(['Genres', ', '.join(MD.Genres)])
    movie_details.append(['Production companies', ', '.join(MD.Production_Companies)])
    return movie_details

def cmnd3(dbConn):
    amount = int(input('\nN? '))
    if amount <= 0:
        print('Please enter a positive value for N...')
        return None
    min = int(input('min number of reviews? '))
    if min <= 0:
        print('Please enter a positive value for min number of reviews...')
        return None
    Rev = objecttier.get_top_N_movies(dbConn, amount, min)
    if not Rev:
        return None
    top_movies = []
    for r in Rev:
        top_movies.append([
            str(r.Movie_ID),
            r.Title,
            '(' + str(r.Release_Year) + ')',
            'avg rating =' + '{:.2f}'.format(r.Avg_Rating),
            '(' + str(r.Num_Reviews) + ' reviews)'
        ])
    return top_movies

def cmnd4(dbConn):
    rating = int(input('\nEnter rating (0..10): '))
    if rating > 10 or rating < 0:
        print('Invalid rating...')
        return None
    movie_id = input('Enter movie id: ')
    fetch = objecttier.add_rating(dbConn, movie_id, rating)
    if fetch == 0:
        return 'No such movie...'
    return 'Review successfully inserted'

def cmnd5(dbConn):
    tagline = input('\ntagline? ')
    movie_id = input('movie id? ')
    fetch = objecttier.set_tagline(dbConn, movie_id, tagline)
    if fetch == 0:
        return 'No such movie...'
    return 'Tagline successfully set'

# Flask app and routes
app = Flask(__name__)

# Route definitions
@app.route('/')
def home():
    dbConn = sqlite3.connect('MovieLens.db')
    stats = Gen(dbConn)
    return render_template('index.html', num_movies=stats[0], num_reviews=stats[1])
@app.route('/commands')
def commands():
    return render_template('commands.html')
@app.route('/search_movies', methods=['GET', 'POST'])
def search_movies():
    if request.method == 'POST':
        pattern = request.form['pattern']
        dbConn = sqlite3.connect('MovieLens.db')
        movies = objecttier.get_movies(dbConn, pattern)
        movie_list = []
        for m in movies:
            movie_list.append({'Movie_ID': m.Movie_ID, 'Title': m.Title, 'Release_Year': m.Release_Year})
        if len(movie_list) == 0:
            no_movie_found = True
        else:
            no_movie_found = False
        return render_template('movies.html', movies=movie_list, no_movie_found=no_movie_found)
    return render_template('search_movies.html')


@app.route('/movie_details', methods=['GET', 'POST'])
def movie_details():
    if request.method == 'POST':
        movie_id = request.form['movie_id']
        dbConn = sqlite3.connect('MovieLens.db')
        movie_details = objecttier.get_movie_details(dbConn, movie_id)
        if movie_details is None:
            movie_details = []
        else:
            details_list = []
            details_list.append([str(movie_details.Movie_ID), movie_details.Title])
            details_list.append(['Release date', movie_details.Release_Date])
            details_list.append(['Runtime', str(movie_details.Runtime) + ' (mins)'])
            details_list.append(['Orig language', movie_details.Original_Language])
            details_list.append(['Budget', '$' + '{:,.2f}'.format(movie_details.Budget) + ' (USD)'])
            details_list.append(['Revenue', '$' + '{:,.2f}'.format(movie_details.Revenue) + ' (USD)'])
            details_list.append(['Number of ratings', str(movie_details.Num_Reviews)])
            details_list.append(['Avg rating', '{:.2f}'.format(movie_details.Avg_Rating) + ' (0..10)'])
            details_list.append(['Genres', ', '.join(movie_details.Genres)])
            details_list.append(['Production companies', ', '.join(movie_details.Production_Companies)])
            movie_details = details_list
        
        return render_template('movie_details.html', movie_details=movie_details)
    
    return render_template('get_movie_details.html')


@app.route('/top_movies', methods=['GET', 'POST'])
def top_movies():
    if request.method == 'POST':
        amount = int(request.form['amount'])
        min_reviews = int(request.form['min_reviews'])
        dbConn = sqlite3.connect('MovieLens.db')
        top_movies = objecttier.get_top_N_movies(dbConn, amount, min_reviews)
        top_movies_list = []
        if not top_movies:
            top_movies_list = []
        else:
            for r in top_movies:
                avg_rating = '{:.2f}'.format(r.Avg_Rating) if r.Avg_Rating is not None else 'N/A'
                top_movies_list.append([
                    str(r.Movie_ID),
                    r.Title,
                    '(' + str(r.Release_Year) + ')',
                    'Average rating: ' + avg_rating,
                    '(' + str(r.Num_Reviews) + ' reviews)'
                ])
        return render_template('top_movies.html', top_movies=top_movies_list)
    return render_template('get_top_movies.html')

@app.route('/add_rating', methods=['GET', 'POST'])
def add_rating():
    if request.method == 'POST':
        rating = int(request.form['rating'])
        movie_id = request.form['movie_id']
        dbConn = sqlite3.connect('MovieLens.db')
        movie_exists = objecttier.get_movie_details(dbConn, movie_id)

        if movie_exists:
            objecttier.add_rating(dbConn, movie_id, rating)
            return redirect(url_for('rating_success'))
        else:
            return redirect(url_for('no_movie'))

    return render_template('add_rating.html')



@app.route('/add_review', methods=['GET', 'POST'])
def add_review():
    if request.method == 'POST':
        name = request.form['name']
        movie_id = request.form['movie_id']
        review = request.form['review']
        concatenated_review = name + ': ' + review  # Concatenate the name and review
        dbConn = sqlite3.connect('MovieLens.db')
        success = objecttier.add_review(dbConn, movie_id, concatenated_review)
        if success:
            return redirect(url_for('review_success'))
        else:
            return redirect(url_for('no_movie'))
    return render_template('add_review.html')


@app.route('/view_review', methods=['GET', 'POST'])
def view_review():
    lst = []
    if request.method == 'POST':
        movie_id = request.form['movie_id']
        dbConn = sqlite3.connect('MovieLens.db')
        reviews = objecttier.get_reviews(dbConn, movie_id)
        for r in reviews:
            lst.append(r[0])
        if reviews:
            return redirect(url_for('reviews', reviews=lst))
        else:
            return redirect(url_for('reviews'))
    return render_template('view_review.html')

@app.route('/reviews')
def reviews():
    reviews = request.args.getlist('reviews')  # Retrieve reviews as a list
    return render_template('reviews.html', reviews=reviews)

@app.route('/review_success')
def review_success():
    message = 'Review successfully added'
    return render_template('review_success.html', message=message)


    
@app.route('/no_movie')
def no_movie():
    message = 'No such movie...'
    return render_template('no_movie.html', message=message)

@app.route('/rating_success')
def rating_success():
    message = 'Rating successfully inserted'
    return render_template('rating_inserted.html', message=message)


if __name__ == '__main__':
    app.run()
