
#
# File: objecttier.py
#
# Builds Movie-related objects from data retrieved through
# the data tier.
#
# Original author:
#   Prof. Joe Hummel
#   U. of Illinois, Chicago
#   CS 341, Spring 2022
#   Project #02
#
# Name: Zaid Al-Zoubi
# UIN: 670498910
# Assignment: Project2 objecttier
import datatier


##################################################################
#
# Movie:
#
# Constructor(...)
# Properties:
#   Movie_ID: int
#   Title: string
#   Release_Year: string
#
class Movie: 
# intializing class
    def __init__(self, ID, TITLE, RELEASE_YEAR):
        self._Movie_ID = ID
        self._Title = TITLE
        self._Release_Year = RELEASE_YEAR

    @property #adding decorator and getters to make properties read only
    def Movie_ID(self):
        return self._Movie_ID

    @property
    def Title(self):
        return self._Title

    @property
    def Release_Year(self):
        return self._Release_Year


##################################################################
#
# MovieRating:
#
# Constructor(...)
# Properties:
#   Movie_ID: int
#   Title: string
#   Release_Year: string
#   Num_Reviews: int
#   Avg_Rating: float
#
class MovieRating(Movie): # inhereting Movie class
# intializing class
    def __init__(self, ID, TITLE, RELEASE_YEAR, N, A):
        self._Num_Reviews = N
        self._Avg_Rating = A
        Movie.__init__(self, ID, TITLE, RELEASE_YEAR)
#adding decorator and getters to make properties read only
    @property
    def Num_Reviews(self):
        return self._Num_Reviews

    @property
    def Avg_Rating(self):
        return self._Avg_Rating


##################################################################
#
# MovieDetails:
#
# Constructor(...)
# Properties:
#   Movie_ID: int
#   Title: string
#   Release_Date: string, date only (no time)
#   Runtime: int (minutes)
#   Original_Language: string
#   Budget: int (USD)
#   Revenue: int (USD)
#   Num_Reviews: int
#   Avg_Rating: float
#   Tagline: string
#   Genres: list of string
#   Production_Companies: list of string
#
class MovieDetails:
# intializing class
    def __init__(self, M, TI, R, RU, O, B, RE, N, A, T, G, P):
        self._Movie_ID = M
        self._Title = TI
        self._Release_Date = R
        self._Runtime = RU
        self._Original_Language = O
        self._Budget = B
        self._Revenue = RE
        self._Num_Reviews = N
        self._Avg_Rating = A
        self._Tagline = T
        self._Genres = G
        self._Production_Companies = P
#adding decorator and getters to make properties read only
    @property
    def Movie_ID(self):
        return self._Movie_ID

    @property
    def Title(self):
        return self._Title

    @property
    def Release_Date(self):
        return self._Release_Date

    @property
    def Runtime(self):
        return self._Runtime

    @property
    def Original_Language(self):
        return self._Original_Language

    @property
    def Budget(self):
        return self._Budget

    @property
    def Revenue(self):
        return self._Revenue

    @property
    def Num_Reviews(self):
        return self._Num_Reviews

    @property
    def Avg_Rating(self):
        return self._Avg_Rating

    @property
    def Tagline(self):
        return self._Tagline

    @property
    def Genres(self):
        return self._Genres

    @property
    def Production_Companies(self):
        return self._Production_Companies


##################################################################
#
# num_movies:
#
# Returns: # of movies in the database; if an error returns -1
#
def num_movies(dbConn): 
    sql = 'select count(Movie_ID) from Movies'
    row = datatier.select_one_row(dbConn, sql)
    if None in row:
        return -1
    if row == (): #if row is zero
      return 0
    return row[0]



##################################################################
#
# num_reviews:
#
# Returns: # of reviews in the database; if an error returns -1
#
def num_reviews(dbConn):
    sql = 'select count(Rating) from Ratings'
    row = datatier.select_one_row(dbConn, sql)
    if None in row: #if row is none
      return -1
    elif row == (): #if row is empty
      return -1
    return row[0]


