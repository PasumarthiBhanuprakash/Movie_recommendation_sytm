from flask import Flask, render_template, request, jsonify
import pandas as pd
import difflib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Load dataset from online
movie_data = pd.read_csv(
    "https://raw.githubusercontent.com/YBI-Foundation/Dataset/main/Movies%20Recommendation.csv"
)

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
        return []

    close_match = find_close_match[0]
    index_of_movie = movie_data[movie_data.title == close_match].index[0]

    similarity_score = list(enumerate(similarity[index_of_movie]))
    sorted_movies = sorted(similarity_score, key=lambda x: x[1], reverse=True)

    recommended = []
    for movie in sorted_movies[1:11]:
        recommended.append(movie_data.iloc[movie[0]]['title'])

    return recommended

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/recommend", methods=["POST"])
def get_recommendations():
    data = request.get_json()
    movie_name = data.get("movie_name")
    results = recommend(movie_name)
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)
