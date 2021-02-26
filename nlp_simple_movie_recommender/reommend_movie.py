# Read in movies file
f = open('movies.txt', 'r+')

movies = f.read()

movies = movies.split("\n")

# Import and load spacy
import spacy
nlp = spacy.load('en_core_web_md')

# Create Planet Hulk description string
print("This simple application will recommend a movie from a defined list of movies based on their blurb descriptions.")
print("\n")
hulk = input("Enter blurb for a movie: ")
print("\n")

# Apply NLP to hulk
hulk_movie = nlp(hulk)

# Define function to find most similar movie
def recommend_movie():
    current_largest_score = 0 # initialize variable
    for movie in movies:
        m = movie.split(" :") # seperate movie titles from movie description
        score = (nlp(m[1])).similarity(hulk_movie) # get the similarity score
        if (score > current_largest_score):
            current_largest_score = score
            most_similar_movie = m[0]
    print("Most similar movie:", most_similar_movie, " - Similarity score:", round(current_largest_score, ndigits=4))

# Execute the function
recommend_movie()