############################################################ ABOVE IS CORRECT
##################################################################
#
# get_movies:
#
# gets and returns all movies whose name are "like"
# the pattern. Patterns are based on SQL, which allow
# the _ and % wildcards. Pass "%" to get all stations.
#
# Returns: list of movies in ascending order by name;
#          an empty list means the query did not retrieve
#          any data (or an internal error occurred, in
#          which case an error msg is already output).
#
def get_movies(dbConn, pattern):  #getting movie objects and appending to list
    Movie_list = []
    sql1 = 'select Movie_ID, Title, SUBSTR(Release_Date,1,4) from Movies where Title like ? order by Title'
    row = datatier.select_n_rows(dbConn, sql1,[pattern])
    if None in row:
        return []
    if len(row) == 0:
        return []
    for i in range(len(row)):
        M = Movie(row[i][0], row[i][1], row[i][2])
        Movie_list.append(M)
    return Movie_list


##################################################################
#
# get_movie_details:
#
# gets and returns details about the given movie; you pass
# the movie id, function returns a MovieDetails object. Returns
# None if no movie was found with this id.
#
# Returns: if the search was successful, a MovieDetails obj
#          is returned. If the search did not find a matching
#          movie, None is returned; note that None is also
#          returned if an internal error occurred (in which
#          case an error msg is already output).
#
def get_movie_details(dbConn, movie_id): # get one movie detail object and return it
    sql1 = 'select Title from Movies where Movie_ID = ?'
    check = datatier.select_one_row(dbConn, sql1, [movie_id])
    if None in check: #if movie isnt there then exit
        return None
    sql2 = 'select count(Rating) from Ratings where Movie_ID = ?'
    num = datatier.select_one_row(dbConn, sql2, [movie_id])
    numR = list(num)
    if numR[0] is None: #setting count to 0
        numR[0] = 0
    sql3 = 'select Avg(Rating) from Ratings where Movie_ID = ?'
    avg = datatier.select_one_row(dbConn, sql3, [movie_id])
    avg2 = list(avg)
    if avg2 == []:
        avg2[0] = 0.0
    elif avg2[0] is None: #setting average to 0
        avg2[0] = 0.0
    sql3 = 'select Movie_ID, Title, SUBSTR(Release_Date,1,10), Runtime, Original_Language, Budget, Revenue from Movies where Movie_ID = ?'
    piece0 = datatier.select_one_row(dbConn, sql3, [movie_id])
    piece = list(piece0)
    if piece == []:
        return None
    if piece[5] is None:
        piece[5] = 0
    if piece[6] is None:
        piece[6] = 0
    sql4 = 'select Tagline from Movie_Taglines where Movie_ID = ?'
    tagline = datatier.select_one_row(dbConn, sql4, [movie_id])
    if None in tagline:
        tagline2 = ("", None)
    elif len(tagline) == 0:
        tagline2 = ("",None)
    else:
        tagline2 = tagline
    sql5 = 'select Genres.Genre_Name from Movie_Genres join Genres on Genres.Genre_ID = Movie_Genres.Genre_ID and Movie_ID = ? order by Genres.Genre_Name'
    Genra = datatier.select_n_rows(dbConn, sql5, [movie_id])
    sql6 = 'select Companies.Company_Name from Movie_Production_Companies join Companies on Companies.Company_ID = Movie_Production_Companies.Company_ID AND Movie_Production_Companies.Movie_ID = ? order by Companies.Company_Name'
    Prod = datatier.select_n_rows(dbConn, sql6, [movie_id])
    Prod_list = []
    if None in Prod:
        Prod_list = []
    else:
        for i in range(len(Prod)):
            Prod_list.append(Prod[i][0])
    Genra_list = []
    if None in Genra:
        Genra_list = []
    else:
        for i in range(len(Genra)):
            Genra_list.append(Genra[i][0])
    MD = MovieDetails(piece[0], piece[1], piece[2], piece[3], piece[4],
                      piece[5], piece[6], numR[0], avg2[0], tagline2[0],
                      Genra_list, Prod_list)
    return MD #return Movie details object
