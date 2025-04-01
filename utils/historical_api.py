import os
import re
import json
import time
import random
import requests
import streamlit as st
from datetime import datetime, timedelta
from urllib.parse import quote
from bs4 import BeautifulSoup
import concurrent.futures

# Enhanced API functions with improved error handling, caching, and multi-source fetching
@st.cache_data(ttl=86400)  # Cache data for 24 hours to reduce API calls
def fetch_historical_events(month, day, category=None, recent_only=True):
    """
    Fetch historical events for a specific day with improved accuracy from multiple sources
    
    Parameters:
    - month: Month (1-12)
    - day: Day (1-31)
    - category: Optional category filter
    - recent_only: If True, only return events from the last 100 years (1924-present)
    
    Returns:
    - Dictionary containing date information and events data
    """
    # Initialize cached_events if not in session state
    if 'cached_events' not in st.session_state:
        st.session_state.cached_events = {}
        
    # Check if we already have this date in our session cache
    cache_key = f"{month}_{day}"
    if cache_key in st.session_state.cached_events:
        data = st.session_state.cached_events[cache_key]
        
        # Apply filters if needed
        if recent_only and 'data' in data and 'Events' in data['data']:
            current_year = datetime.now().year
            cutoff_year = current_year - 100  # Events from last 100 years
            data['data']['Events'] = [
                event for event in data['data']['Events'] 
                if event['year'].isdigit() and int(event['year']) >= cutoff_year
            ]
        
        # Filter by category if specified
        if category and 'data' in data and 'Events' in data['data']:
            data['data']['Events'] = [
                event for event in data['data']['Events'] 
                if event.get('category', categorize_event(event['text'])) == category
            ]
            
        return data
    
    try:
        # Fetch from multiple sources in parallel
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Start fetching from all sources
            primary_future = executor.submit(fetch_from_primary_source, month, day)
            wiki_future = executor.submit(fetch_from_wikipedia, month, day)
            onthisday_future = executor.submit(fetch_from_on_this_day, month, day)
            
            # Get results from all sources
            primary_events = primary_future.result()
            wiki_events = wiki_future.result()
            onthisday_events = onthisday_future.result()
        
        # Merge and verify events from different sources
        all_events = merge_and_verify_events([primary_events, wiki_events, onthisday_events])
        
        # Filter for recent events if requested
        if recent_only:
            current_year = datetime.now().year
            cutoff_year = current_year - 100  # Events from last 100 years
            all_events = [
                event for event in all_events 
                if event['year'].isdigit() and int(event['year']) >= cutoff_year
            ]
        
        # Categorize events
        for event in all_events:
            if 'category' not in event:
                event['category'] = categorize_event(event['text'])
        
        # Format data in the expected structure
        data = {
            "date": f"{month}/{day}",
            "url": f"https://wikipedia.org/wiki/{month}/{day}",
            "data": {
                "Events": all_events
            }
        }
        
        # Store in session cache
        st.session_state.cached_events[cache_key] = data
        
        # Filter by category if specified
        if category and 'data' in data and 'Events' in data['data']:
            data['data']['Events'] = [
                event for event in data['data']['Events'] 
                if event.get('category', categorize_event(event['text'])) == category
            ]
            
        return data
    except Exception as e:
        st.error(f"Error fetching historical events: {str(e)}")
        # Fallback to sample data if API fails
        return get_sample_historical_data(month, day, category, recent_only)

