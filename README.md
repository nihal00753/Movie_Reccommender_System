<div align="center">

# 🎬 CINEMATCH
### Content-Based Movie Recommender System

[![Live Demo](https://img.shields.io/badge/🚀%20Live%20Demo-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://moviereccommendersystem-0753.streamlit.app/)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/nihal00753/Movie_Reccommender_System)

<br/>

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=flat-square&logo=scikit-learn&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat-square&logo=pandas&logoColor=white)
![TMDB](https://img.shields.io/badge/TMDB%20API-01B4E4?style=flat-square&logo=themoviedatabase&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-F37626?style=flat-square&logo=jupyter&logoColor=white)

</div>

---

## 📌 Overview

**CineMatch** is a content-based movie recommendation engine that suggests similar films based on the movie a user selects. It combines NLP-driven feature engineering with cosine similarity to find the most contextually related movies from the TMDB dataset — all wrapped in a sleek, dark-themed Streamlit web app.

> Try it live → **[moviereccommendersystem-0753.streamlit.app](https://moviereccommendersystem-0753.streamlit.app/)**

---

## ✨ What Was Achieved

### 🔬 Data Processing & Feature Engineering (Jupyter Notebook)
- Loaded and merged the **TMDB 5000 Movies** and **TMDB 5000 Credits** datasets
- Extracted and parsed structured metadata from JSON-like columns: **genres**, **cast**, **crew** (director), and **keywords**
- Applied NLP preprocessing — **lowercasing**, **whitespace removal**, and **stemming** (Porter Stemmer) — to reduce words to their root forms and avoid duplicate features like `"action"` vs `"actions"`
- Combined all features into a single **"tags"** column per movie (overview + genres + keywords + cast + director)
- Vectorized tags using **CountVectorizer** (Bag-of-Words, top 5000 features, English stop-words removed)
- Computed a **cosine similarity matrix** across all ~4800 movies
- Serialized the processed movie data (`movies_dict.pkl`) and the similarity matrix (`similarity.pkl`) for fast runtime loading

### 🌐 Live Web Application (Streamlit)
- Built a fully interactive app branded as **CINEMATCH** with a custom dark-mode UI (deep black `#0a0a0a` background, minimalist typography, hover transitions)
- **Dual-strategy poster fetching via TMDB API:**
  - Strategy 1: Fetch poster directly by TMDB movie ID
  - Strategy 2: Fall back to searching by movie title if the ID lookup fails
  - Strategy 3: Gracefully display a styled placeholder if no poster exists
- Adjustable **recommendation count** (5, 10, or 15 results) via a slider
- Results displayed in **responsive grid rows of 5**, each card showing the movie poster, rank badge, and title
- Deployed on **Streamlit Community Cloud** with a public shareable URL

---

## 🗂️ Project Structure

```
Movie_Reccommender_System/
│
├── notebook.ipynb          # Data processing, feature engineering & model building
├── app.py                  # Streamlit web application (515 lines)
├── movies_dict.pkl         # Serialized processed movie DataFrame
├── similarity.pkl          # Precomputed cosine similarity matrix
├── requirements.txt        # Python dependencies
└── README.md
```

---

## ⚙️ How It Works

```
User selects a movie
        ↓
Look up movie index in movies_dict.pkl
        ↓
Retrieve cosine similarity scores from similarity.pkl
        ↓
Sort all movies by similarity score (descending)
        ↓
Return top-N movies (excluding the selected film)
        ↓
Fetch posters from TMDB API → Display in grid UI
```

The core of the recommendation is **cosine similarity** between movie tag vectors. Two movies are considered similar if their combined tag vectors point in the same direction in high-dimensional feature space — meaning they share overlapping genres, cast, directors, themes, and keywords.

---

## 🧰 Tech Stack

| Layer | Tools |
|---|---|
| **Language** | Python 3.x |
| **Web App** | Streamlit 1.39.0 |
| **ML / NLP** | scikit-learn (CountVectorizer, cosine_similarity) |
| **Data Processing** | Pandas 2.1.4, NLTK (PorterStemmer) |
| **External API** | TMDB (The Movie Database) API v3 |
| **Serialization** | Python Pickle |
| **Notebook** | Jupyter Notebook |
| **Deployment** | Streamlit Community Cloud |

---

## 🚀 Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/nihal00753/Movie_Reccommender_System.git
cd Movie_Reccommender_System

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch the app
streamlit run app.py
```

> **Note:** The `movies_dict.pkl` and `similarity.pkl` files must be present (generated by `notebook.ipynb`). If missing, run the notebook first.

---

## 🔗 Links

| | |
|---|---|
| 🌐 **Live App** | [moviereccommendersystem-0753.streamlit.app](https://moviereccommendersystem-0753.streamlit.app/) |
| 💻 **GitHub Repo** | [github.com/nihal00753/Movie_Reccommender_System](https://github.com/nihal00753/Movie_Reccommender_System) |
| 🎬 **Dataset** | [TMDB 5000 Movie Dataset — Kaggle](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata) |

---

<div align="center">
  <sub>Built with ❤️ using Streamlit · TMDB Dataset · Cosine Similarity</sub>
</div>
