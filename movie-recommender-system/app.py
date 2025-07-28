import streamlit as st
import pickle
import pandas as pd

# Load data
movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Ensure no extra spaces in movie titles



# Recommendation function
def recommend(movie):
    if movie not in movies['title'].values:
        st.error("Selected movie not found in database!")
        return []

    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    for i in movie_list:
        title = movies.iloc[i[0]].title
        if not isinstance(title, str) or title.strip() == "":
            st.warning(f"Invalid title found for index {i[0]}, skipping...")
            continue
        recommended_movies.append(title.strip())
    return recommended_movies


# Streamlit Page Config
st.set_page_config(page_title="🎬 Movie Recommender", layout="wide")

# Custom CSS
st.markdown("""
    <style>
        .movie-card {
            background-color: #f9f9f9;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 10px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            color: #000000; /* FIX: text color */
            font-size: 20px;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)


# App Title
st.markdown("<h1 class='title'>🎥 Movie Recommender System</h1>", unsafe_allow_html=True)
st.write("Get movie recommendations based on your favorite film!")

# Sidebar
st.sidebar.header("Choose Your Movie 🎬")
selected_movie_name = st.sidebar.selectbox("Select a movie:", movies['title'].values)

# Recommend Button
if st.sidebar.button('Recommend'):
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<h2 class='recommend-title'>📽 Recommended Movies:</h2>", unsafe_allow_html=True)

    recommendations = recommend(selected_movie_name)

    if recommendations:
        for movie in recommendations:
            st.markdown(f"<div class='movie-card'>🎬 {movie}</div>", unsafe_allow_html=True)
else:
    st.sidebar.info("Select a movie and click 'Recommend' to get started!")


