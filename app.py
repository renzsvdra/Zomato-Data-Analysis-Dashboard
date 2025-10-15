# app.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# ==========================
# Page Config
# ==========================
st.set_page_config(page_title="🍴 Zomato Dashboard & Recommender", layout="wide")

# ==========================
# Sidebar Theme Mode
# ==========================
st.sidebar.title("🍽️ Zomato Data Analysis Dashboard")
st.sidebar.title("👨‍💻 Siva")
theme_choice = st.sidebar.radio("🌗 Theme Mode", ["Light Mode", "Dark Mode"])

# Adaptive color palette
if theme_choice == "Light Mode":
    plotly_template = "plotly_white"
    wc_background = "#C2CFDA"
    wc_color = "black"
    card_bg_color = "#C3CCD4"
    card_text_color = "#323941"
else:
    plotly_template = "plotly_dark"
    wc_background = "#24282F"
    wc_color = "white"
    card_bg_color = "#383333"
    card_text_color = "#DFD7D7"

# ==========================
# Custom CSS & Navbar
# ==========================
logo_url = "https://img.icons8.com/color/48/000000/restaurant.png"
st.markdown(f"""
    <style>
    .stApp {{
        background-color:{wc_background};
        color:{card_text_color};
    }}
    .stButton>button {{
        background-color: #FF6F61;
        color: white;
        font-weight:bold;
        border:none;
        border-radius:8px;
        padding:8px 16px;
    }}
    .navbar {{
        position: fixed;
        top: 150%;
        width: 100%;
        z-index: 100;
        background-color: {card_bg_color};
        padding: 10px 20px;
        color: {card_text_color};
        font-size: 18px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }}

    .nav-links {{display:flex; gap:20px;}}
    .nav-link {{color: {card_text_color}; text-decoration:none; font-weight:bold;}}
    .nav-link:hover {{color:#FF6F61;}}
    .stApp {{padding-top:80px;}}
    .logo {{height:40px; margin-right:10px;}}
    .kpi-card {{
        padding:20px; border-radius:10px;
        background-color:{card_bg_color};
        color:{card_text_color}; text-align:center;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    }}
    .recommend-card {{
        padding:15px; border-radius:10px;
        background-color:{card_bg_color};
        color:{card_text_color}; margin-bottom:10px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    }}
    .leader-card {{
        padding:15px; border-radius:10px;
        background-color:{card_bg_color};
        color:{card_text_color}; margin-bottom:10px;
        display:flex; align-items:center;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    }}
    .restaurant-img {{
        height:60px; width:60px; border-radius:10px; margin-right:15px;
    }}
    </style>
    <div class="navbar">
        <div style="display:flex; align-items:center;">
            <img src="{logo_url}" class="logo">
            <span style="font-weight:bold; font-size:20px;">Zomato Dashboard</span>
        </div>
        <div class="nav-links">
            <a class="nav-link" href="#recommendation-system">Recommendation</a>
            <a class="nav-link" href="#eda-dashboards">EDA</a>
            <a class="nav-link" href="#map-visualization">Map</a>
            <a class="nav-link" href="#top-restaurants">Top Restaurants</a>
        </div>
    </div>
""", unsafe_allow_html=True)

