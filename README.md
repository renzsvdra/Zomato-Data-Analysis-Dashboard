# 🍴 Zomato Data Analysis Dashboard & Recommendation System

An **interactive Streamlit web application** for analyzing Zomato restaurant data and recommending similar restaurants using **TF-IDF** and **Cosine Similarity**.  
The dashboard includes **EDA (Exploratory Data Analysis)** visualizations, **interactive maps**, and **restaurant recommendations** with a modern, theme-adaptive UI.

---

## 🚀 Features

### 🔍 1. Restaurant Recommendation System
- Select any restaurant and get top similar restaurants based on **cuisine, cost, and rating**.  
- Uses **TF-IDF vectorization** and **cosine similarity** to find restaurant similarities.  
- Customizable number of recommendations (1–10).  

### 📊 2. Interactive EDA Dashboards
- View key performance indicators (KPIs) like **total restaurants**, **average rating**, and **average cost**.  
- Explore **top cuisines** with dynamic bar charts.  
- Visualize **rating distributions** (highlighting top 3 restaurants).  
- Analyze **Price vs Rating** scatter plots.  
- Generate **WordClouds** from cuisine data.  

### 🗺️ 3. Map Visualization
- Interactive map of restaurant locations using **Plotly Mapbox**.  
- Filter by **rating range** dynamically.  
- Highlights **Top 3 restaurants** on the map with gold stars.  

### 🏆 4. Top Restaurants Leaderboard
- Displays the **Top 10 restaurants** based on ratings.  
- Includes thumbnails, cuisines, and average costs.  

---

## 💡 Tech Stack

| Component | Technology |
|------------|-------------|
| **Frontend/UI** | Streamlit |
| **Data Handling** | Pandas, NumPy |
| **Visualization** | Plotly Express, Matplotlib, WordCloud |
| **Machine Learning** | Scikit-learn (TF-IDF, Cosine Similarity) |
| **Language** | Python |
| **Dataset** | Zomato Dataset (`zomato.csv`) |

---

## 🧠 How It Works

### 🔹 Recommendation Logic
1. Combine **cuisines**, **average cost**, and **ratings** into a single text field.  
2. Convert text into numerical vectors using **TF-IDF**.  
3. Compute **cosine similarity** between restaurants.  
4. Recommend the most similar restaurants excluding the selected one.  

---

## 🌗 UI Theme
The app supports both **Light Mode** and **Dark Mode** for enhanced viewing.  
You can switch between them using the sidebar option 🌗.

---

## 🧭 Navigation

| Section | Description |
|----------|-------------|
| **Recommendation System** | Find similar restaurants. |
| **EDA Dashboards** | View data insights and plots. |
| **Map Visualization** | Explore restaurant locations. |
| **Top Restaurants** | See the best-rated restaurants. |

---

## 📊 Sample Visuals

📈 **Top 10 Cuisines Bar Chart**  
⭐ **Rating Distribution (highlighted Top 3)**  
☁️ **Cuisine WordCloud**  
🗺️ **Interactive Map with Rating Filter**  
🏆 **Top Restaurants Leaderboard**  

*(Screenshots will be included in the repository with links.)*

---

## 🧩 Key Functions

| Function | Description |
|-----------|-------------|
| `load_data()` | Loads and cleans the dataset. |
| `filter_data()` | Applies user-selected filters (city, delivery, booking). |
| `get_top3()` | Returns top 3 restaurants by rating. |
| `build_tfidf_matrix()` | Builds TF-IDF feature matrix for recommendation system. |

---

## 📚 Insights You Can Derive
- Most popular cuisines in each city.  
- Correlation between **price range** and **ratings**.  
- Restaurant distribution by **rating range**.  
- Identify **high-performing restaurants** for recommendations.  

---

## 🔄 Workflow Overview

**A → B → C → D → E**

**A. Data Loading & Cleaning** →  
**B. Filtering by City/Services** →  
**C. EDA Visualization** →  
**D. Map Visualization** →  
**E. Recommendation System**

---
## 🏁 Future Improvements
- ✅ Add sentiment analysis on customer reviews.  
- ✅ Include filter for cuisine-specific recommendations.  
- ✅ Integrate real-time Zomato API for live data.  

---

## 👨‍💻 Author  

**Lomada Siva Gangi Reddy**  
- 🎓 B.Tech CSE (Data Science), RGMCET (2021–2025)  
- 🎯 Aspiring Data Analyst | Skilled in Python, SQL, Power BI, and Data Science  
- 📍 Open to **Internships & Job Offers**  

📬 **Contact Me**:  
- 📞 9346493592  
- [💼 LinkedIn](https://www.linkedin.com/in/lomada-siva-gangi-reddy-a64197280/) [🌐 GitHub](https://github.com/shivareddy2002)  

---