################################################################## FUNCTION ABOVE IS CORRECT
#
# get_top_N_movies:
#
# gets and returns the top N movies based on their average
# rating, where each movie has at least the specified # of
# reviews. Example: pass (10, 100) to get the top 10 movies
# with at least 100 reviews.
#
# Returns: returns a list of 0 or more MovieRating objects;
#          the list could be empty if the min # of reviews
#          is too high. An empty list is also returned if
#          an internal error occurs (in which case an error
#          msg is already output).
#
#error seems to be here avg rating can't be with count rating check online.
def get_top_N_movies(dbConn, N, min_num_reviews):  # getting top movies
    top = []
    sql1 = 'select Movies.Movie_ID,Movies.Title,SUBSTR(Movies.Release_Date,1,4),count(Rating), Avg(Rating) from Ratings join Movies on Ratings.Movie_ID = Movies.Movie_ID group by Movies.Movie_ID Having count(Rating) >= ? order by Avg(Rating) desc limit ?'
    ans = datatier.select_n_rows(dbConn, sql1,[min_num_reviews,N])
    if None in ans:
        return [] #if none return empty list
    if ans == []:
        return []
    for i in range(len(ans)):
        M = MovieRating(ans[i][0], ans[i][1], ans[i][2], ans[i][3], ans[i][4])
        top.append(M)
    return top
##################################################################
#
# add_review:
#
# Inserts the given review --- a rating value 0..10 --- into
# the database for the given movie. It is considered an error
# if the movie does not exist (see below), and the review is
# not inserted.
#
# Returns: 1 if the review was successfully added, returns
#          0 if not (e.g. if the movie does not exist, or if
#          an internal error occurred).
#

def add_rating(dbConn, movie_id, rating): #adding review
    chec = 'select Movie_id from Movies where Movie_ID = ?'
    check0 = datatier.select_one_row(dbConn, chec, [movie_id])
    check = list(check0) 
    if None in check: # returning 0 to indicate movie doesn't exist
        return 0
    if check == []:
        return 0 
    sql1 = 'Insert Into Ratings(Rating,Movie_ID) VALUES (?, ?)'
    ans1 = datatier.perform_action(dbConn, sql1,[rating,movie_id])
    return ans1

##################################################################


def add_review(dbConn, movie_id, review):
    # Check if the movie exists
    sql = 'SELECT Movie_ID FROM Movies WHERE Movie_ID = ?'
    result = datatier.select_one_row(dbConn, sql, [movie_id])
    if result is None:
        return False

    # Insert the review into the Reviews table
    sql = 'INSERT INTO Reviews (Movie_ID, Review) VALUES (?, ?)'
    success = datatier.insert_row(dbConn, sql, [movie_id, review])
    if not success:
        return False

    # Update the movie's number of reviews
    sql = 'SELECT COUNT(Review) FROM Reviews WHERE Movie_ID = ?'
    result = datatier.select_one_row(dbConn, sql, [movie_id])
    num_reviews = result[0]

    # sql = 'UPDATE Movies SET Num_Reviews = ? WHERE Movie_ID = ?'
    # success = datatier.update_row(dbConn, sql, [num_reviews, movie_id])
    return success

def get_reviews(dbConn, movie_id):
    # Check if the movie exists
    sql = 'SELECT Movie_ID FROM Movies WHERE Movie_ID = ?'
    result = datatier.select_one_row(dbConn, sql, [movie_id])
    if result is None:
        return None

    # Retrieve all the reviews for the movie
    sql = 'SELECT Review FROM Reviews WHERE Movie_ID = ?'
    reviews = datatier.select_all_rows(dbConn, sql, [movie_id])
    return reviews