# ==========================
# Load & Clean Data
# ==========================
@st.cache_data
def load_data(path="zomato.csv"):
    df = pd.read_csv(path, encoding="latin1")
    # normalize column names
    df.columns = df.columns.str.strip().str.lower().str.replace(r"[^a-z0-9]", "_", regex=True)

    # average_cost_for_two may or may not exist
    if "average_cost_for_two" in df.columns:
        df["average_cost_for_two"] = pd.to_numeric(df["average_cost_for_two"], errors="coerce")
    else:
        df["average_cost_for_two"] = np.nan

    # fill and safe defaults
    if "cuisines" in df.columns:
        df["cuisines"] = df["cuisines"].fillna("Unknown")
    else:
        df["cuisines"] = "Unknown"

    if "aggregate_rating" in df.columns:
        df["aggregate_rating"] = pd.to_numeric(df["aggregate_rating"], errors="coerce")
        df["aggregate_rating"].fillna(df["aggregate_rating"].median(skipna=True), inplace=True)
    else:
        df["aggregate_rating"] = 0.0

    if "has_online_delivery" in df.columns:
        df["has_online_delivery"] = df["has_online_delivery"].fillna("No")
    else:
        df["has_online_delivery"] = "No"

    if "has_table_booking" in df.columns:
        df["has_table_booking"] = df["has_table_booking"].fillna("No")
    else:
        df["has_table_booking"] = "No"

    if "price_range" in df.columns:
        df["price_range"] = pd.to_numeric(df["price_range"], errors="coerce")
        df["price_range"].fillna(df["price_range"].median(skipna=True), inplace=True)
    else:
        df["price_range"] = np.nan

    # remove obvious bad city values
    if "city" in df.columns:
        df = df[df["city"].notna() & (df["city"].str.upper() != "NEW")]
    else:
        df["city"] = "Unknown"

    # ensure lat/lon present
    if "latitude" in df.columns and "longitude" in df.columns:
        df.dropna(subset=["latitude", "longitude"], inplace=True)
    else:
        df["latitude"] = np.nan
        df["longitude"] = np.nan

    # restaurant thumbnail
    default_thumb = "https://img.icons8.com/ios-filled/100/000000/restaurant.png"
    if "restaurant_thumb" in df.columns:
        df["restaurant_thumb"] = df["restaurant_thumb"].fillna(default_thumb)
    else:
        df["restaurant_thumb"] = default_thumb

    df.drop_duplicates(inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df

df = load_data()

# ==========================
# Helper: Top 3 by rating (uses current df)
# ==========================
def get_top3(df_local):
    if df_local.empty:
        return pd.DataFrame()
    return df_local.sort_values(by="aggregate_rating", ascending=False).head(3)

# ==========================
# Sidebar Filters
# ==========================
st.sidebar.title("🍴 Filters")
city_filter = st.sidebar.multiselect("City", sorted(df["city"].dropna().unique()))
st.sidebar.markdown("**Service Availability**")
online_delivery_chk = st.sidebar.checkbox("Online Delivery ✅", value=False)
table_booking_chk = st.sidebar.checkbox("Table Booking 🪑", value=False)

@st.cache_data
def filter_data(df, city_filter, online_delivery_chk, table_booking_chk):
    filtered = df.copy()
    if city_filter:
        filtered = filtered[filtered["city"].isin(city_filter)]
    service_conditions = []
    if online_delivery_chk:
        service_conditions.append(filtered["has_online_delivery"].astype(str).str.upper() == "YES")
    if table_booking_chk:
        service_conditions.append(filtered["has_table_booking"].astype(str).str.upper() == "YES")
    if service_conditions:
        filtered = filtered[np.logical_or.reduce(service_conditions)]
    filtered = filtered.reset_index(drop=True)
    return filtered

filtered_df = filter_data(df, city_filter, online_delivery_chk, table_booking_chk)

# top3 computed on the filtered set (used in charts & map highlight)
top3 = get_top3(filtered_df)

# ==========================
# Cache TF-IDF Matrix
# ==========================
@st.cache_resource
def build_tfidf_matrix(df_for_tfidf):
    # Build a single text representation per row
    combined = (
        df_for_tfidf["cuisines"].astype(str).fillna("") + " " +
        df_for_tfidf["average_cost_for_two"].fillna("").astype(str) + " " +
        df_for_tfidf["aggregate_rating"].fillna("").astype(str)
    )
    tfidf = TfidfVectorizer(stop_words="english")
    matrix = tfidf.fit_transform(combined)
    return matrix, tfidf

# ==========================
# Page Navigation
# ==========================
page = st.sidebar.radio("Navigate:", ["Recommendation System", "EDA Dashboards", "Map Visualization", "Top Restaurants"])

# ==========================
# Recommendation System
# ==========================
if page == "Recommendation System":
    st.markdown("<h2 id='recommendation-system'>🍽️ Restaurant Recommendation System</h2>", unsafe_allow_html=True)

    if filtered_df.empty:
        st.warning("⚠️ No restaurants available for the selected filters.")
    else:
        # Use a reset-index version to ensure positional indices align with TF-IDF matrix
        filtered_df_reset = filtered_df.reset_index(drop=True)

        restaurant_list = sorted(filtered_df_reset["restaurant_name"].dropna().unique())
        selected_restaurant = st.selectbox("Select a restaurant:", restaurant_list)
        top_n = st.slider("Number of recommendations", 1, 10, 5)

        if st.button("🔍 Show Recommendations"):
            # Build matrix aligned to filtered_df_reset
            matrix, tfidf = build_tfidf_matrix(filtered_df_reset)

            if selected_restaurant not in filtered_df_reset["restaurant_name"].values:
                st.warning("❗ Selected restaurant not found in the current filtered dataset.")
            else:
                # pick the first matching restaurant (if duplicates exist)
                pos_indices = filtered_df_reset.index[filtered_df_reset["restaurant_name"] == selected_restaurant].tolist()
                if not pos_indices:
                    st.warning("❗ Couldn't locate the selected restaurant after resetting index.")
                else:
                    idx = pos_indices[0]  # positional index aligned to TF-IDF
                    if matrix.shape[0] <= 1:
                        st.info("Not enough restaurants to build recommendations (need at least 2).")
                    else:
                        cosine_sim = cosine_similarity(matrix, matrix)
                        sim_scores = list(enumerate(cosine_sim[idx]))
                        # sort by similarity (exclude self)
                        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
                        # remove self match
                        sim_scores = [s for s in sim_scores if s[0] != idx]
                        # limit to available items
                        max_available = len(sim_scores)
                        n_pick = min(top_n, max_available)
                        sim_indices = [i[0] for i in sim_scores[:n_pick]]

                        if not sim_indices:
                            st.info("No similar restaurants found for this selection.")
                        else:
                            results = filtered_df_reset.iloc[sim_indices][
                                ["restaurant_name", "cuisines", "average_cost_for_two", "aggregate_rating", "restaurant_thumb"]
                            ].reset_index(drop=True)

                            st.markdown("### 🎯 Recommended Restaurants")
                            for _, row in results.iterrows():
                                with st.expander(f"🍴 {row['restaurant_name']} — ⭐ {row['aggregate_rating']}"):
                                    if pd.notna(row["restaurant_thumb"]) and str(row["restaurant_thumb"]).strip():
                                        st.image(row["restaurant_thumb"], width=100)
                                    else:
                                        st.image("https://via.placeholder.com/100x100.png?text=No+Image", width=100)
                                    st.markdown(f"**🍛 Cuisines:** {row['cuisines']}")
                                    st.markdown(f"**💰 Average Cost for Two:** ₹{row['average_cost_for_two']}")
                                    st.markdown("---")

# ==========================
# EDA Dashboards
# ==========================
elif page == "EDA Dashboards":
    st.markdown("<h2 id='eda-dashboards'>📊 Interactive EDA Dashboard</h2>", unsafe_allow_html=True)
    if filtered_df.empty:
        st.warning("No restaurants match the selected filters.")
    else:
        total_restaurants = len(filtered_df)
        avg_rating = round(filtered_df['aggregate_rating'].mean(), 2)
        avg_cost = round(filtered_df['average_cost_for_two'].mean(), 2) if filtered_df['average_cost_for_two'].notna().any() else 0

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"<div class='kpi-card'><h4>Total Restaurants</h4><h2>{total_restaurants}</h2></div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<div class='kpi-card'><h4>Average Rating</h4><h2>{avg_rating}</h2></div>", unsafe_allow_html=True)
        with col3:
            st.markdown(f"<div class='kpi-card'><h4>Avg Cost for Two</h4><h2>₹{avg_cost}</h2></div>", unsafe_allow_html=True)

        # Top cuisines
        st.markdown("### 🍲 Top 10 Cuisines")
        cuisine_counts = filtered_df["cuisines"].str.split(",").explode().str.strip().value_counts().head(10)
        fig_cuisine = px.bar(x=cuisine_counts.index, y=cuisine_counts.values, labels={"x": "Cuisine", "y": "Count"}, template=plotly_template)
        st.plotly_chart(fig_cuisine, use_container_width=True)

        # Ratings Distribution
        rating_counts = filtered_df.groupby("aggregate_rating")["restaurant_name"].apply(lambda x: ", ".join(x)).reset_index()
        rating_counts['num'] = rating_counts['restaurant_name'].str.split(",").apply(len)
        # highlight if rating in top3 list
        top3_ratings = top3['aggregate_rating'].unique() if (top3 is not None and not top3.empty) else []
        rating_counts['color'] = rating_counts['aggregate_rating'].apply(lambda x: "Top Three Ratings" if x in top3_ratings else "Other Ratings")
        st.markdown("### ⭐ Ratings Distribution (Top 3 Highlighted)")
        fig_rating = px.bar(
            rating_counts,
            x='aggregate_rating',
            y='num',
            hover_data={'restaurant_name':True},
            color='color',
            labels={'aggregate_rating':'Rating','num':'Number of Restaurants'},
            template=plotly_template,
            text='num'
        )
        st.plotly_chart(fig_rating, use_container_width=True)

        # Price vs Rating Scatter
        st.markdown("### 💰 Price vs Rating")
        fig_scatter = px.scatter(filtered_df, x="price_range", y="aggregate_rating", color="city", template=plotly_template)
        st.plotly_chart(fig_scatter, use_container_width=True)

        # WordCloud
        st.markdown("### ☁️ Cuisine WordCloud")
        text = " ".join(filtered_df['cuisines'].dropna().astype(str))
        # WordCloud background uses wc_background and colormap default; colormap cannot be explicitly set to wc_color string
        wc = WordCloud(background_color=wc_background, width=800, height=400).generate(text)
        fig_wc, ax_wc = plt.subplots(figsize=(10, 5))
        ax_wc.imshow(wc, interpolation='bilinear')
        ax_wc.axis('off')
        st.pyplot(fig_wc)

