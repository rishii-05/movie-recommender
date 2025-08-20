import streamlit as st
import pickle
import pandas as pd

# Function to recommend movies
def recommend(movie):
    # Find the index of the movie that matches the title
    movie_index = movies[movies['title'] == movie].index[0]
    
    # Get the similarity scores for that movie with all other movies
    distances = similarity[movie_index]
    
    # Sort the movies based on similarity scores in descending order
    # We skip the first element [1:6] because it will be the movie itself (similarity of 1)
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommended_movies = []
    for i in movies_list:
        # Get the title of the recommended movie from its index
        recommended_movies.append(movies.iloc[i[0]].title)
    return recommended_movies

# --- App Layout ---

# Set the title of the web app
st.title('Movie Recommender System')

# Load the processed movie data and similarity matrix from the saved files
try:
    movies_dict = pickle.load(open('artifacts/movie_dict.pkl', 'rb'))
    movies = pd.DataFrame(movies_dict)
    similarity = pickle.load(open('artifacts/similarity.pkl', 'rb'))
except FileNotFoundError:
    st.error("Model files not found. Please make sure 'movie_dict.pkl' and 'similarity.pkl' are in the 'artifacts' folder.")
    st.stop()


# Create the movie selection dropdown with a placeholder
# We set index=None to ensure no movie is selected by default
selected_movie_name = st.selectbox(
    'Select a movie you like, and we will recommend similar ones!',
    movies['title'].values,
    index=None,
    placeholder="Select a movie..."
)

# Create a button that the user will click to get recommendations
if st.button('Recommend'):
    # Check if the user has selected a movie from the dropdown
    if selected_movie_name:
        # If a movie is selected, call the recommend function
        recommendations = recommend(selected_movie_name)
        st.write('Here are your recommendations:')
        # Display the list of recommended movies
        for movie in recommendations:
            st.write(f"- {movie}")
    else:
        # If no movie is selected, show a message
        st.warning("Please select a movie first to get recommendations.")

