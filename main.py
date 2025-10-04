import streamlit as st
import requests
import gzip
import pickle
import os
import time

# ------------------------------
# File paths (works locally & on Render)
# ------------------------------
BASE_DIR = os.path.dirname(__file__)
MOVIES_FILE = os.path.join(BASE_DIR, 'movies.pkl')
SIMILARITY_FILE = os.path.join(BASE_DIR, 'similarity.pkl')

# ------------------------------
# Load movie data and similarity matrix
# ------------------------------
try:
    with gzip.open(MOVIES_FILE, 'rb') as f:
        movies_data = pickle.load(f)
except FileNotFoundError:
    st.error(f"Could not find {MOVIES_FILE}. Make sure it is in the repo.")
    st.stop()

try:
    with gzip.open(SIMILARITY_FILE, 'rb') as f:
        movies_similarity = pickle.load(f)
except FileNotFoundError:
    st.error(f"Could not find {SIMILARITY_FILE}. Make sure it is in the repo.")
    st.stop()

# ------------------------------
# Custom CSS
# ------------------------------
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

# ------------------------------
# Fetch poster from TMDB
# ------------------------------
TMDB_API_KEY = "bfce2fc336baec9af3883a9940ebbd89"

def fetch_poster(movie_id, retries=3, delay=1):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}"
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
        time.sleep(delay)
    return None

# ------------------------------
# Get top 5 recommended movies
# ------------------------------
def get_recommendations(movie_title):
    try:
        movie_index = movies_data[movies_data['title'] == movie_title].index[0]
    except IndexError:
        return []
    
    distances = movies_similarity[movie_index]
    top_indices = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommendations = []
    for i in top_indices:
        movie_id = movies_data.iloc[i[0]].id
        title = movies_data.iloc[i[0]].title
        recommendations.append((title, movie_id))
    return recommendations

# ------------------------------
# Streamlit UI
# ------------------------------
st.title("Movie Recommender System 🎬")

option = st.selectbox('Choose a movie:', movies_data['title'])

if st.button("Recommend"):
    recommendations = get_recommendations(option)
    
    if not recommendations:
        st.warning("No recommendations found!")
    
    for title, movie_id in recommendations:
        poster_url = fetch_poster(movie_id)
        st.subheader(title)
        if poster_url:
            st.image(poster_url)
        else:
            st.write("Poster not available")
