# Movie Recommender

A movie recommendation system that suggests films based on your preferences. Built with Python and collaborative filtering techniques.

## What it does

Give it a movie you like, and it'll suggest similar ones you might enjoy. The recommendations are based on patterns from thousands of user ratings and movie metadata like genres, cast, and plot keywords.

## Getting started

**Install requirements:**
```bash
pip install pandas numpy scikit-learn streamlit
```

**Run the app:**
```bash
streamlit run app.py
```

The web interface will open in your browser.

## How to use

1. Type in a movie title you enjoyed
2. Hit enter or click the recommend button
3. Get a list of similar movies with match scores
4. Click on any recommendation to see details

## How it works

The system uses content-based filtering:

1. **Movie features** - Extracts info like genre, director, cast, keywords
2. **Vectorization** - Converts text features into numerical vectors
3. **Similarity calculation** - Uses cosine similarity to find close matches
4. **Ranking** - Sorts recommendations by similarity score

Basically, if two movies share similar genres, actors, and themes, they'll score high on similarity.

## Dataset

The recommender works with movie datasets from sources like:
- TMDb (The Movie Database)
- IMDb datasets
- MovieLens ratings

You'll need to download the dataset and place it in the `data/` folder. Common files:
- `movies.csv` - Movie titles and metadata
- `ratings.csv` - User ratings (optional, for hybrid models)
- `credits.csv` - Cast and crew info

## Example

```python
# Input: "The Dark Knight"
# Output:
# 1. The Dark Knight Rises (0.89)
# 2. Batman Begins (0.85)
# 3. Inception (0.72)
# 4. Interstellar (0.68)
# 5. The Prestige (0.65)
```

## Improving recommendations

You can make it better by:
- Adding more features (plot summaries, user reviews)
- Using hybrid filtering (content + collaborative)
- Incorporating user ratings and watch history
- Fine-tuning similarity weights
- Adding popularity bias to surface well-known films

## Project structure

```
MovieRecommender/
├── app.py                  # Streamlit web interface
├── recommender.py          # Core recommendation logic
├── data/                   # Movie datasets
├── models/                 # Saved models/vectorizers
└── utils/                  # Helper functions
```

## Common issues

**"Dataset not found"**
Make sure you've downloaded the movie dataset and placed it in the `data/` folder.

**Recommendations seem random**
This usually means the similarity model needs tuning. Try adjusting feature weights or adding more metadata.

**Slow performance**
For large datasets, precompute the similarity matrix and save it. Loading it is much faster than calculating on the fly.

## Tech used

- **Pandas** - Data manipulation
- **scikit-learn** - TF-IDF vectorization and similarity
- **Streamlit** - Web interface
- **NumPy** - Numerical operations

## Future ideas

- Add user accounts and watch history
- Build a rating prediction system
- Include streaming availability info
- Add filters (year, genre, rating)
- Integrate with movie APIs for posters and trailers
- Deploy as a web service

## Credits

Movie data from TMDb and IMDb. Built as a learning project to explore recommendation algorithms.