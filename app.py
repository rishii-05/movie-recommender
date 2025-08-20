import streamlit as st
import pickle
import pandas as pd

# Function to recommend movies
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommended_movies = []
    for i in movies_list:
        recommended_movies.append(movies.iloc[i[0]].title)
    return recommended_movies

# Load the movie data and similarity matrix
movies_dict = pickle.load(open('artifacts/movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('artifacts/similarity.pkl', 'rb'))

# Streamlit app layout
st.title('Movie Recommender System')

# Movie selection dropdown
selected_movie_name = st.selectbox(
    'Select a movie you like, and we will recommend similar ones!',
    movies['title'].values
)

# Recommend button
if st.button('Recommend'):
    recommendations = recommend(selected_movie_name)
    st.write('Here are your recommendations:')
    for movie in recommendations:
        st.write(movie)