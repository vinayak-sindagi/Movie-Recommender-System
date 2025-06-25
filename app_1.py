import streamlit as st
import pickle
import pandas as pd
import requests
import time


def fetch_poster(movie_id):
    # Properly format the API request URL
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'

    # Add a user-agent header to avoid bot blocking
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    # Retry logic with timeout and error handling
    retries = 3
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()  # Will raise HTTPError if the response code is 4xx/5xx
            data = response.json()
            return f'https://image.tmdb.org/t/p/w500{data["poster_path"]}'  # Return the poster URL
        except requests.exceptions.RequestException as e:
            print(f"Error fetching poster for movie {movie_id}: {e}")
            if attempt < retries - 1:
                time.sleep(2)  # Retry after 2 seconds
            else:
                return None  # Return None if max retries reached


def recommend(movie):
    # Find the index of the selected movie in the dataframe
    movie_index = movies[movies['title'] == movie].index[0]

    # Get the distances (similarity scores) for the selected movie
    distances = similarity[movie_index]

    # Get the top 5 most similar movies, sorted by distance (ignore the first one as it's the selected movie itself)
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommend_movies = []
    recommend_movies_posters = []

    # Loop through the recommended movies and fetch their posters
    for i in movies_list:
        movie_id = movies.iloc[i[0]]['id']
        recommend_movies.append(movies.iloc[i[0]].title)
        poster = fetch_poster(movie_id)  # Fetch the poster for the recommended movie
        recommend_movies_posters.append(poster)

    return recommend_movies, recommend_movies_posters  # Return both movie names and posters


# Load movie data and similarity matrix
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))  # This is the entire dataframe
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

# Streamlit UI
st.title('Movie Recommender System')
selected_movie_name = st.selectbox('Select a movie', movies['title'].values)

if st.button('Recommend Movies'):
    # Get the recommended movies and their posters
    names, posters = recommend(selected_movie_name)

    # Display the recommended movies and their posters in a 5-column layout
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.header(names[0])
        if posters[0]:
            st.image(posters[0])
        else:
            st.write("Poster not available")

    with col2:
        st.header(names[1])
        if posters[1]:
            st.image(posters[1])
        else:
            st.write("Poster not available")

    with col3:
        st.header(names[2])
        if posters[2]:
            st.image(posters[2])
        else:
            st.write("Poster not available")

    with col4:
        st.header(names[3])
        if posters[3]:
            st.image(posters[3])
        else:
            st.write("Poster not available")

    with col5:
        st.header(names[4])
        if posters[4]:
            st.image(posters[4])
        else:
            st.write("Poster not available")
