import streamlit as st
from datetime import datetime, timedelta
import requests
import json
import random
import os
import re
from urllib.parse import quote
import time
import sys

# Add the parent directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Import the enhanced historical API
from utils.historical_api import (
    fetch_historical_events,
    categorize_event,
    display_event_card,
    is_indian_event,
    toggle_favorite,
    toggle_bookmark
)

# Add custom CSS with improved styling and dark mode support
def add_custom_css():
    st.markdown("""
    <style>
    :root {
      --primary-dark: #1c3144;      
      --primary-medium: #2d4b6a;    
      --primary-light: #3e6b8d;     
      --accent-gold: #d9a566;       
      --accent-copper: #b87333;     
      --text-light: #f4f1e9;        
      --text-dark: #142231;         
      --background-light: #f7f3ea;  
      --background-cream: #f2e8d5;  
      --transition-speed: 0.3s;
      --border-radius: 12px;
      --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.1);
      --shadow-md: 0 4px 12px rgba(0, 0, 0, 0.15);
      --shadow-lg: 0 8px 24px rgba(0, 0, 0, 0.2);
    }
    
    .dark-mode {
      --primary-dark: #0f1a24;
      --primary-medium: #1e3a54;
      --primary-light: #2c5277;
      --accent-gold: #e6b980;
      --accent-copper: #d18f4a;
      --text-light: #f4f1e9;
      --text-dark: #e0dcd3;
      --background-light: #121212;
      --background-cream: #1e1e1e;
    }
    
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700&family=Lora:wght@400;500;600&display=swap');

    .stApp {
        background-color: var(--background-light);
        color: var(--text-dark);
        background-image: url("data:image/svg+xml,%3Csvg width='100' height='100' viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M11 18c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm48 25c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm-43-7c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm63 31c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zM34 90c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm56-76c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zM12 86c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm28-65c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm23-11c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm-6 60c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm29 22c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zM32 63c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm57-13c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm-9-21c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM60 91c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM35 41c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM12 60c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2z' fill='%233e6b8d' fill-opacity='0.05' fill-rule='evenodd'/%3E%3C/svg%3E");
        transition: all 0.3s ease;
    }
    
    .dark-mode .stApp {
        background-image: url("data:image/svg+xml,%3Csvg width='100' height='100' viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M11 18c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm48 25c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm-43-7c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm63 31c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zM34 90c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm56-76c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zM12 86c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm28-65c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm23-11c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm-6 60c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm29 22c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zM32 63c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm57-13c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm-9-21c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM60 91c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM35 41c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM12 60c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2z' fill='%232c5277' fill-opacity='0.05' fill-rule='evenodd'/%3E%3C/svg%3E");
    }
    
    .css-18e3th9, .css-1d391kg {
        background: transparent;
    }
    
    body, .stTextInput, .stSelectbox {
        font-family: 'Lora', Georgia, serif;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Playfair Display', serif;
        font-weight: 700;
        color: white;
    }
    
    .dark-mode h1, .dark-mode h2, .dark-mode h3, .dark-mode h4, .dark-mode h5, .dark-mode h6 {
        color: var(--text-light);
    }
    
    h1 {
        font-size: 2.5rem;
        letter-spacing: 1px;
    }
    
    a {
        text-decoration: none;
        color: inherit;
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(to bottom, var(--primary-dark), #142231);
        color: white;
    }
    
    .sidebar-icon {
        background-color: rgba(255, 255, 255, 0.1);
        width: 50px;
        height: 50px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 1rem;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        transition: all var(--transition-speed) ease;
        font-size: 1.2rem;
        margin-left: auto;
        margin-right: auto;
    }
    
    .sidebar-icon:hover {
        background-color: var(--accent-gold);
        transform: translateY(-3px);
        border-radius: 16px;
        color: var(--primary-dark);
    }
    
    
    .profile-icon {
        width: 56px;
        height: 56px;
        background-color: var(--primary-light);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 24px;
        position: relative;
        transition: all var(--transition-speed) ease;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        margin-left: auto;
        margin-right: auto;
    }
    
    .profile-icon i {
        font-size: 30px;
    }
    
    .profile-icon:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
        background-color: var(--accent-gold);
        color: var(--primary-dark);
    }
    
    .divider {
        height: 1px;
        background-color: rgba(255, 255, 255, 0.2);
        margin: 1rem 0;
    }
    
    .header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 1.5rem 0;
        border-bottom: 1px solid rgba(0, 0, 0, 0.1);
        margin-bottom: 1.5rem;
        background: linear-gradient(to right, var(--primary-dark), var(--primary-medium));
        color: white;
        box-shadow: var(--shadow-md);
        border-radius: var(--border-radius);
    }
    
    .dark-mode .header {
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .logo h1 {
        margin: 0;
        font-family: 'Playfair Display', serif;
        font-size: 36px;
        font-weight: 700;
        color: var(--text-light);
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
        letter-spacing: 1px;
    }
    
    .search-bar {
        display: flex;
        align-items: center;
        background-color: rgba(255, 255, 255, 0.15);
        border-radius: 24px;
        padding: 10px 18px;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
        transition: all var(--transition-speed) ease;
        border: 1px solid rgba(255, 255, 255, 0.1);
        width: 100%;
    }
    
    .search-bar:focus-within {
        background-color: rgba(255, 255, 255, 0.25);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        transform: translateY(-2px);
    }
    
    .stTextInput input {
        background-color: rgba(255, 255, 255, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.2);
        color: var(--text-light);
        border-radius: 24px;
        padding: 10px 18px;
        transition: all var(--transition-speed) ease;
    }
    
    .stTextInput input:focus {
        background-color: rgba(255, 255, 255, 0.25);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        border-color: var(--accent-gold);
    }
    
    .stTextInput input::placeholder {
        color: rgba(255, 255, 255, 0.6);
    }
    
    .icon {
        font-size: 1.5rem;
        color: var(--accent-gold);
        transition: all var(--transition-speed) ease;
    }
    
    .icon:hover {
        transform: scale(1.1);
        color: var(--text-light);
    }
    
    .fact-section {
        background: linear-gradient(135deg, var(--primary-medium), var(--primary-dark));
        border-radius: var(--border-radius);
        padding: 36px;
        box-shadow: var(--shadow-md);
        color: var(--text-light);
        position: relative;
        overflow: hidden;
        margin-bottom: 1.5rem;
        transition: transform var(--transition-speed) ease, box-shadow var(--transition-speed) ease;
    }
    
    .fact-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-image: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.05'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
        opacity: 0.1;
        z-index: 0;
    }
    
    .fact-section:hover {
        transform: translateY(-5px);
        box-shadow: var(--shadow-lg);
    }
    
    .section-title {
        font-family: 'Playfair Display', serif;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 1.5rem;
        color: var(--text-light);
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
        letter-spacing: 1px;
        position: relative;
        z-index: 1;
    }
    
    .fact-highlight {
        background-color: rgba(0, 0, 0, 0.2);
        border-radius: var(--border-radius);
        padding: 28px;
        margin-bottom: 28px;
        animation: pulse 3s infinite alternate;
        border: 1px solid rgba(255, 255, 255, 0.1);
        position: relative;
        z-index: 1;
        display: flex;
        gap: 20px;
    }
    
    @keyframes pulse {
        0% {
            box-shadow: 0 0 0 0 rgba(217, 165, 102, 0.4);
        }
        100% {
            box-shadow: 0 0 0 20px rgba(217, 165, 102, 0);
        }
    }
    
    .highlight {
        font-size: 1.5rem;
        font-weight: 500;
        color: #142231;
        margin: 0;
        letter-spacing: 0.5px;
        line-height: 1.4;
    }
    
    .info-link {
        display: inline-block;
        background-color: var(--accent-gold);
        color: var(--primary-dark);
        text-decoration: none;
        font-weight: 600;
        padding: 12px 30px;
        border-radius: 30px;
        margin-top: 0.5rem;
        transition: all var(--transition-speed) ease;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        position: relative;
        z-index: 1;
    }
    
    .info-link:hover {
        background-color: var(--text-light);
        transform: translateY(-3px);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
    }
    
    .section-header {
        display: flex;
        align-items: center;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid rgba(0, 0, 0, 0.1);
        
    }
    
    .dark-mode .section-header {
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .section-header i {
        font-size: 32px;
        color: var(--primary-dark);
        background-color: rgba(255, 255, 255, 0.5);
        width: 50px;
        height: 50px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: var(--shadow-sm);
        margin-right: 15px;
    }
    
    .dark-mode .section-header i {
        color: --primary-dark);
        background-color: rgba(255, 255, 255, 0.1);
    }
    
    .section-header h3 {
        margin: 0;
        font-size: 1.5rem;
        color: var(--primary-dark);
    }
    
    .dark-mode .section-header h3 {
        color: --primary-dark;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
        background-color: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(45, 75, 106, 0.1);
        color: var(--primary-dark);
        border-radius: 4px 4px 0 0;
        padding: 10px 20px;
        font-family: 'Playfair Display', serif;
    }
    
    .dark-mode .stTabs [data-baseweb="tab"] {
        background-color: rgba(45, 75, 106, 0.3);
        color: var(--text-light);
    }
    
    .stTabs [aria-selected="true"] {
        background-color: var(--primary-medium);
        color: var(--text-light);
    }
    
    .stAlert {
        background-color: var(--background-cream);
        color: var(--text-dark);
        border-radius: var(--border-radius);
        border-left: 4px solid var(--primary-medium);
    }
    
    .dark-mode .stAlert {
        background-color: rgba(30, 30, 30, 0.7);
        color: var(--text-light);
    }
    
    /* Hide Streamlit default elements */
    #MainMenu, footer, header {
        visibility: hidden;
    }
    
    /* Event card styling */
    .event-card {
        background-color: rgba(255, 255, 255, 0.9);
        border-radius: var(--border-radius);
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: var(--shadow-md);
        transition: transform var(--transition-speed) ease, box-shadow var(--transition-speed) ease;
    }
    
    .dark-mode .event-card {
        background-color: rgba(30, 30, 30, 0.9);
    }
    
    .event-card:hover {
        transform: translateY(-3px);
        box-shadow: var(--shadow-lg);
    }
    
    .event-content {
        flex: 1;
    }
    
    .event-year {
        font-family: 'Playfair Display', serif;
        font-size: 1.4rem;
        color: --primary-dark;
        margin: 0 0 8px 0;
    }
    
    .dark-mode .event-year {
        color: --primary-dark ;
    }
    
    .event-text {
        color: var(--text-dark);
        margin-bottom: 10px;
    }
    
    .dark-mode .event-text {
        color: --primary-dark;
    }
    
    .event-actions {
        display: flex;
        gap: 10px;
    }
    
    .event-button {
        background-color: var(--primary-light);
        color: white;
        border: none;
        border-radius: 20px;
        padding: 5px 15px;
        cursor: pointer;
        transition: all var(--transition-speed) ease;
    }
    
    .event-button:hover {
        background-color: var(--primary-dark);
    }
    
    .favorite-active {
        background-color: var(--accent-gold);
        color: var(--primary-dark);
    }
    
    .bookmark-active {
        background-color: var(--accent-copper);
        color: white;
    }
    
    /* Button styling for favorite and bookmark */
    .stButton > button {
        background-color: var(--primary-light);
        color: white !important;
        border: none;
        border-radius: 20px;
        padding: 5px 15px;
        cursor: pointer;
        transition: all var(--transition-speed) ease;
        font-weight: 500;
        width: 100%;
    }
    
    .stButton > button:hover {
        background-color: var(--primary-dark);
        color: white !important;
    }
    
    /* Scrollable container for events */
    .scrollable-events {
        max-height: 600px;
        overflow-y: auto;
        padding-right: 10px;
    }
    
    .scrollable-events::-webkit-scrollbar {
        width: 8px;
    }
    
    .scrollable-events::-webkit-scrollbar-track {
        background: rgba(0, 0, 0, 0.05);
        border-radius: 10px;
    }
    
    .dark-mode .scrollable-events::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.05);
    }
    
    .scrollable-events::-webkit-scrollbar-thumb {
        background: var(--primary-light);
        border-radius: 10px;
    }
    
    .scrollable-events::-webkit-scrollbar-thumb:hover {
        background: var(--primary-medium);
    }
    
    /* Timeline styling */
    .timeline {
        position: relative;
        max-width: 1200px;
        margin: 0 auto;
        padding: 20px 0;
    }
    
    .timeline::after {
        content: '';
        position: absolute;
        width: 6px;
        background-color: var(--primary-medium);
        top: 0;
        bottom: 0;
        left: 50%;
        margin-left: -3px;
        border-radius: 10px;
    }
    
    .dark-mode .timeline::after {
        background-color: var(--primary-light);
    }
    
    .timeline-container {
        padding: 10px 40px;
        position: relative;
        background-color: inherit;
        width: 50%;
    }
    
    .timeline-container::after {
        content: '';
        position: absolute;
        width: 20px;
        height: 20px;
        right: -10px;
        background-color: var(--accent-gold);
        border: 4px solid var(--primary-dark);
        top: 15px;
        border-radius: 50%;
        z-index: 1;
    }
    
    .dark-mode .timeline-container::after {
        border: 4px solid var(--primary-light);
    }
    
    .timeline-left {
        left: 0;
    }
    
    .timeline-right {
        left: 50%;
    }
    
    .timeline-left::before {
        content: " ";
        height: 0;
        position: absolute;
        top: 22px;
        width: 0;
        z-index: 1;
        right: 30px;
        border: medium solid var(--background-cream);
        border-width: 10px 0 10px 10px;
        border-color: transparent transparent transparent var(--background-cream);
    }
    
    .dark-mode .timeline-left::before {
        border-color: transparent transparent transparent var(--background-cream);
    }
    
    .timeline-right::before {
        content: " ";
        height: 0;
        position: absolute;
        top: 22px;
        width: 0;
        z-index: 1;
        left: 30px;
        border: medium solid var(--background-cream);
        border-width: 10px 10px 10px 0;
        border-color: transparent var(--background-cream) transparent transparent;
    }
    
    .dark-mode .timeline-right::before {
        border-color: transparent var(--background-cream) transparent transparent;
    }
    
    .timeline-right::after {
        left: -10px;
    }
    
    .timeline-content {
        padding: 20px;
        background-color: var(--background-cream);
        position: relative;
        border-radius: var(--border-radius);
        box-shadow: var(--shadow-md);
    }
    
    .dark-mode .timeline-content {
        background-color: var(--background-cream);
    }
    
    .timeline-content h2 {
        color: var(--primary-dark);
        margin-top: 0;
    }
    
    .dark-mode .timeline-content h2 {
        color: var(--primary-dark);
    }
    
    .timeline-content p {
        margin-bottom: 0;
        color: #142231;
    }
    
    .dark-mode .timeline-content p {
        color: var(--text-dark);
    }
    
    /* Search results styling */
    .search-result {
        background-color: rgba(255, 255, 255, 0.9);
        border-radius: var(--border-radius);
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: var(--shadow-md);
        transition: transform var(--transition-speed) ease, box-shadow var(--transition-speed) ease;
    }
    
    .dark-mode .search-result {
        background-color: rgba(30, 30, 30, 0.9);
    }
    
    .search-result:hover {
        transform: translateY(-3px);
        box-shadow: var(--shadow-lg);
    }
    
    .search-result h3 {
        color: var(--primary-dark);
        margin-top: 0;
    }
    
    .dark-mode .search-result h3 {
        color: var(--text-light);
    }
    
    .search-result p {
        margin-bottom: 10px;
    }
    
    .search-result-source {
        font-size: 0.8rem;
        color: var(--primary-medium);
        font-style: italic;
    }
    
    .dark-mode .search-result-source {
        color: var(--accent-gold);
    }
    
    .search-result-link {
        display: inline-block;
        color: var(--primary-medium);
        font-weight: 600;
        text-decoration: none;
        border-bottom: 2px solid transparent;
        padding-bottom: 2px;
        transition: all var(--transition-speed) ease;
    }
    
    .search-result-link:hover {
        color: var(--primary-dark);
        border-bottom-color: var(--accent-gold);
    }
    
    .dark-mode .search-result-link {
        color: var(--accent-gold);
    }
    
    .dark-mode .search-result-link:hover {
        color: var(--text-light);
    }
    
    /* Responsive styles */
    @media (max-width: 768px) {
        .section-title {
            font-size: 2rem;
        }
        
        .highlight {
            font-size: 1.2rem;
        }
        
        .category-card {
            padding: 16px;
        }
        
        .event-card {
            flex-direction: column;
        }
        
        .timeline::after {
            left: 31px;
        }
        
        .timeline-container {
            width: 100%;
            padding-left: 70px;
            padding-right: 25px;
        }
        
        .timeline-container::before {
            left: 60px;
            border: medium solid var(--background-cream);
            border-width: 10px 10px 10px 0;
            border-color: transparent var(--background-cream) transparent transparent;
        }
        
        .timeline-left::after, .timeline-right::after {
            left: 15px;
        }
        
        .timeline-right {
            left: 0%;
        }
    }
    
    /* Theme toggle button */
    .theme-toggle {
        position: fixed;
        bottom: 20px;
        right: 20px;
        width: 50px;
        height: 50px;
        border-radius: 50%;
        background-color: var(--primary-medium);
        color: var(--text-light);
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        box-shadow: var(--shadow-md);
        z-index: 1000;
        transition: all var(--transition-speed) ease;
    }
    
    .theme-toggle:hover {
        transform: scale(1.1);
        background-color: var(--primary-dark);
    }
    
    /* Animation classes */
    .fade-in {
        animation: fadeIn 0.5s ease-in-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    .slide-in {
        animation: slideIn 0.5s ease-in-out;
    }
    
    @keyframes slideIn {
        from { transform: translateY(20px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    
    /* Category icon styling */
    .category-icon {
        font-size: 2rem;
        color: var(--primary-medium);
        margin-bottom: 0.5rem;
    }
    
    .dark-mode .category-icon {
        color: var(--accent-gold);
    }
    
    /* Badge for Indian events */
    .indian-badge {
        display: inline-block;
        background-color: rgba(255, 153, 51, 0.2);
        border-left: 3px solid #FF9933;
        padding: 5px 10px;
        border-radius: 4px;
        margin-top: 10px;
        font-weight: bold;
        color: #FF9933;
    }
    
    .dark-mode .indian-badge {
        background-color: rgba(255, 153, 51, 0.1);
    }
    </style>
    """, unsafe_allow_html=True)


