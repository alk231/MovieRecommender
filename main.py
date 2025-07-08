import streamlit as st
import requests

# Load movie data and similarity matrix
import gzip
import pickle

with gzip.open('movies.pkl.gz', 'rb') as f:
    movies_data = pickle.load(f)

with gzip.open('similarity.pkl.gz', 'rb') as f:
    movies_similarity = pickle.load(f)


st.markdown(
    """
    <style>
    div[data-baseweb="select"] > div {
        cursor: pointer;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# Fetch poster from TMDB
import time

def fetch_poster(movie_id, retries=3, delay=1):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=bfce2fc336baec9af3883a9940ebbd89"
    
    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                poster_path = data.get('poster_path')
                if poster_path:
                    return "https://image.tmdb.org/t/p/w500" + poster_path
                else:
                    return None
            else:
                print(f"Attempt {attempt+1}: Status code {response.status_code}")
        except Exception as e:
            print(f"Attempt {attempt+1} failed: {e}")
        
        time.sleep(delay)  # wait before retrying
    
    return None


# Get top 5 recommended movie IDs and titles
def get_reccomendations(movie_title):
    movie_index = movies_data[movies_data['title'] == movie_title].index[0]
    distance = movies_similarity[movie_index]
    movie_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommended_movies = []
    for i in movie_list:
        movie_id = movies_data.iloc[i[0]].id
        movie_title = movies_data.iloc[i[0]].title
        recommended_movies.append((movie_title, movie_id))
    return recommended_movies

# Streamlit UI
st.title("Movie Recommender System")

option = st.selectbox('Choose a movie:', movies_data['title'])

if st.button("Recommend"):
    recommendations = get_reccomendations(option)
    
    for title, movie_id in recommendations:
        poster_url = fetch_poster(movie_id)
        st.subheader(title)
        if poster_url:
            st.image(poster_url)
        else:
            st.write("Poster not available")
