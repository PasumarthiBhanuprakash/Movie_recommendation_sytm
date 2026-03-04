from flask import Flask, render_template, request
import pandas as pd
import difflib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Load dataset from online source
movie_data = pd.read_csv("https://raw.githubusercontent.com/YBI-Foundation/Dataset/main/Movies%20Recommendation.csv")

selected_features = ['genres','keywords','tagline','cast','director']

for feature in selected_features:
    movie_data[feature] = movie_data[feature].fillna('')

combined_features = (
    movie_data['genres'] + ' ' +
    movie_data['keywords'] + ' ' +
    movie_data['tagline'] + ' ' +
    movie_data['cast'] + ' ' +
    movie_data['director']
)

vectorizer = TfidfVectorizer()
feature_vectors = vectorizer.fit_transform(combined_features)

similarity = cosine_similarity(feature_vectors)

def recommend(movie_name):
    list_of_all_titles = movie_data['title'].tolist()
    find_close_match = difflib.get_close_matches(movie_name, list_of_all_titles)

    if not find_close_match:
        return ["Movie not found. Please try another name."]

    close_match = find_close_match[0]
    index_of_the_movie = movie_data[movie_data.title == close_match].index[0]

    similarity_score = list(enumerate(similarity[index_of_the_movie]))
    sorted_similar_movies = sorted(similarity_score, key=lambda x: x[1], reverse=True)

    recommended_movies = []

    for movie in sorted_similar_movies[1:11]:
        index = movie[0]
        title = movie_data.iloc[index]['title']
        recommended_movies.append(title)

    return recommended_movies


@app.route("/", methods=["GET", "POST"])
def home():
    recommendations = []
    if request.method == "POST":
        movie_name = request.form["movie_name"]
        recommendations = recommend(movie_name)

    return render_template("index.html", recommendations=recommendations)


if __name__ == "__main__":
    app.run(debug=True)
