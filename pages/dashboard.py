import streamlit as st
import random
import datetime
import time
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import date, timedelta
import calendar

# Function to simulate API call for historical facts
def fetch_indian_historical_facts(date=None, keyword=None, category=None, century=None, limit=50):
    """
    Simulates an API call to fetch Indian historical facts
    In a real application, replace with actual API endpoint
    """
    # Sample database of Indian historical facts with categories and images
    indian_facts = [
        {"date": "August 15, 1947", "fact": "India gained independence from British rule after nearly 200 years of colonization.", "category": "Politics", "image": "independence.jpg", "century": "20th"},
        {"date": "January 26, 1950", "fact": "The Constitution of India came into effect, and India became a republic.", "category": "Politics", "image": "constitution.jpg", "century": "20th"},
        {"date": "October 2, 1869", "fact": "Mahatma Gandhi, leader of India's independence movement, was born in Porbandar, Gujarat.", "category": "People", "image": "gandhi.jpg", "century": "19th"},
        {"date": "November 14, 1889", "fact": "Jawaharlal Nehru, the first Prime Minister of independent India, was born.", "category": "People", "image": "nehru.jpg", "century": "19th"},
        {"date": "December 16, 1971", "fact": "The Indo-Pakistani War ended with the surrender of Pakistan and the creation of Bangladesh.", "category": "War", "image": "indo-pak-war.jpg", "century": "20th"},
        {"date": "May 18, 1974", "fact": "India conducted its first nuclear test, codenamed 'Smiling Buddha', in Rajasthan.", "category": "Science", "image": "nuclear-test.jpg", "century": "20th"},
        {"date": "June 25, 1975", "fact": "Prime Minister Indira Gandhi declared a state of emergency across India.", "category": "Politics", "image": "emergency.jpg", "century": "20th"},
        {"date": "October 31, 1984", "fact": "Prime Minister Indira Gandhi was assassinated by her bodyguards.", "category": "Politics", "image": "indira-gandhi.jpg", "century": "20th"},
        {"date": "December 3, 1984", "fact": "The Bhopal Gas Tragedy occurred, one of the world's worst industrial disasters.", "category": "Disaster", "image": "bhopal.jpg", "century": "20th"},
        {"date": "May 21, 1991", "fact": "Former Prime Minister Rajiv Gandhi was assassinated during an election campaign.", "category": "Politics", "image": "rajiv-gandhi.jpg", "century": "20th"},
        {"date": "May 11, 1998", "fact": "India conducted a series of nuclear tests known as Pokhran-II.", "category": "Science", "image": "pokhran.jpg", "century": "20th"},
        {"date": "July 26, 1999", "fact": "The Kargil War between India and Pakistan ended with India recapturing key territories.", "category": "War", "image": "kargil.jpg", "century": "20th"},
        {"date": "December 13, 2001", "fact": "The Indian Parliament was attacked by terrorists, leading to increased tensions with Pakistan.", "category": "Terrorism", "image": "parliament-attack.jpg", "century": "21st"},
        {"date": "November 26, 2008", "fact": "Mumbai terror attacks began, lasting for four days and killing 166 people.", "category": "Terrorism", "image": "mumbai-attacks.jpg", "century": "21st"},
        {"date": "August 5, 2019", "fact": "The Indian government revoked the special status of Jammu and Kashmir.", "category": "Politics", "image": "kashmir.jpg", "century": "21st"},
        {"date": "January 16, 2021", "fact": "India began the world's largest COVID-19 vaccination drive.", "category": "Health", "image": "covid-vaccine.jpg", "century": "21st"},
        {"date": "April 3, 1919", "fact": "Jallianwala Bagh massacre took place in Amritsar, Punjab.", "category": "Colonial", "image": "jallianwala.jpg", "century": "20th"},
        {"date": "March 12, 1930", "fact": "Mahatma Gandhi began the Salt March, a nonviolent protest against the British salt monopoly.", "category": "Colonial", "image": "salt-march.jpg", "century": "20th"},
        {"date": "August 8, 1942", "fact": "The Quit India Movement was launched by Mahatma Gandhi.", "category": "Colonial", "image": "quit-india.jpg", "century": "20th"},
        {"date": "July 18, 1947", "fact": "The Indian Independence Act was passed by the British Parliament.", "category": "Politics", "image": "independence-act.jpg", "century": "20th"},
        {"date": "September 17, 1948", "fact": "Operation Polo led to the integration of Hyderabad State into India.", "category": "Politics", "image": "hyderabad.jpg", "century": "20th"},
        {"date": "October 20, 1962", "fact": "The Sino-Indian War began with Chinese forces attacking Indian positions.", "category": "War", "image": "sino-indian.jpg", "century": "20th"},
        {"date": "April 24, 1993", "fact": "The Bombay Stock Exchange bombing killed 257 people and injured hundreds more.", "category": "Terrorism", "image": "bse-bombing.jpg", "century": "20th"},
        {"date": "February 27, 2002", "fact": "The Godhra train burning incident triggered communal riots in Gujarat.", "category": "Disaster", "image": "godhra.jpg", "century": "21st"},
        {"date": "July 18, 2007", "fact": "Pratibha Patil became the first woman President of India.", "category": "Politics", "image": "patil.jpg", "century": "21st"},
        {"date": "November 8, 2016", "fact": "The Indian government announced the demonetization of ₹500 and ₹1000 banknotes.", "category": "Economy", "image": "demonetization.jpg", "century": "21st"},
        {"date": "June 21, 2015", "fact": "The first International Day of Yoga was celebrated across India.", "category": "Culture", "image": "yoga-day.jpg", "century": "21st"},
        {"date": "September 24, 2014", "fact": "India's Mars Orbiter Mission (Mangalyaan) successfully entered Mars orbit.", "category": "Science", "image": "mangalyaan.jpg", "century": "21st"},
        {"date": "February 24, 1948", "fact": "The Constituent Assembly of India adopted Hindi as the official language.", "category": "Culture", "image": "hindi.jpg", "century": "20th"},
        {"date": "December 6, 1992", "fact": "The Babri Masjid in Ayodhya was demolished, leading to widespread communal riots.", "category": "Religion", "image": "babri.jpg", "century": "20th"},
        {"date": "March 23, 1931", "fact": "Bhagat Singh, Rajguru, and Sukhdev were hanged by the British for their revolutionary activities.", "category": "Colonial", "image": "bhagat-singh.jpg", "century": "20th"},
        {"date": "March 23, 1940", "fact": "The Lahore Resolution (Pakistan Resolution) was passed, demanding separate Muslim states.", "category": "Politics", "image": "lahore-resolution.jpg", "century": "20th"},
        {"date": "March 23, 1977", "fact": "The Emergency in India ended, and general elections were announced.", "category": "Politics", "image": "emergency-end.jpg", "century": "20th"},
        {"date": "January 30, 1948", "fact": "Mahatma Gandhi was assassinated by Nathuram Godse in Delhi.", "category": "People", "image": "gandhi-assassination.jpg", "century": "20th"},
        {"date": "July 8, 1497", "fact": "Vasco da Gama set sail from Lisbon, eventually reaching Calicut, India in 1498.", "category": "Colonial", "image": "vasco-da-gama.jpg", "century": "15th"},
        {"date": "August 2, 1858", "fact": "The Government of India Act transferred the administration of India from the East India Company to the British Crown.", "category": "Colonial", "image": "british-raj.jpg", "century": "19th"},
        {"date": "April 13, 1919", "fact": "The Jallianwala Bagh massacre occurred in Amritsar, Punjab, where British troops fired on a large crowd of unarmed Indians.", "category": "Colonial", "image": "jallianwala-bagh.jpg", "century": "20th"},
        {"date": "September 20, 1932", "fact": "Mahatma Gandhi began a fast unto death in Yerwada Jail against the British government's decision to separate the electoral system for untouchables.", "category": "Social", "image": "gandhi-fast.jpg", "century": "20th"},
        {"date": "February 13, 1931", "fact": "New Delhi was inaugurated as the capital of India by Lord Irwin.", "category": "Colonial", "image": "new-delhi.jpg", "century": "20th"},
        {"date": "November 4, 1952", "fact": "The first general elections were held in independent India.", "category": "Politics", "image": "first-election.jpg", "century": "20th"},
    ]
    
    # Filter by date if provided
    if date:
        month_day = date.strftime("%B %d")
        filtered_facts = [fact for fact in indian_facts if month_day in fact["date"]]
        if filtered_facts:
            return filtered_facts
    
    # Filter by keyword if provided
    if keyword:
        filtered_facts = [fact for fact in indian_facts if keyword.lower() in fact["fact"].lower() or keyword.lower() in fact["date"].lower()]
        if filtered_facts:
            return filtered_facts[:limit]
    
    # Filter by category if provided
    if category and category != "All":
        filtered_facts = [fact for fact in indian_facts if fact["category"] == category]
        if filtered_facts:
            return filtered_facts[:limit]
    
    # Filter by century if provided
    if century and century != "All":
        filtered_facts = [fact for fact in indian_facts if fact["century"] == century]
        if filtered_facts:
            return filtered_facts[:limit]
    
    # Return all facts if no filters or no results with filters
    return indian_facts[:limit]

