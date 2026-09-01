import streamlit as st
import pandas as pd
import numpy as np
import os
import base64
import requests
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
import lightgbm as lgbm

# ---------------------------
# Configuration & Setup
# ---------------------------
st.set_page_config(
    page_title="🌍 Destination Recommender",
    layout="wide",
    page_icon="🌍",
    initial_sidebar_state="expanded"
)

# ---------------------------
# Local Background Image Setup
# ---------------------------
def get_base64_image(image_file):
    current_dir = os.path.dirname(__file__)
    image_path = os.path.join(current_dir, image_file)
    try:
        with open(image_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except Exception:
        return ""

base64_nepal = get_base64_image("nepal.png")

# ---------------------------
# Professional Modern Styling (UI/UX Revamp)
# ---------------------------
bg_style = f"""
    background-image: linear-gradient(rgba(15, 23, 42, 0.65), rgba(15, 23, 42, 0.75)), url("data:image/png;base64,{base64_nepal}");
    background-size: cover;
    background-attachment: fixed;
    background-position: center;
""" if base64_nepal else "background-color: #0f172a;"

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');

    .stApp {{
        {bg_style}
        font-family: 'Plus Jakarta Sans', sans-serif;
    }}

    /* Main Title & Subtitle */
    .main-title-container {{
        text-align: center;
        padding: 2rem 1rem 0.5rem 1rem;
    }}
    .title {{
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: #FFFFFF;
        font-size: 46px;
        font-weight: 700;
        letter-spacing: -0.5px;
        margin-bottom: 5px;
        text-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }}
    .subtitle {{
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: #F59E0B;
        font-size: 20px;
        font-weight: 500;
        margin-bottom: 2rem;
        text-shadow: 0 2px 8px rgba(0,0,0,0.3);
    }}

    /* Glassmorphism Recommendation Cards */
    .recommendation-card {{
        background: rgba(255, 255, 255, 0.88);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.4);
        color: #1E293B;
        padding: 1.5rem;
        border-radius: 18px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
        margin: 0.75rem 0;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }}
    .recommendation-card:hover {{
        transform: translateY(-6px);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.25);
        background: rgba(255, 255, 255, 0.95);
    }}
    .card-title {{
        font-size: 22px;
        font-weight: 700;
        color: #0F172A;
        margin-bottom: 8px;
    }}
    .card-badge {{
        display: inline-block;
        background: #F1F5F9;
        color: #475569;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        margin-bottom: 12px;
    }}
    .card-metric {{
        font-size: 14px;
        color: #334155;
        margin: 6px 0;
    }}

    /* Sidebar Clean Styling */
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, #0F172A 0%, #1E293B 100%);
        color: #F8FAFC;
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }}
    [data-testid="stSidebar"] .stMarkdown h2, 
    [data-testid="stSidebar"] .stMarkdown h3, 
    [data-testid="stSidebar"] label {{
        color: #F8FAFC !important;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }}

    /* Custom Buttons */
    .stButton > button {{
        background: linear-gradient(135deg, #F59E0B 0%, #D97706 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.6rem 1.2rem;
        font-weight: 600;
        font-family: 'Plus Jakarta Sans', sans-serif;
        box-shadow: 0 4px 14px rgba(245, 158, 11, 0.4);
        transition: all 0.2s ease;
        width: 100%;
    }}
    .stButton > button:hover {{
        background: linear-gradient(135deg, #D97706 0%, #B45309 100%);
        box-shadow: 0 6px 20px rgba(245, 158, 11, 0.6);
        color: white;
    }}
    </style>
""", unsafe_allow_html=True)

# ---------------------------
# Data Loading and ML Model
# ---------------------------
@st.cache_data
def load_data():
    current_dir = os.path.dirname(__file__)
    csv_path = os.path.join(current_dir, "destinations_with_coordinates.csv")
    
    data = pd.read_csv(csv_path)
    
    # Clean and normalize data
    data.columns = data.columns.str.strip().str.lower()
    data["pname"] = data["pname"].str.strip().str.lower()
    data["latitude"] = pd.to_numeric(data["latitude"], errors="coerce")
    data["longitude"] = pd.to_numeric(data["longitude"], errors="coerce")
    
    # Process tags safely
    if 'tags' in data.columns:
        data['tags'] = data['tags'].apply(
            lambda x: ','.join([tag.strip().lower() for tag in str(x).split(',')]) 
            if pd.notna(x) else np.nan
        )
    else:
        data['tags'] = np.nan
    
    # Feature engineering
    feature_cols = ['culture', 'adventure', 'wildlife', 'sightseeing', 'history']
    scaler = MinMaxScaler()
    data[feature_cols] = scaler.fit_transform(data[feature_cols])
    
    # Train ML model
    data['popularity'] = data[feature_cols].mean(axis=1) + 0.1 * data['culture']
    X_train, X_test, y_train, y_test = train_test_split(
        data[feature_cols], data['popularity'], test_size=0.2, random_state=42
    )
    
    lgbm_model = lgbm.LGBMRegressor(num_leaves=31, learning_rate=0.05, n_estimators=100)
    lgbm_model.fit(X_train, y_train)
    data['ml_score'] = lgbm_model.predict(data[feature_cols])
    
    # Normalize ML scores
    data['ml_score'] = MinMaxScaler().fit_transform(data[['ml_score']])
    
    return data, scaler, feature_cols, lgbm_model

data, scaler, feature_cols, lgbm_model = load_data()

# ---------------------------
# Weather API (Safe Streamlit Secrets)
# ---------------------------
def get_weather(lat, lon):
    try:
        if pd.isna(lat) or pd.isna(lon):
            return "No weather data"
        
        api_key = st.secrets["WEATHER_API_KEY"]
        
        url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
        response = requests.get(url)
        response.raise_for_status()
        weather_data = response.json()
        description = weather_data['weather'][0]['description'].capitalize()
        temp = round(weather_data['main']['temp'])
        return f"{description}, {temp}°C"
    except Exception:
        return "Weather unavailable"

# ---------------------------
# Recommendation Engine
# ---------------------------
def recommend_destinations(user_preferences, input_destination, selected_tags, data, top_n=6):
    similarity_scores = np.zeros(len(data))
    input_destination = input_destination.strip().lower() if input_destination else ""
    
    # Destination-based similarity
    if input_destination:
        if input_destination in data['pname'].values:
            destination_idx = data[data['pname'] == input_destination].index[0]
            destination_features = data.loc[destination_idx, feature_cols].values.reshape(1, -1)
            similarity_scores += cosine_similarity(data[feature_cols].values, destination_features).flatten()
        else:
            st.warning(f"Destination '{input_destination}' not found")
    
    # User preferences similarity
    if user_preferences:
        user_df = pd.DataFrame([user_preferences])
        user_scaled = scaler.transform(user_df)
        similarity_scores += cosine_similarity(data[feature_cols].values, user_scaled).flatten()
    
    # Tag-based matching
    if selected_tags:
        normalized_tags = [tag.strip().lower() for tag in selected_tags]
        max_tag_score = len(normalized_tags)
        for idx, row in data.iterrows():
            if pd.notna(row['tags']):
                row_tags = [t.strip().lower() for t in row['tags'].split(',')]
                tag_score = sum(1 for tag in normalized_tags if tag in row_tags)
                similarity_scores[idx] += (tag_score / max_tag_score) if max_tag_score > 0 else 0
    
    # Blend with ML predictions
    similarity_scores = 0.7 * similarity_scores + 0.3 * data['ml_score']
    
    # Normalize final scores
    min_score = np.min(similarity_scores)
    max_score = np.max(similarity_scores)
    if max_score - min_score > 0:
        similarity_scores = (similarity_scores - min_score) / (max_score - min_score + 1e-8)
    
    data_copy = data.copy()
    data_copy['similarity'] = similarity_scores
    
    if input_destination:
        data_copy = data_copy[data_copy['pname'] != input_destination]
    
    sorted_data = data_copy.sort_values(by='similarity', ascending=False)
    
    recommendations = []
    for _, row in sorted_data.head(top_n).iterrows():
        lat, lon = row['latitude'], row['longitude']
        weather_info = get_weather(lat, lon)
        province_val = row.get('province', "")
        if province_val and not str(province_val).lower().startswith("province"):
            province_val = f"Province {province_val}"
        recommendations.append({
            "Destination": row['pname'].title(),
            "Similarity": round(row['similarity'] * 100, 1), # Express as percentage for better UX
            "Tags": row['tags'].title() if pd.notna(row['tags']) else "General",
            "Weather": weather_info,
            "Province": province_val
        })
    return pd.DataFrame(recommendations)

# ---------------------------
# UI Components & Flow
# ---------------------------
def generate_recommendations():
    dest = st.session_state.get("input_destination", "").strip().lower()
    prefs = st.session_state.get("user_preferences", None)
    tags = [tag.strip().lower() for tag in st.session_state.get("selected_tags", [])]
    recs = recommend_destinations(prefs, dest, tags, data)
    st.session_state.recommendations = recs

# Sidebar Design
st.sidebar.markdown("### 🎛️ Customize Trip")
st.sidebar.text_input("🔍 Search destination:", key="input_destination", on_change=generate_recommendations)

st.sidebar.markdown("---")
add_preferences = st.sidebar.checkbox("⭐ Set category preferences?")
if add_preferences:
    st.sidebar.markdown("##### Adjust Interest Sliders")
    st.session_state.user_preferences = {
        "culture": st.sidebar.slider("Culture", 0, 5, 3),
        "adventure": st.sidebar.slider("Adventure", 0, 5, 3),
        "wildlife": st.sidebar.slider("Wildlife", 0, 5, 3),
        "sightseeing": st.sidebar.slider("Sightseeing", 0, 5, 3),
        "history": st.sidebar.slider("History", 0, 5, 3)
    }
else:
    st.session_state.user_preferences = None

st.sidebar.markdown("---")
add_tags = st.sidebar.checkbox("🏷️ Filter by tags?")
if add_tags:
    all_tags = sorted(list(set(
        tag.strip().lower()
        for tags in data['tags'].dropna()
        for tag in tags.split(',')
    )))
    st.session_state.selected_tags = st.sidebar.multiselect(
        "Select tags:", 
        [tag.title() for tag in all_tags]
    )
else:
    st.session_state.selected_tags = []

st.sidebar.markdown("<br>", unsafe_allow_html=True)
st.sidebar.button("✨ Get Recommendations", on_click=generate_recommendations)

# Main UI Header
st.markdown("""
    <div class="main-title-container">
        <div class="title">🌍 Destination Recommender</div>
        <div class="subtitle">Discover your next unforgettable journey</div>
    </div>
""", unsafe_allow_html=True)

# Main Content Grid Display
if "recommendations" in st.session_state and st.session_state.recommendations is not None:
    recs = st.session_state.recommendations
    if not recs.empty:
        st.markdown("### ✨ Top Recommendations For You")
        cols = st.columns(3)
        for i, (_, row) in enumerate(recs.iterrows()):
            with cols[i % 3]:
                province_display = f"📍 {row['Province']}" if row.get("Province") else "📍 Explore Region"
                st.markdown(f"""
                    <div class="recommendation-card">
                        <div class="card-title">{row['Destination']}</div>
                        <div class="card-badge">{province_display}</div>
                        <div class="card-metric">🔥 <b>Match Score:</b> {row['Similarity']}%</div>
                        <div class="card-metric">🏷️ <b>Tags:</b> {row['Tags']}</div>
                        <div class="card-metric">🌤️ <b>Weather:</b> {row['Weather']}</div>
                    </div>
                """, unsafe_allow_html=True)
    else:
        st.warning("No recommendations found matching your specific inputs. Try modifying your filters.")
else:
    st.info("👋 Welcome! Search a destination or set your preferences in the sidebar to reveal custom recommendations.")

st.sidebar.markdown("---")
st.sidebar.markdown("<div style='text-align: center; color: #94A3B8; font-size: 12px;'>Powered by Machine Learning & Streamlit</div>", unsafe_allow_html=True)
