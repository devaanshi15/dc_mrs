
import streamlit as st
import pickle
import pandas as pd
import requests
import certifi

# Custom CSS for an elegant movie recommendation app
st.markdown("""
    <style>
    /* General Background and Font Styles */
    body {
        background-color: #1e1e1e;
        color: white;
        font-family: 'Helvetica Neue', sans-serif;
    }

    /* Main App Title */
    .main h1 {
        color: #f39c12;
        font-size: 3em;
        text-align: center;
        font-weight: 600;
        margin-bottom: 20px;
    }

    /* Movie Title Styling */
    .movie-title {
        font-size: 16px;
        font-weight: bold;
        text-align: center;
        color: #f39c12;
        margin-top: 10px;
    }

    /* Column Layout and Poster Styling */
    .stImage {
        display: flex;
        justify-content: center;
        margin: 0 auto;
        transition: transform 0.3s ease;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.6);
    }

    /* Hover Effect for Posters */
    .stImage:hover {
        transform: scale(1.05);
    }

    /* Buttons Styling */
    .stButton>button {
        background-color: #e74c3c;
        color: white;
        font-size: 16px;
        padding: 10px 24px;
        border-radius: 8px;
        border: none;
        margin-top: 20px;
        font-weight: bold;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }

    /* Button Hover Effect */
    .stButton>button:hover {
        background-color: #c0392b;
    }

    /* Dropdown Styling */
    .stSelectbox {
        font-size: 16px;
        color: black;
    }

    /* Align Content Centered */
    .main {
        padding-top: 50px;
        max-width: 1200px;
        margin: 0 auto;
    }
    </style>
    """, unsafe_allow_html=True)


def fetch_poster(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=5e82b4d611ee8df116118cc3a236c36b&language=en-US'.format(
            movie_id), verify=False)
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommend_movies = []
    recommend_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommend_movies.append(movies.iloc[i[0]].title)
        recommend_movies_posters.append(fetch_poster(movie_id))
    return recommend_movies, recommend_movies_posters


movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    "Enter the movie name to get the top 5 recommendations:",
    movies['title'].values)

if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.markdown(f"<div class='movie-title'>{names[0]}</div>", unsafe_allow_html=True)
        st.image(posters[0], use_column_width=True)
    with col2:
        st.markdown(f"<div class='movie-title'>{names[1]}</div>", unsafe_allow_html=True)
        st.image(posters[1], use_column_width=True)
    with col3:
        st.markdown(f"<div class='movie-title'>{names[2]}</div>", unsafe_allow_html=True)
        st.image(posters[2], use_column_width=True)
    with col4:
        st.markdown(f"<div class='movie-title'>{names[3]}</div>", unsafe_allow_html=True)
        st.image(posters[3], use_column_width=True)
    with col5:
        st.markdown(f"<div class='movie-title'>{names[4]}</div>", unsafe_allow_html=True)
        st.image(posters[4], use_column_width=True)