# Function to get today's historical fact
def get_todays_fact():
    today = datetime.datetime.now()
    facts = fetch_indian_historical_facts(date=today)
    if facts:
        return facts
    else:
        # If no fact for today, return a random fact
        return [random.choice(fetch_indian_historical_facts())]

# Function to get a random historical fact
def get_random_fact():
    facts = fetch_indian_historical_facts()
    return random.choice(facts)

# Function to extract year from date string
def extract_year(date_str):
    try:
        return int(date_str.split(", ")[-1] if ", " in date_str else date_str.split()[-1])
    except:
        return None

# Function to apply theme based on user selection
def apply_theme(theme_choice):
    if theme_choice == "Vintage":
        st.markdown("""
        <style>
            :root {
                --primary-bg: #F8F0E3;
                --secondary-bg: #E6D7C3;
                --accent-color: #8B4513;
                --text-color: #3E2723;
                --highlight-color: #A87B51;
                --border-color: #8D6E63;
            }
            
            .main {
                background-image: url('https://img.freepik.com/free-photo/old-paper-texture_1194-6201.jpg');
                background-size: cover;
                color: var(--text-color);
            }
            .stApp {
                background-color: rgba(248, 240, 227, 0.9);
            }
            h1, h2, h3 {
                font-family: 'Playfair Display', serif;
                color: var(--accent-color);
            }
            .fact-box {
                background-color: rgba(230, 215, 195, 0.9);
                border: 2px solid var(--border-color);
                border-radius: 10px;
                padding: 20px;
                margin: 15px 0;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            }
            .fact-date {
                color: var(--accent-color);
                font-weight: bold;
                font-size: 1.2em;
            }
            .fact-content {
                color: var(--text-color);
                font-size: 1.1em;
                line-height: 1.6;
            }
            .stButton>button {
                background-color: var(--accent-color);
                color: #F8F0E3;
                border: 2px solid var(--border-color);
                border-radius: 5px;
                transition: all 0.3s ease;
            }
            .stButton>button:hover {
                background-color: var(--highlight-color);
                transform: translateY(-2px);
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            }
            .stDateInput>div>div>input {
                background-color: var(--secondary-bg);
                color: var(--text-color);
                border: 1px solid var(--border-color);
            }
            .stTextInput>div>div>input {
                background-color: var(--secondary-bg);
                color: var(--text-color);
                border: 1px solid var(--border-color);
            }
            .stSelectbox>div>div {
                background-color: var(--secondary-bg);
                color: var(--text-color);
                border: 1px solid var(--border-color);
            }
            .category-card {
                background-color: var(--secondary-bg);
                border: 1px solid var(--border-color);
                border-radius: 8px;
                padding: 15px;
                text-align: center;
                transition: all 0.3s ease;
            }
            .category-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
                background-color: var(--highlight-color);
                color: #F8F0E3;
            }
            .timeline-item {
                border-left: 3px solid var(--accent-color);
                padding-left: 15px;
                margin-bottom: 20px;
                position: relative;
            }
            .timeline-item:before {
                content: '';
                position: absolute;
                left: -10px;
                top: 0;
                width: 15px;
                height: 15px;
                border-radius: 50%;
                background-color: var(--accent-color);
            }
            .today-highlight {
                background-color: var(--highlight-color);
                color: #F8F0E3;
                padding: 10px;
                border-radius: 8px;
                font-weight: bold;
                text-align: center;
                margin: 10px 0;
                font-size: 1.2em;
            }
        </style>
        """, unsafe_allow_html=True)
    else:  # Cyber theme
        st.markdown("""
        <style>
            :root {
                --primary-bg: #0A0E17;
                --secondary-bg: #1A1E2E;
                --accent-color: #00FF9D;
                --text-color: #E0E0FF;
                --highlight-color: #0066FF;
                --border-color: #304FFE;
            }
            
            .main {
                background-color: var(--primary-bg);
                color: var(--text-color);
                background-image: linear-gradient(to bottom, rgba(10, 14, 23, 0.9), rgba(10, 14, 23, 0.95)), 
                                  url('https://www.transparenttextures.com/patterns/carbon-fibre.png');
            }
            .stApp {
                background-color: var(--primary-bg);
            }
            h1, h2, h3 {
                font-family: 'Orbitron', sans-serif;
                color: var(--accent-color);
                text-shadow: 0 0 10px rgba(0, 255, 157, 0.5);
            }
            .fact-box {
                background-color: var(--secondary-bg);
                border: 1px solid var(--accent-color);
                border-radius: 5px;
                padding: 20px;
                margin: 15px 0;
                box-shadow: 0 0 15px rgba(0, 255, 157, 0.2);
            }
            .fact-date {
                color: var(--accent-color);
                font-weight: bold;
                font-size: 1.2em;
            }
            .fact-content {
                color: var(--text-color);
                font-size: 1.1em;
                line-height: 1.6;
            }
            .stButton>button {
                background-color: var(--secondary-bg);
                color: var(--accent-color);
                border: 1px solid var(--accent-color);
                border-radius: 5px;
                transition: all 0.3s ease;
            }
            .stButton>button:hover {
                background-color: var(--accent-color);
                color: var(--primary-bg);
                transform: translateY(-2px);
                box-shadow: 0 0 15px rgba(0, 255, 157, 0.5);
            }
            .stDateInput>div>div>input {
                background-color: var(--secondary-bg);
                color: var(--text-color);
                border: 1px solid var(--accent-color);
            }
            .stTextInput>div>div>input {
                background-color: var(--secondary-bg);
                color: var(--text-color);
                border: 1px solid var(--accent-color);
            }
            .stSelectbox>div>div {
                background-color: var(--secondary-bg);
                color: var(--text-color);
                border: 1px solid var(--accent-color);
            }
            .category-card {
                background-color: var(--secondary-bg);
                border: 1px solid var(--accent-color);
                border-radius: 8px;
                padding: 15px;
                text-align: center;
                transition: all 0.3s ease;
            }
            .category-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 0 15px rgba(0, 255, 157, 0.5);
                background-color: var(--highlight-color);
                color: var(--text-color);
            }
            .timeline-item {
                border-left: 3px solid var(--accent-color);
                padding-left: 15px;
                margin-bottom: 20px;
                position: relative;
            }
            .timeline-item:before {
                content: '';
                position: absolute;
                left: -10px;
                top: 0;
                width: 15px;
                height: 15px;
                border-radius: 50%;
                background-color: var(--accent-color);
                box-shadow: 0 0 10px rgba(0, 255, 157, 0.8);
            }
            .today-highlight {
                background-color: var(--highlight-color);
                color: var(--text-color);
                padding: 10px;
                border-radius: 8px;
                font-weight: bold;
                text-align: center;
                margin: 10px 0;
                font-size: 1.2em;
                border: 1px solid var(--accent-color);
                box-shadow: 0 0 15px rgba(0, 102, 255, 0.5);
            }
        </style>
        """, unsafe_allow_html=True)