# --------------------------
# Map Visualization
# --------------------------
elif page == "Map Visualization":
    st.markdown("<h2 id='map-visualization'>🗺️ Restaurant Locations Map</h2>", unsafe_allow_html=True)

    if filtered_df.empty:
        st.warning("No restaurants available to display on the map.")
    else:
        if theme_choice == "Light Mode":
            mapbox_style = "open-street-map"
            color_scale = "Viridis"
        else:
            mapbox_style = "open-street-map"
            color_scale = "Cividis"

        # Rating range slider
        min_rating = float(filtered_df["aggregate_rating"].min())
        max_rating = float(filtered_df["aggregate_rating"].max())
        min_sel, max_sel = st.slider(
            "Select Rating Range",
            min_rating,
            max_rating,
            (min_rating, max_rating)
        )

        rating_filtered_df = filtered_df[
            (filtered_df["aggregate_rating"] >= min_sel) &
            (filtered_df["aggregate_rating"] <= max_sel)
        ]

        if rating_filtered_df.empty:
            st.warning("No restaurants found in this rating range.")
        else:
            fig_map = px.scatter_mapbox(
                rating_filtered_df,
                lat="latitude",
                lon="longitude",
                hover_name="restaurant_name",
                hover_data={
                    "cuisines": True,
                    "average_cost_for_two": True,
                    "aggregate_rating": True
                },
                color="aggregate_rating",
                color_continuous_scale=color_scale,
                size_max=15,
                zoom=10,
                height=600,
            )

            # Highlight Top 3 Restaurants (based on filtered set)
            if (top3 is not None) and (not top3.empty):
                # ensure top3 has lat/lon
                if top3['latitude'].notna().any() and top3['longitude'].notna().any():
                    fig_map.add_scattermapbox(
                        lat=top3['latitude'],
                        lon=top3['longitude'],
                        mode='markers',
                        marker=dict(size=20, color='gold', symbol='star'),
                        hovertext=top3['restaurant_name'],
                        name='Top 3 Restaurants'
                    )

            fig_map.update_layout(
                mapbox_style=mapbox_style,
                margin={"r": 0, "t": 0, "l": 0, "b": 0},
                coloraxis_colorbar=dict(title="Aggregate Rating", ticks="outside")
            )
            st.plotly_chart(fig_map, use_container_width=True)

# ==========================
# Top Restaurants
# ==========================
elif page == "Top Restaurants":
    st.markdown("<h2 id='top-restaurants'>🏆 Top 10 Restaurants by Rating</h2>", unsafe_allow_html=True)
    if filtered_df.empty:
        st.warning("No restaurants available to display leaderboard.")
    else:
        top_restaurants = filtered_df.sort_values(by="aggregate_rating", ascending=False).head(10)
        for _, row in top_restaurants.iterrows():
            # ensure rating is numeric and within reasonable bounds
            try:
                stars = "⭐" * int(round(float(row["aggregate_rating"])))
            except Exception:
                stars = ""
            thumb = row.get('restaurant_thumb', "https://img.icons8.com/ios-filled/100/000000/restaurant.png")
            avg_cost = row.get('average_cost_for_two', "")
            st.markdown(f"""
                <div class="leader-card">
                    <img src="{thumb}" class="restaurant-img">
                    <div>
                        <strong>{row['restaurant_name']}</strong> {stars}<br>
                        Cuisines: {row['cuisines']}<br>
                        Avg Cost for Two: ₹{avg_cost}
                    </div>
                </div>
            """, unsafe_allow_html=True)