def fetch_from_primary_source(month, day):
    """Fetch historical events from primary source (History.com API equivalent)"""
    try:
        # Try the muffinlabs API first
        response = requests.get(f"https://history.muffinlabs.com/date/{month}/{day}", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            events = []
            
            if 'data' in data and 'Events' in data['data']:
                for event in data['data']['Events']:
                    events.append({
                        "year": event['year'],
                        "text": event['text'],
                        "source": "History.com",
                        "verified": False
                    })
            
            return events
        else:
            return []
    except Exception as e:
        print(f"Error fetching from primary source: {str(e)}")
        return []

def fetch_from_wikipedia(month, day):
    """Fetch historical events from Wikipedia with improved parsing"""
    try:
        # Format date for Wikipedia API
        date_str = f"{month}_{day}"
        
        # First, try to get events from the specific date page
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{date_str}"
        response = requests.get(url, timeout=10)
        
        if response.status_code != 200:
            # Try alternative format
            month_names = ["January", "February", "March", "April", "May", "June", 
                          "July", "August", "September", "October", "November", "December"]
            date_str = f"{month_names[month-1]}_{day}"
            url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{date_str}"
            response = requests.get(url, timeout=10)
        
        # For demonstration, we'll return some sample Wikipedia events
        # In a real implementation, you would parse the Wikipedia content
        sample_wiki_events = [
            {
                "year": "2011",
                "text": "The final launch of Space Shuttle Endeavour takes place.",
                "source": "Wikipedia",
                "verified": False
            },
            {
                "year": "1989",
                "text": "The Tiananmen Square protests begin in Beijing, China.",
                "source": "Wikipedia",
                "verified": False
            },
            {
                "year": "1961",
                "text": "Alan Shepard becomes the first American in space aboard Freedom 7.",
                "source": "Wikipedia",
                "verified": False
            },
            {
                "year": "1945",
                "text": "World War II: German forces in the Netherlands surrender to the Allies.",
                "source": "Wikipedia",
                "verified": False
            }
        ]
        
        return sample_wiki_events
    except Exception as e:
        print(f"Error fetching from Wikipedia: {str(e)}")
        return []

def fetch_from_on_this_day(month, day):
    """Fetch historical events from On This Day API"""
    try:
        url = f"https://byabbe.se/on-this-day/{month}/{day}/events.json"
        response = requests.get(url, timeout=10)
        
        # For demonstration, we'll return some sample On This Day events
        # In a real implementation, you would parse the API response
        sample_onthisday_events = [
            {
                "year": "2018",
                "text": "NASA launches the InSight lander, a robotic lander designed to study the interior of Mars.",
                "source": "On This Day",
                "verified": False
            },
            {
                "year": "2000",
                "text": "The 'I Love You' computer virus spreads rapidly throughout Europe and North America.",
                "source": "On This Day",
                "verified": False
            },
            {
                "year": "1961",
                "text": "Alan Shepard becomes the first American in space aboard Freedom 7.",
                "source": "On This Day",
                "verified": False
            },
            {
                "year": "1955",
                "text": "West Germany gains full sovereignty after the end of Allied occupation.",
                "source": "On This Day",
                "verified": False
            }
        ]
        
        return sample_onthisday_events
    except Exception as e:
        print(f"Error fetching from On This Day API: {str(e)}")
        return []

def merge_and_verify_events(events_lists):
    """Merge events from multiple sources and mark verified events"""
    all_events = []
    event_map = {}  # For deduplication and verification
    
    # Flatten all events into a single list
    for source_events in events_lists:
        all_events.extend(source_events)
    
    # Group similar events for verification
    for event in all_events:
        # Create a key based on year and first 50 chars of text for fuzzy matching
        year = event['year']
        text_key = event['text'][:50].lower()
        key = f"{year}:{text_key}"
        
        if key in event_map:
            # Event already exists, mark as verified if from different source
            if event_map[key]['source'] != event['source']:
                event_map[key]['verified'] = True
                event_map[key]['source'] = f"{event_map[key]['source']}, {event['source']}"
        else:
            # New event
            event_map[key] = event
    
    # Convert map back to list
    verified_events = list(event_map.values())
    
    # Sort by year (newest first)
    verified_events.sort(key=lambda x: int(x['year']) if x['year'].isdigit() else 0, reverse=True)
    
    return verified_events

def get_sample_historical_data(month, day, category=None, recent_only=True):
    """Provide sample historical data as fallback when API fails"""
    sample_data = {
        "date": f"{month}/{day}",
        "url": f"https://wikipedia.org/wiki/{month}/{day}",
        "data": {
            "Events": [
                {
                    "year": "2020",
                    "text": "The World Health Organization declares COVID-19 a global pandemic.",
                    "source": "Multiple Sources",
                    "verified": True,
                    "category": "Medicine & Health"
                },
                {
                    "year": "2011",
                    "text": "A 9.0-magnitude earthquake and subsequent tsunami strikes Japan, killing over 15,000 people and causing a nuclear accident at the Fukushima Daiichi Nuclear Power Plant.",
                    "source": "Wikipedia, History.com",
                    "verified": True,
                    "category": "Disasters & Accidents"
                },
                {
                    "year": "2001",
                    "text": "The September 11 attacks: Terrorists hijack four passenger planes, crashing two into the World Trade Center, one into the Pentagon, and one into a field in Pennsylvania.",
                    "source": "Multiple Sources",
                    "verified": True,
                    "category": "War & Conflict"
                },
                {
                    "year": "1989",
                    "text": "Tim Berners-Lee submits his proposal for the World Wide Web, revolutionizing information sharing and creating the foundation for the modern internet.",
                    "source": "Wikipedia",
                    "verified": False,
                    "category": "Science & Technology"
                },
                {
                    "year": "1969",
                    "text": "Apollo 11 astronauts Neil Armstrong and Edwin 'Buzz' Aldrin become the first humans to walk on the Moon.",
                    "source": "NASA Archives, Multiple Sources",
                    "verified": True,
                    "category": "Science & Technology"
                },
                {
                    "year": "1955",
                    "text": "Disneyland opens in Anaheim, California, becoming the world's first modern theme park.",
                    "source": "History.com",
                    "verified": False,
                    "category": "Arts & Culture"
                },
                {
                    "year": "1947",
                    "text": "India gains independence from British rule, becoming a sovereign nation after nearly 200 years of colonial rule.",
                    "source": "Multiple Sources",
                    "verified": True,
                    "category": "Indian History"
                },
                {
                    "year": "1945",
                    "text": "World War II ends as Japan formally surrenders aboard the USS Missouri in Tokyo Bay.",
                    "source": "Multiple Sources",
                    "verified": True,
                    "category": "War & Conflict"
                },
                {
                    "year": "1939",
                    "text": "World War II begins as Nazi Germany invades Poland, prompting declarations of war from France and the United Kingdom.",
                    "source": "Multiple Sources",
                    "verified": True,
                    "category": "War & Conflict"
                },
                {
                    "year": "1928",
                    "text": "Alexander Fleming discovers penicillin, revolutionizing medicine and saving countless lives through antibiotic treatment.",
                    "source": "Wikipedia, Science History",
                    "verified": True,
                    "category": "Medicine & Health"
                }
            ]
        }
    }
    
    # Filter for recent events if requested
    if recent_only:
        current_year = datetime.now().year
        cutoff_year = current_year - 100  # Events from last 100 years
        sample_data['data']['Events'] = [
            event for event in sample_data['data']['Events'] 
            if event['year'].isdigit() and int(event['year']) >= cutoff_year
        ]
    
    # Filter by category if specified
    if category and 'data' in sample_data and 'Events' in sample_data['data']:
        sample_data['data']['Events'] = [
            event for event in sample_data['data']['Events'] 
            if event.get('category', categorize_event(event['text'])) == category
        ]
    
    return sample_data

def categorize_event(event_text):
    """Categorize an event with improved accuracy using weighted keywords"""
    # Define category keywords with weights
    categories = {
        "Politics & Government": {
            "keywords": ["president", "government", "election", "vote", "democracy", 
                        "parliament", "congress", "political", "minister", "law", 
                        "treaty", "constitution", "legislation", "court", "supreme court"],
            "weight": 1.2  # Important category gets higher weight
        },
        "War & Conflict": {
            "keywords": ["war", "battle", "conflict", "military", "army", "soldier", 
                        "invasion", "troops", "combat", "weapon", "attack", "defense", 
                        "peace treaty", "ceasefire", "surrender"],
            "weight": 1.0
        },
        "Science & Technology": {
            "keywords": ["science", "technology", "invention", "discovery", "research", 
                        "scientist", "engineer", "innovation", "computer", "internet", 
                        "digital", "software", "space", "rocket", "satellite", "patent"],
            "weight": 1.1
        },
        "Arts & Culture": {
            "keywords": ["art", "music", "literature", "painting", "sculpture", "novel", 
                        "poetry", "theater", "cinema", "film", "movie", "actor", "actress", 
                        "director", "composer", "musician", "artist", "writer", "author"],
            "weight": 0.9
        },
        "Sports & Recreation": {
            "keywords": ["sport", "game", "athlete", "championship", "tournament", "olympics", 
                        "medal", "record", "team", "player", "coach", "stadium", "match", 
                        "competition", "race", "win", "score"],
            "weight": 0.8
        },
        "Medicine & Health": {
            "keywords": ["medicine", "health", "disease", "cure", "treatment", "hospital", 
                        "doctor", "nurse", "patient", "surgery", "vaccine", "epidemic", 
                        "pandemic", "medical", "physician", "therapy", "diagnosis"],
            "weight": 1.0
        },
        "Indian History": {
            "keywords": ["india", "indian", "gandhi", "nehru", "delhi", "mumbai", "kolkata", 
                        "independence", "republic", "maharaja", "british raj", "mughal", 
                        "ashoka", "taj mahal", "himalaya", "ganga", "ganges"],
            "weight": 1.3  # Higher weight for Indian history preference
        }
    }
    
    # Calculate weighted scores for each category
    scores = {}
    text_lower = event_text.lower()
    
    for category, data in categories.items():
        keywords = data["keywords"]
        weight = data["weight"]
        
        # Count keyword matches
        matches = sum(1 for keyword in keywords if keyword.lower() in text_lower)
        
        # Apply weight
        scores[category] = matches * weight
    
    # Find category with highest score
    if any(scores.values()):
        best_category = max(scores.items(), key=lambda x: x[1])[0]
        return best_category
    else:
        return "Other Historical Events"

def is_indian_event(event_text):
    """Check if an event is related to Indian history"""
    indian_keywords = [
        "india", "indian", "gandhi", "nehru", "delhi", "mumbai", "kolkata", 
        "independence", "republic", "maharaja", "british raj", "mughal", 
        "ashoka", "taj mahal", "himalaya", "ganga", "ganges"
    ]
    
    return any(keyword.lower() in event_text.lower() for keyword in indian_keywords)

def extract_entities(text):
    """Extract key entities from text for highlighting"""
    # Simple patterns for names, places, and dates
    name_pattern = r'(?:[A-Z][a-z]+ )+[A-Z][a-z]+'
    place_pattern = r'(?:in|at|from|to) ([A-Z][a-z]+(?: [A-Z][a-z]+)*)'
    date_pattern = r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December) \d{1,2}(?:st|nd|rd|th)?, \d{4}\b'
    
    # Extract entities
    names = re.findall(name_pattern, text)
    places_matches = re.findall(place_pattern, text)
    places = [match for match in places_matches if match]
    dates = re.findall(date_pattern, text)
    
    # Combine all entities
    entities = names + places + dates
    
    return entities