# Add FontAwesome for icons
def add_fontawesome():
    st.markdown("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    """, unsafe_allow_html=True)

def create_header():
    """Create an improved header with better search functionality"""
    # Apply dark mode class if needed
    if st.session_state.get('theme', 'light') == "dark":
        st.markdown("""
        <script>
            document.body.classList.add('dark-mode');
        </script>
        """, unsafe_allow_html=True)
    
    # Header with logo and search
    st.markdown("""
    <div class="header">
        <div class="logo" style="margin-left:30px;">
            <h1>HISTOFACTS</h1>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Header with logo and search
    st.markdown("""
    <div class="header">
        <div class="logo" style="margin-left:30px;">
            <h1>HISTOFACTS</h1>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Date picker and search bar
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        current_date = st.session_state.get('current_date', datetime.now())
        selected_date = st.date_input("Select Date", current_date)
        if current_date != selected_date:
            st.session_state.current_date = selected_date
            # Fetch timeline events for the selected date
            st.session_state.timeline_events = fetch_timeline_events(selected_date)
            st.rerun()
    
    with col2:
        search_query = st.text_input("search", placeholder="Search historical facts...", key="search_input")
        if search_query and search_query != st.session_state.get('search_query', ""):
            st.session_state.search_query = search_query
            st.session_state.search_results = search_historical_events(search_query)
            st.session_state.page = "search_results"
            st.rerun()
    


def create_fact_section(date):
    """Create an improved fact section with better visuals and animations"""
    # Fetch historical events for the selected date
    data = fetch_historical_events(date.month, date.day)
    
    if data and 'data' in data and 'Events' in data['data'] and len(data['data']['Events']) > 0:
        # Get multiple featured events
        featured_events = data['data']['Events'][:3]  # Get top 3 events
        
        st.markdown(f"""
        <div class="fact-section slide-in">
            <div class="fact-content">
                <h2 class="section-title">HISTOFACTS</h2>
        """, unsafe_allow_html=True)
        
        for i, event in enumerate(featured_events):
            category = event.get('category', categorize_event(event['text']))
            
            st.markdown(f"""
            <div class="fact-highlight">
                <div style="flex: 4;">
                    <p class="highlight">Today in History: {date.strftime("%B %d")}, {event['year']} - {event['text']}</p>
                    <div style="margin-top: 10px; font-size: 0.9rem; color: rgba(255,255,255,0.7);">
                        <i class="fas fa-tag" style="margin-right: 5px;"></i> {category}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown(f"""
                <a href="#" class="info-link" style="text-decoration:none; color:#2c3e50;">Explore Historical Significance</a>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="fact-section slide-in">
            <div class="fact-content">
                <h2 class="section-title">HISTOFACTS</h2>
                <div class="fact-highlight">
                    <p class="highlight">Today in History: {date.strftime("%B %d")}</p>
                </div>
                <a href="#" class="info-link" style="text-decoration:none; color:#2c3e50;">Explore Historical Significance</a>
            </div>
        </div>
        """, unsafe_allow_html=True)

def create_daily_events_section(date):
    """Create an improved section displaying daily historical events by category"""
    # Fetch historical events for the selected date
    data = fetch_historical_events(date.month, date.day)
    
    if not data or 'data' not in data or 'Events' not in data['data'] or len(data['data']['Events']) == 0:
        st.warning(f"No historical events found for {date.strftime('%B %d')}.")
        return
    
    st.markdown("""
    <div class="section-header">
        <i class="fas fa-clock"></i>
        <h3>Historical Events</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Group events by category
    events_by_category = {}
    for i, event in enumerate(data['data']['Events']):
        category = event.get('category', categorize_event(event['text']))
        if category not in events_by_category:
            events_by_category[category] = []
        
        # Add category to event if not already present
        if 'category' not in event:
            event['category'] = category
        
        events_by_category[category].append((event, f"{event['year']}_{i}"))
    
    # Create tabs for each category
    if events_by_category:
        # Sort categories to prioritize Indian History if preference is set
        indian_history_preference = st.session_state.get('indian_history_preference', True)
        sorted_categories = sorted(events_by_category.keys(), 
                                  key=lambda x: (0 if x == "Indian History" and indian_history_preference else 1, x))
        
        tabs = st.tabs(sorted_categories)
        
        # Determine how many events to show per category
        max_events_per_category = st.session_state.get('events_count', 10)
        
        for i, category in enumerate(sorted_categories):
            events = events_by_category[category]
            with tabs[i]:
                with st.container():
                    st.markdown('<div class="scrollable-events">', unsafe_allow_html=True)
                    
                    # Sort events by year (newest first)
                    events.sort(key=lambda x: int(x[0]['year']) if x[0]['year'].isdigit() else 0, reverse=True)
                    
                    # Check if category is expanded
                    categories_expanded = st.session_state.get('categories_expanded', {})
                    if category not in categories_expanded:
                        categories_expanded[category] = False
                    
                    # Display events
                    for event, event_id in events[:max_events_per_category]:
                        display_event_card(event, event_id, is_indian=is_indian_event(event['text']))
                    
                    # Show "Load More" button if there are more events
                    if len(events) > max_events_per_category and not categories_expanded[category]:
                        if st.button(f"Load More {category} Events", key=f"load_more_{category}"):
                            categories_expanded[category] = True
                            st.session_state.categories_expanded = categories_expanded
                            st.rerun()
                    
                    # Show additional events if expanded
                    if categories_expanded.get(category, False):
                        for event, event_id in events[max_events_per_category:]:
                            display_event_card(event, event_id, is_indian=is_indian_event(event['text']))
                        
                        if st.button(f"Show Less", key=f"show_less_{category}"):
                            categories_expanded[category] = False
                            st.session_state.categories_expanded = categories_expanded
                            st.rerun()
                    
                    st.markdown('</div>', unsafe_allow_html=True)

def fetch_timeline_events(date):
    """Placeholder for timeline events function"""
    # This would be implemented in utils/historical_api.py
    return []

def search_historical_events(query):
    """Placeholder for search function"""
    # This would be implemented in utils/historical_api.py
    return []

def show_favorites():
    """Show user's favorite historical events"""
    add_custom_css()
    add_fontawesome()
    create_header()
    
    st.markdown("<h2>Your Favorite Historical Events</h2>", unsafe_allow_html=True)
    
    if not st.session_state.favorites:
        st.info("You haven't added any favorites yet. Explore historical events to find interesting facts!")
        return
    
    # Get the current date to fetch events
    date = st.session_state.get('current_date', datetime.now())
    
    # Fetch historical events
    data = fetch_historical_events(date.month, date.day)
    
    if not data or 'data' not in data or 'Events' not in data['data']:
        st.warning("Could not load historical events. Please try again later.")
        return
    
    # Display favorite events
    for i, event in enumerate(data['data']['Events']):
        event_id = f"{event['year']}_{i}"
        if event_id in st.session_state.favorites:
            # Add category to event if not already present
            if 'category' not in event:
                event['category'] = categorize_event(event['text'])
            display_event_card(event, event_id, is_indian=is_indian_event(event['text']))
    
    if st.button("Clear All Favorites"):
        st.session_state.favorites = []
        st.rerun()

def show_bookmarks():
    """Show user's bookmarked historical events"""
    add_custom_css()
    add_fontawesome()
    create_header()
    
    st.markdown("<h2>Your Bookmarked Historical Events</h2>", unsafe_allow_html=True)
    
    if not st.session_state.bookmarks:
        st.info("You haven't bookmarked any events yet. Explore historical events to bookmark interesting facts!")
        return
    
    # Get the current date to fetch events
    date = st.session_state.get('current_date', datetime.now())
    
    # Fetch historical events
    data = fetch_historical_events(date.month, date.day)
    
    if not data or 'data' not in data or 'Events' not in data['data']:
        st.warning("Could not load historical events. Please try again later.")
        return
    
    # Display bookmarked events
    for i, event in enumerate(data['data']['Events']):
        event_id = f"{event['year']}_{i}"
        if event_id in st.session_state.bookmarks:
            # Add category to event if not already present
            if 'category' not in event:
                event['category'] = categorize_event(event['text'])
            display_event_card(event, event_id, is_indian=is_indian_event(event['text']))
    
    if st.button("Clear All Bookmarks"):
        st.session_state.bookmarks = []
        st.rerun()


def render_settings_page():
    """Render improved settings page"""
    st.markdown("<h2>Settings</h2>", unsafe_allow_html=True)
    
    st.write("Customize your HistoFacts experience")
    
    # Theme setting
    theme = st.selectbox("Theme", ["Light", "Dark"], 
                         index=0 if st.session_state.theme == "light" else 1)
    
    # Number of events to show
    events_count = st.slider("Number of events to show per category", 
                             min_value=5, max_value=20, value=st.session_state.events_count)
    
    # Indian history preference
    indian_history_preference = st.checkbox("Prioritize Indian historical events", 
                                           value=st.session_state.indian_history_preference)
    
    # Save settings button
    if st.button("Save Settings"):
        st.session_state.theme = "light" if theme == "Light" else "dark"
        st.session_state.events_count = events_count
        st.session_state.indian_history_preference = indian_history_preference
        save_data()
        st.success("Settings saved successfully!")
        time.sleep(1)
        st.rerun()

def render_category_page():
    """Render a page for a specific category"""
    category = st.session_state.current_category
    
    st.markdown(f"<h2>{category}</h2>", unsafe_allow_html=True)
    
    # Get category icon
    category_icons = {
        "Politics & Government": "fas fa-landmark",
        "War & Conflict": "fas fa-fighter-jet",
        "Science & Technology": "fas fa-microscope",
        "Arts & Culture": "fas fa-palette",
        "Sports & Recreation": "fas fa-trophy",
        "Religion & Spirituality": "fas fa-pray",
        "Exploration & Geography": "fas fa-globe-americas",
        "Disasters & Accidents": "fas fa-exclamation-triangle",
        "Social Movements": "fas fa-users",
        "Medicine & Health": "fas fa-heartbeat",
        "Indian History": "fas fa-om",
        "Other Historical Events": "fas fa-history"
    }
    
    icon = category_icons.get(category, "fas fa-history")
    
    # Get category description
    category_descriptions = {
        "Politics & Government": "Explore the evolution of political systems, governance, and leadership throughout history.",
        "War & Conflict": "Discover the major conflicts and military engagements that shaped nations and changed the course of history.",
        "Science & Technology": "Learn about groundbreaking discoveries, inventions, and technological advancements that transformed human civilization.",
        "Arts & Culture": "Immerse yourself in the rich tapestry of human creativity through art, music, literature, and cultural movements.",
        "Sports & Recreation": "Relive the greatest moments in sports history, from ancient Olympic games to modern athletic achievements.",
        "Religion & Spirituality": "Understand the development of religious traditions, spiritual practices, and their influence on societies.",
        "Exploration & Geography": "Follow the journeys of explorers who mapped our world and expanded the boundaries of human knowledge.",
        "Disasters & Accidents": "Examine catastrophic events that tested human resilience and often led to important safety reforms.",
        "Social Movements": "Study the collective actions that fought for rights, equality, and social change throughout history.",
        "Medicine & Health": "Trace the evolution of medical knowledge, treatments, and public health initiatives that improved human wellbeing.",
        "Indian History": "Discover the rich tapestry of Indian civilization, from ancient kingdoms to modern independence, and its profound impact on world history, culture, and thought."
    }
    
    description = category_descriptions.get(category, "Explore fascinating events from this historical category.")
    
    # Display category header
    st.markdown(f"""
    <div style="display: flex; align-items: center; margin-bottom: 20px;">
        <div style="font-size: 3rem; color: var(--primary-medium); margin-right: 20px;">
            <i class="{icon}"></i>
        </div>
        <div>
            <p>{description}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Get the current date to fetch events
    date = st.session_state.current_date if 'current_date' in st.session_state else datetime.now()
    
    # Fetch historical events specifically for this category
    data = fetch_historical_events(date.month, date.day, category)
    
    if not data or 'data' not in data or 'Events' not in data['data'] or len(data['data']['Events']) == 0:
        st.info(f"No {category} events found for {date.strftime('%B %d')}. Try selecting a different date.")
        return
    
    # Display events
    st.markdown('<div class="scrollable-events">', unsafe_allow_html=True)
    for i, event in enumerate(data['data']['Events']):
        event_id = f"{event['year']}_{i}"
        # Add category to event
        event['category'] = category
        display_event_card(event, event_id, is_indian=is_indian_event(event['text']))
    st.markdown('</div>', unsafe_allow_html=True)

def render_help_page():
    """Render improved help page"""
    st.markdown("<h2>Help</h2>", unsafe_allow_html=True)
    
    st.markdown("""
    ### How to use HistoFacts
    
    - **Date Selection**: Use the date picker at the top to view historical events for a specific date.
    - **Search**: Use the search bar to find specific historical events or topics.
    - **Timeline**: Explore historical events in chronological order in the timeline section.
    - **Categories**: Events are organized by categories in tabs for easy browsing.
    - **Favorites**: Click the "⭐ Favorite" button on any event to add it to your favorites.
    - **Bookmarks**: Click the "🔖 Bookmark" button on any event to bookmark it for later.
    - **Theme**: Toggle between light and dark mode in the settings or using the theme toggle button.
    
    ### FAQ
    
    **Q: How do I save my favorites and bookmarks?**  
    A: Your favorites and bookmarks are automatically saved when you add or remove them.
    
    **Q: Can I search for specific historical events?**  
    A: Yes, use the search bar at the top to find specific events or topics.
    
    **Q: How do I view events from a different date?**  
    A: Use the date picker at the top of the page to select any date.
    
    **Q: How do I change the theme?**  
    A: You can change the theme in the Settings page or use the theme toggle button in the sidebar.
    
    **Q: How do I prioritize Indian historical events?**  
    A: Go to Settings and check the "Prioritize Indian historical events" option.
    
    **Q: How do I contact support?**  
    A: Please email us at support@histofacts.com for any issues or suggestions.
    """)

def render_about_page():
    """Render improved about page"""
    st.markdown("<h2>About HistoFacts</h2>", unsafe_allow_html=True)
    
    st.markdown("""
    ### Our Mission
    
    HistoFacts aims to make learning about historical events engaging and accessible to everyone. 
    We believe that understanding our past helps us make better decisions for our future.
    
    ### Data Sources
    
    Our historical events data comes from various reputable sources, including:
    - History.com
    - Wikipedia
    - Today in History
    - The Library of Congress
    - National Archives
    - Britannica Encyclopedia
    - World History Encyclopedia
    
    ### Features
    
    - **Daily Historical Facts**: Discover what happened on this day in history.
    - **Timeline View**: Visualize historical events in chronological order.
    - **Categorized Events**: Browse events by category such as Politics, Science, Arts, and more.
    - **Search Functionality**: Find specific historical events or topics.
    - **Favorites & Bookmarks**: Save events for later reference.
    - **Responsive Design**: Enjoy a seamless experience on any device.
    - **Dark Mode**: Reduce eye strain with our dark theme option.
    
    ### Development Team
    
    This application was developed by a team of history enthusiasts and software developers 
    who are passionate about bringing history to life through technology.
    
    ### Version
    
    Current Version: 4.0.0
    Last Updated: March 2023
    """)

def main():
    """Main dashboard function"""
    # Add custom CSS and FontAwesome
    add_custom_css()
    add_fontawesome()
    
    # Create header
    create_header()
    
    # Get the current date from session state
    date = st.session_state.get('current_date', datetime.now())
    
    # Create fact section
    create_fact_section(date)
    
    # Create daily events section
    create_daily_events_section(date)
    
    # Add theme toggle button
    st.markdown("""
    <div class="theme-toggle" onclick="document.body.classList.toggle('dark-mode');">
        <i class="fas fa-moon"></i>
    </div>
    """, unsafe_allow_html=True)

# Initialize necessary session state variables
def init_dashboard_state():
    """Initialize dashboard-specific session state variables"""
    if 'current_date' not in st.session_state:
        st.session_state.current_date = datetime.now()
    if 'theme' not in st.session_state:
        st.session_state.theme = "light"
    if 'events_count' not in st.session_state:
        st.session_state.events_count = 10
    if 'indian_history_preference' not in st.session_state:
        st.session_state.indian_history_preference = True
    if 'categories_expanded' not in st.session_state:
        st.session_state.categories_expanded = {}