__import__('os').environ['STREAMLIT_SERVER_MAX_MESSAGE_SIZE'] = '500'
import streamlit as st
import pickle
import requests
import pandas as pd

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Movie Recommender System",
    page_icon="🎬",
    layout="wide"
)

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>
    /* Hide streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Background */
    .stApp {
        background-color: #0a0a0a;
    }

    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 6px;
    }
    ::-webkit-scrollbar-track {
        background: #0a0a0a;
    }
    ::-webkit-scrollbar-thumb {
        background: #333333;
        border-radius: 10px;
    }

    /* Title */
    .main-title {
        text-align: center;
        font-size: 3rem;
        font-weight: 900;
        color: #ffffff;
        letter-spacing: 0.3em;
        padding: 1.5rem 0 0.3rem 0;
        text-transform: uppercase;
    }

    .sub-title {
        text-align: center;
        font-size: 0.8rem;
        color: #555555;
        margin-bottom: 2rem;
        letter-spacing: 0.2em;
        text-transform: uppercase;
    }

    /* Divider */
    .custom-divider {
        border: none;
        border-top: 1px solid #1f1f1f;
        margin: 1rem 0;
    }

    /* Selectbox label */
    div[data-testid="stSelectbox"] label {
        color: #555555 !important;
        font-size: 0.75rem !important;
        text-transform: uppercase;
        letter-spacing: 0.15em;
    }

    /* Selectbox */
    div[data-testid="stSelectbox"] > div > div {
        background-color: #111111 !important;
        border: 1px solid #2a2a2a !important;
        color: #ffffff !important;
        border-radius: 6px !important;
    }

    /* Slider label */
    div[data-testid="stSlider"] label {
        color: #555555 !important;
        font-size: 0.75rem !important;
        text-transform: uppercase;
        letter-spacing: 0.15em;
    }

    /* Slider track */
    div[data-testid="stSlider"] > div > div > div {
        background-color: #ffffff !important;
    }

    /* Button */
    .stButton > button {
        background-color: #ffffff;
        color: #000000;
        font-size: 0.85rem;
        font-weight: 800;
        border-radius: 6px;
        padding: 0.65rem 2rem;
        border: none;
        width: 100%;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        background-color: #cccccc;
        color: #000000;
        transform: scale(1.02);
    }

    .stButton > button:active {
        background-color: #aaaaaa;
    }

    /* Selected movie card */
    .selected-card {
        background-color: #111111;
        border: 1px solid #2a2a2a;
        border-left: 4px solid #ffffff;
        border-radius: 8px;
        padding: 1.2rem 1.8rem;
        margin: 1.5rem 0 2rem 0;
    }

    .selected-card-title {
        color: #ffffff;
        font-size: 1.6rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: 0.03em;
    }

    .selected-card-meta {
        color: #555555;
        font-size: 0.8rem;
        margin-top: 0.4rem;
        letter-spacing: 0.1em;
        text-transform: uppercase;
    }

    /* Section title */
    .section-title {
        color: #555555;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.2em;
        text-transform: uppercase;
        margin-bottom: 1.2rem;
        padding-bottom: 0.6rem;
        border-bottom: 1px solid #1f1f1f;
    }

    /* Movie card */
    .movie-card {
        background-color: #111111;
        border: 1px solid #1f1f1f;
        border-radius: 8px;
        padding: 0.5rem;
        margin-bottom: 0.5rem;
        transition: all 0.2s ease;
        cursor: pointer;
    }

    .movie-card:hover {
        border-color: #ffffff;
        background-color: #161616;
        transform: translateY(-3px);
    }

    /* Movie rank */
    .movie-rank {
        color: #333333;
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.1em;
        text-align: center;
        margin-top: 0.5rem;
    }

    /* Movie title under poster */
    .movie-title-card {
        color: #cccccc;
        font-size: 0.8rem;
        font-weight: 600;
        text-align: center;
        margin-top: 0.3rem;
        min-height: 2.4rem;
        line-height: 1.3;
        padding: 0 0.2rem;
    }

    /* No poster box */
    .no-poster-box {
        background-color: #111111;
        border: 1px solid #1f1f1f;
        border-radius: 8px;
        height: 260px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        color: #333333;
        font-size: 0.75rem;
        text-align: center;
        letter-spacing: 0.05em;
        gap: 0.5rem;
    }

    .no-poster-icon {
        font-size: 2rem;
        margin-bottom: 0.3rem;
    }

    /* Empty state */
    .empty-state {
        text-align: center;
        padding: 4rem 2rem;
        color: #333333;
        border: 1px dashed #1f1f1f;
        border-radius: 10px;
        margin-top: 1rem;
    }

    .empty-state-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }

    .empty-state-text {
        font-size: 0.9rem;
        letter-spacing: 0.1em;
        text-transform: uppercase;
    }

    /* Spinner */
    .stSpinner > div {
        border-top-color: #ffffff !important;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #2a2a2a;
        font-size: 0.75rem;
        padding: 1.5rem 0;
        letter-spacing: 0.15em;
        text-transform: uppercase;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():
    try:
        movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
        movies_df = pd.DataFrame(movies_dict)
        similarity_matrix = pickle.load(open('similarity.pkl', 'rb'))
        return movies_df, similarity_matrix
    except FileNotFoundError:
        st.error("Pickle files not found. Please run the notebook first.")
        st.stop()
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        st.stop()


movies, similarity = load_data()

# ============================================================
# POSTER FETCHING
# ============================================================

TMDB_API_KEY = "8265bd1679663a7ea12ac168da84d2e8"
PLACEHOLDER = None


def fetch_poster(movie_id, title=""):
    """
    Fetch poster from TMDB.
    Strategy 1: Fetch by movie ID
    Strategy 2: Search by title
    Strategy 3: Return None (show custom placeholder)
    """

    # Strategy 1: Fetch by movie ID
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}"
        params = {"api_key": TMDB_API_KEY, "language": "en-US"}
        response = requests.get(url, params=params, timeout=5)

        if response.status_code == 200:
            data = response.json()
            poster_path = data.get("poster_path")
            if poster_path:
                return f"https://image.tmdb.org/t/p/w500{poster_path}"

    except Exception:
        pass

    # Strategy 2: Search by title
    try:
        if title:
            search_url = "https://api.themoviedb.org/3/search/movie"
            params = {
                "api_key": TMDB_API_KEY,
                "query": title,
                "language": "en-US"
            }
            response = requests.get(search_url, params=params, timeout=5)

            if response.status_code == 200:
                results = response.json().get("results", [])
                for result in results:
                    poster_path = result.get("poster_path")
                    if poster_path:
                        return f"https://image.tmdb.org/t/p/w500{poster_path}"

    except Exception:
        pass

    # Strategy 3: No poster found
    return PLACEHOLDER