# Initialize session state variables
def init_dashboard_state():
    if 'dashboard_page' not in st.session_state:
        st.session_state.dashboard_page = 'home'
    if 'theme' not in st.session_state:
        st.session_state.theme = 'Vintage'
    if 'favorites' not in st.session_state:
        st.session_state.favorites = []
    if 'high_scores' not in st.session_state:
        st.session_state.high_scores = [
            {"name": "Rahul", "score": 95},
            {"name": "Priya", "score": 90},
            {"name": "Amit", "score": 85},
            {"name": "Sneha", "score": 80},
            {"name": "Vikram", "score": 75}
        ]

# Helper function for quiz score message
def get_score_message(percentage):
    if percentage >= 90:
        return "Outstanding! You're a true Indian history expert!"
    elif percentage >= 70:
        return "Great job! You know your Indian history well!"
    elif percentage >= 50:
        return "Good effort! You have a solid understanding of Indian history."
    else:
        return "Keep learning! Indian history has so much more to discover."

def main():
    # Initialize dashboard state
    init_dashboard_state()
    
    # Apply theme based on user selection
    apply_theme(st.session_state.theme)
    
    # Sidebar for navigation
    with st.sidebar:
        st.title("🏛️ HistoFacts")
        st.markdown("### Explore Indian History")
        
        # Today's date prominently displayed
        today = datetime.datetime.now()
        st.markdown(f"""
        <div class="today-highlight">
            Today is {today.strftime('%B %d, %Y')}
        </div>
        """, unsafe_allow_html=True)
        
        # Navigation buttons
        if st.button("🏠 Home", key="dash_home"):
            st.session_state.dashboard_page = 'home'
            st.rerun()
        if st.button("📅 Timeline", key="dash_timeline"):
            st.session_state.dashboard_page = 'timeline'
            st.rerun()
        if st.button("🔍 Search & Explore", key="dash_search"):
            st.session_state.dashboard_page = 'search'
            st.rerun()
        if st.button("❓ Quiz", key="dash_quiz"):
            # Return to main app and switch to quiz page
            st.session_state.page = "Quiz"
            st.session_state.quiz_state = "welcome"
            st.rerun()
        if st.button("🏠 Back to Main", key="dash_main"):
            st.session_state.page = "Home"
            st.rerun()
        
        # Theme selector
        st.markdown("---")
        st.subheader("Theme Settings")
        theme_option = st.radio("Select Theme:", ("Vintage", "Cyber"), 
                               index=0 if st.session_state.theme == 'Vintage' else 1)
        
        if theme_option != st.session_state.theme:
            st.session_state.theme = theme_option
            st.rerun()
        
        # Check if today is a significant date
        todays_facts = fetch_indian_historical_facts(date=today)
        if todays_facts:
            st.markdown("---")
            st.markdown("#### On this day in history:")
            for fact in todays_facts:
                year = fact["date"].split(", ")[-1] if ", " in fact["date"] else fact["date"].split()[-1]
                st.markdown(f"- {year}: {fact['fact'][:50]}...")

    # Main content based on selected page
    if st.session_state.dashboard_page == 'home':
        # Home page / Main Dashboard
        st.title("HistoFacts: Indian Historical Explorer")
        st.subheader("Discover the Rich Tapestry of Indian History")
        
        # Today's date prominently displayed
        today = datetime.datetime.now()
        st.markdown(f"""
        <div class="today-highlight">
            Today is {today.strftime('%B %d, %Y')}
        </div>
        """, unsafe_allow_html=True)
        
        # Today's historical facts
        st.markdown("## Today's Historical Facts")
        todays_facts = fetch_indian_historical_facts(date=today)
        
        if todays_facts:
            for fact in todays_facts:
                st.markdown(f"""
                <div class="fact-box">
                    <div class="fact-date">{fact['date']}</div>
                    <div class="fact-content">{fact['fact']}</div>
                    <div style="margin-top: 10px; font-style: italic;">Category: {fact['category']}</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Add to favorites button
                if st.button(f"❤️ Add to Favorites", key=f"fav_{fact['date']}_{fact['category']}"):
                    if fact not in st.session_state.favorites:
                        st.session_state.favorites.append(fact)
                        st.success("Added to favorites!")
        else:
            # If no fact for today, show a random fact
            random_fact = get_random_fact()
            st.markdown(f"""
            <div class="fact-box">
                <div class="fact-date">{random_fact['date']}</div>
                <div class="fact-content">{random_fact['fact']}</div>
                <div style="margin-top: 10px; font-style: italic;">Category: {random_fact['category']}</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Button to get a new random fact
        if st.button("Discover a New Fact"):
            random_fact = get_random_fact()
            st.markdown(f"""
            <div class="fact-box">
                <div class="fact-date">{random_fact['date']}</div>
                <div class="fact-content">{random_fact['fact']}</div>
                <div style="margin-top: 10px; font-style: italic;">Category: {random_fact['category']}</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Featured categories
        st.markdown("## Explore by Category")
        
        categories = ["Politics", "War", "Science", "Colonial", "Culture", "People"]
        cols = st.columns(3)
        
        for i, category in enumerate(categories):
            with cols[i % 3]:
                st.markdown(f"""
                <div class="category-card">
                    <h3>{category}</h3>
                    <p>Explore {category.lower()} events in Indian history</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Since the onclick doesn't work in Streamlit, add a button
                if st.button(f"Explore {category}", key=f"cat_{category}"):
                    st.session_state.selected_category = category
                    st.session_state.dashboard_page = 'search'
                    st.rerun()
        
        # Quick stats
        st.markdown("## Quick Stats")
        
        # Get all facts and extract years
        all_facts = fetch_indian_historical_facts()
        years = [extract_year(fact["date"]) for fact in all_facts]
        years = [year for year in years if year is not None]
        
        # Count facts by century
        centuries = {}
        for year in years:
            century = f"{(year // 100) + 1}th"
            if century in centuries:
                centuries[century] += 1
            else:
                centuries[century] = 1
        
        # Count facts by category
        categories = {}
        for fact in all_facts:
            category = fact["category"]
            if category in categories:
                categories[category] += 1
            else:
                categories[category] = 1
        
        # Display stats in columns
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Facts by Century")
            century_df = pd.DataFrame({
                "Century": list(centuries.keys()),
                "Count": list(centuries.values())
            })
            fig = px.bar(century_df, x="Century", y="Count", color="Count", 
                        color_continuous_scale="Viridis")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Facts by Category")
            category_df = pd.DataFrame({
                "Category": list(categories.keys()),
                "Count": list(categories.values())
            })
            fig = px.pie(category_df, values="Count", names="Category", hole=0.4)
            st.plotly_chart(fig, use_container_width=True)

    elif st.session_state.dashboard_page == 'timeline':
        st.title("Historical Timeline")
        st.write("Explore Indian historical events through an interactive timeline.")
        
        # Filters for the timeline
        st.markdown("### Filter Timeline")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            century_filter = st.selectbox("Century", ["All", "15th", "16th", "17th", "18th", "19th", "20th", "21st"])
        
        with col2:
            category_filter = st.selectbox("Category", ["All", "Politics", "War", "Science", "Colonial", "Culture", "People", "Disaster", "Terrorism", "Religion", "Economy", "Health", "Social"])
        
        with col3:
            keyword_filter = st.text_input("Keyword Search")
        
        # Apply filters to get facts
        filtered_facts = fetch_indian_historical_facts(
            century=None if century_filter == "All" else century_filter,
            category=None if category_filter == "All" else category_filter,
            keyword=keyword_filter if keyword_filter else None
        )
        
        # Sort facts by year
        filtered_facts = sorted(filtered_facts, key=lambda x: extract_year(x["date"]) if extract_year(x["date"]) else 0)
        
        # Create interactive timeline
        if filtered_facts:
            # Group facts by year for the timeline
            years = {}
            for fact in filtered_facts:
                year = extract_year(fact["date"])
                if year:
                    if year in years:
                        years[year].append(fact)
                    else:
                        years[year] = [fact]
            
            # Create timeline visualization
            timeline_data = []
            for year, facts in sorted(years.items()):
                for fact in facts:
                    timeline_data.append({
                        "Year": year,
                        "Event": fact["fact"],
                        "Category": fact["category"]
                    })
            
            timeline_df = pd.DataFrame(timeline_data)
            
            # Create interactive timeline with plotly
            fig = px.scatter(timeline_df, x="Year", y="Category", 
                            color="Category", size=[10] * len(timeline_df),
                            hover_name="Event", 
                            labels={"Year": "Year", "Category": "Category"})
            
            fig.update_layout(
                title="Interactive Timeline of Indian History",
                xaxis_title="Year",
                yaxis_title="Category",
                height=500
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Display timeline events in a scrollable format
            st.markdown("### Timeline Events")
            
            current_century = None
            for fact in filtered_facts:
                year = extract_year(fact["date"])
                if year:
                    century = f"{(year // 100) + 1}th Century"
                    
                    if century != current_century:
                        st.markdown(f"## {century}")
                        current_century = century
                    
                    st.markdown(f"""
                    <div class="timeline-item">
                        <div class="fact-date">{fact['date']}</div>
                        <div class="fact-content">{fact['fact']}</div>
                        <div style="margin-top: 10px; font-style: italic;">Category: {fact['category']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Add to favorites button
                    if st.button(f"❤️ Add to Favorites", key=f"fav_timeline_{fact['date']}_{fact['category']}"):
                        if fact not in st.session_state.favorites:
                            st.session_state.favorites.append(fact)
                            st.success("Added to favorites!")
        else:
            st.info("No events found with the selected filters. Try different criteria.")

    elif st.session_state.dashboard_page == 'search':
        st.title("Search & Explore")
        st.write("Search for historical events by keyword, date, or category.")
        
        # Search options
        search_tab, category_tab, favorites_tab = st.tabs(["Search", "Categories", "My Favorites"])
        
        with search_tab:
            st.subheader("Search Historical Facts")
            
            col1, col2 = st.columns(2)
            
            with col1:
                search_term = st.text_input("Enter keywords to search:")
            
            with col2:
                search_category = st.selectbox("Filter by Category", 
                                              ["All", "Politics", "War", "Science", "Colonial", 
                                               "Culture", "People", "Disaster", "Terrorism", 
                                               "Religion", "Economy", "Health", "Social"])
            
            if search_term or search_category != "All":
                results = fetch_indian_historical_facts(
                    keyword=search_term if search_term else None,
                    category=None if search_category == "All" else search_category
                )
                
                if results:
                    st.write(f"Found {len(results)} results:")
                    
                    for fact in results:
                        with st.expander(f"{fact['date']} - {fact['fact'][:50]}..."):
                            st.markdown(f"""
                            <div class="fact-box">
                                <div class="fact-date">{fact['date']}</div>
                                <div class="fact-content">{fact['fact']}</div>
                                <div style="margin-top: 10px; font-style: italic;">Category: {fact['category']}</div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Simulated image display
                            st.image("https://via.placeholder.com/600x300?text=Historical+Image", 
                                    caption=f"Illustration related to {fact['date']} event")
                            
                            # Source information
                            st.markdown("*Sources:*")
                            st.markdown("- National Archives of India")
                            st.markdown("- Historical Society of India")
                            
                            # Add to favorites button
                            if st.button(f"❤️ Add to Favorites", key=f"fav_search_{fact['date']}_{fact['category']}"):
                                if fact not in st.session_state.favorites:
                                    st.session_state.favorites.append(fact)
                                    st.success("Added to favorites!")
                else:
                    st.write(f"No results found for '{search_term}'. Try different keywords.")
        
        with category_tab:
            st.subheader("Browse by Category")
            
            # Display categories in a grid
            categories = ["Politics", "War", "Science", "Colonial", "Culture", "People", 
                         "Disaster", "Terrorism", "Religion", "Economy", "Health", "Social"]
            
            # Create 3 columns
            cols = st.columns(3)
            
            for i, category in enumerate(categories):
                with cols[i % 3]:
                    st.markdown(f"""
                    <div class="category-card">
                        <h3>{category}</h3>
                        <p>Explore {category.lower()} events in Indian history</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button(f"View {category} Events", key=f"cat_view_{category}"):
                        category_facts = fetch_indian_historical_facts(category=category)
                        
                        if category_facts:
                            st.subheader(f"{category} Events in Indian History")
                            
                            for fact in category_facts:
                                st.markdown(f"""
                                <div class="fact-box">
                                    <div class="fact-date">{fact['date']}</div>
                                    <div class="fact-content">{fact['fact']}</div>
                                </div>
                                """, unsafe_allow_html=True)
        
        with favorites_tab:
            st.subheader("My Favorite Historical Facts")
            
            if st.session_state.favorites:
                for i, fact in enumerate(st.session_state.favorites):
                    st.markdown(f"""
                    <div class="fact-box">
                        <div class="fact-date">{fact['date']}</div>
                        <div class="fact-content">{fact['fact']}</div>
                        <div style="margin-top: 10px; font-style: italic;">Category: {fact['category']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button("Remove from Favorites", key=f"remove_fav_{i}"):
                        st.session_state.favorites.remove(fact)
                        st.success("Removed from favorites!")
                        st.rerun()
            else:
                st.info("You haven't added any favorites yet. Explore historical facts and add them to your favorites!")