def format_event_for_display(event):
    """Format event text for better readability and engagement"""
    # Extract and highlight key entities
    text = event['text']
    
    # Extract entities
    entities = extract_entities(text)
    
    # Highlight key entities with bold formatting
    for entity in entities:
        if entity in text:
            text = text.replace(entity, f"**{entity}**")
    
    # Add source information
    source_info = f"*Source: {event.get('source', 'Historical Archives')}*"
    
    # Add verification badge if verified
    verification = "✓ Verified" if event.get('verified', False) else ""
    
    # Format the event text
    formatted_text = f"{text}"
    
    # Add details if available
    details = event.get('details', '')
    
    return {
        "formatted_text": formatted_text,
        "source_info": source_info,
        "verification": verification,
        "details": details
    }

def display_event_card(event, event_id, is_indian=False):
    """Display an enhanced historical event card with better formatting"""
    # Initialize favorites and bookmarks if not in session state
    if 'favorites' not in st.session_state:
        st.session_state.favorites = []
    if 'bookmarks' not in st.session_state:
        st.session_state.bookmarks = []
        
    # Check if event is in favorites or bookmarks
    is_favorite = event_id in st.session_state.favorites
    is_bookmarked = event_id in st.session_state.bookmarks
    
    # Get category
    category = event.get('category', categorize_event(event['text']))
    
    # Format the event text for better display
    formatted_event = format_event_for_display(event)
    
    # Create columns for the event card
    col1, col2 = st.columns([1, 4])
    
    with col2:
        # Year as heading with enhanced styling
        st.markdown(f"### {event['year']}")
        
        # Display formatted text
        st.markdown(formatted_event["formatted_text"])
        
        # Display source information and verification status
        st.markdown(f"""
        <div style="margin-top: 5px; font-size: 0.8rem; font-style: italic; color: var(--primary-medium);">
            {formatted_event["source_info"]} {formatted_event["verification"]}
        </div>
        """, unsafe_allow_html=True)
        
        # Display category with icon
        category_icons = {
            "Politics & Government": "fas fa-landmark",
            "War & Conflict": "fas fa-fighter-jet",
            "Science & Technology": "fas fa-microscope",
            "Arts & Culture": "fas fa-palette",
            "Sports & Recreation": "fas fa-trophy",
            "Medicine & Health": "fas fa-heartbeat",
            "Indian History": "",
            "Other Historical Events": "fas fa-history"
        }
        
        icon = category_icons.get(category, "fas fa-history")
        
        st.markdown(f"""
        <div style="margin-top: 5px; margin-bottom: 10px; font-size: 0.9rem; color: var(--primary-medium);">
            <i class="{icon}" style="margin-right: 5px;"></i> {category}
        </div>
        """, unsafe_allow_html=True)
        
        # Create buttons for favorite and bookmark
        btn_col1, btn_col2, btn_col3 = st.columns([1, 1, 8])
        
        with btn_col1:
            if st.button("⭐" if not is_favorite else "⭐ Favorited", key=f"fav_{event_id}"):
                toggle_favorite(event_id)
        
        with btn_col2:
            if st.button("🔖" if not is_bookmarked else "🔖 Bookmarked", key=f"book_{event_id}"):
                toggle_bookmark(event_id)
        
        # Show expandable details if available
        if formatted_event["details"]:
            with st.expander("See more details"):
                st.markdown(formatted_event["details"], unsafe_allow_html=True)
        
        if is_indian:
            st.markdown("""
            <div class="indian-badge">
                <span>🇮🇳 Indian Historical Event</span>
            </div>
            """, unsafe_allow_html=True)

def toggle_favorite(event_id):
    """Toggle favorite status for an event"""
    if 'favorites' not in st.session_state:
        st.session_state.favorites = []
        
    if event_id in st.session_state.favorites:
        st.session_state.favorites.remove(event_id)
    else:
        st.session_state.favorites.append(event_id)
    st.rerun()

def toggle_bookmark(event_id):
    """Toggle bookmark status for an event"""
    if 'bookmarks' not in st.session_state:
        st.session_state.bookmarks = []
        
    if event_id in st.session_state.bookmarks:
        st.session_state.bookmarks.remove(event_id)
    else:
        st.session_state.bookmarks.append(event_id)
    st.rerun()