# ============================================================
# RECOMMENDATION FUNCTION
# ============================================================

def recommend(movie, n=10):
    """Get n similar movie recommendations with posters"""
    try:
        movie_index = movies[movies['title'] == movie].index[0]

        distances = sorted(
            list(enumerate(similarity[movie_index])),
            reverse=True,
            key=lambda x: x[1]
        )

        recommended_movies = []
        recommended_posters = []

        for i in distances[1:n + 1]:
            row = movies.iloc[i[0]]
            movie_id = row.movie_id
            title = row.title
            recommended_movies.append(title)
            recommended_posters.append(fetch_poster(movie_id, title))

        return recommended_movies, recommended_posters

    except IndexError:
        st.error("Movie not found.")
        return [], []
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return [], []


# ============================================================
# HEADER
# ============================================================

st.markdown('<div class="main-title">CINEMATCH</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">Content-Based Movie Recommender &nbsp;·&nbsp; TMDB Dataset</div>',
    unsafe_allow_html=True
)
st.markdown("<hr class='custom-divider'>", unsafe_allow_html=True)

# ============================================================
# CONTROLS
# ============================================================

col1, col2, col3 = st.columns([4, 1.5, 1.5], gap="medium")

with col1:
    selected_movie = st.selectbox(
        "Select a Movie",
        movies['title'].values,
        index=0
    )

with col2:
    n_recommendations = st.slider(
        "Number of Results",
        min_value=5,
        max_value=15,
        value=10,
        step=5
    )

with col3:
    st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
    recommend_clicked = st.button("RECOMMEND", use_container_width=True)

# ============================================================
# SELECTED MOVIE CARD
# ============================================================

st.markdown(
    f"""
    <div class="selected-card">
        <div class="selected-card-title">{selected_movie}</div>
        <div class="selected-card-meta">Selected Movie &nbsp;·&nbsp; Click Recommend to Find Similar Movies</div>
    </div>
    """,
    unsafe_allow_html=True
)

# ============================================================
# RECOMMENDATIONS
# ============================================================

if recommend_clicked:

    with st.spinner("Finding similar movies..."):
        names, posters = recommend(selected_movie, n=n_recommendations)

    if names:

        st.markdown(
            f'<div class="section-title">Top {len(names)} Recommendations for &nbsp;"{selected_movie}"</div>',
            unsafe_allow_html=True
        )

        # Display in rows of 5
        movies_per_row = 5
        total_rows = (len(names) + movies_per_row - 1) // movies_per_row

        for row in range(total_rows):
            start = row * movies_per_row
            end = min(start + movies_per_row, len(names))

            cols = st.columns(movies_per_row, gap="small")

            for col_idx, movie_idx in enumerate(range(start, end)):
                with cols[col_idx]:

                    poster_url = posters[movie_idx]
                    movie_name = names[movie_idx]
                    rank = movie_idx + 1

                    st.markdown('<div class="movie-card">', unsafe_allow_html=True)

                    # Poster or placeholder
                    if poster_url:
                        st.image(poster_url, use_column_width=True)
                    else:
                        st.markdown(
                            f"""
                            <div class="no-poster-box">
                                <div class="no-poster-icon">◻</div>
                                <div>{movie_name}</div>
                                <div style="color:#222222; font-size:0.7rem;">
                                    No Poster
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                    # Rank and title
                    st.markdown(
                        f"""
                        <div class="movie-rank">#{rank}</div>
                        <div class="movie-title-card">{movie_name}</div>
                        """,
                        unsafe_allow_html=True
                    )

                    st.markdown('</div>', unsafe_allow_html=True)

else:
    # Empty state before clicking recommend
    st.markdown(
        """
        <div class="empty-state">
            <div class="empty-state-icon">◻</div>
            <div class="empty-state-text">
                Select a movie and click Recommend
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ============================================================
# FOOTER
# ============================================================

st.markdown("<hr class='custom-divider'>", unsafe_allow_html=True)
st.markdown(
    """
    <div class="footer">
        Built with Streamlit &nbsp;·&nbsp; TMDB Dataset &nbsp;·&nbsp; Cosine Similarity
    </div>
    """,
    unsafe_allow_html=True
)