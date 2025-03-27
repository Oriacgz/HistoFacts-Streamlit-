import streamlit as st
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the current directory to the path so we can import our modules
sys.path.append(os.path.dirname(__file__))

# Import our modules
from pages.login import create_user, login_user, dashboard, check_login
from pages.quiz import show_welcome_page as show_quiz_welcome, show_quiz_page, show_results_page
from pages.dashboard import fetch_indian_historical_facts, get_todays_fact, get_random_fact

# Set page configuration
st.set_page_config(
    page_title="HISTOFACT",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = "Sign-Up"
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_email' not in st.session_state:
    st.session_state.user_email = None
if 'quiz_state' not in st.session_state:
    st.session_state.quiz_state = "welcome"

# Apply background image
page_bg_img = '''
<style>
.stApp {
    background-image: url("https://unblast.com/wp-content/uploads/2021/01/Space-Background-Images-1024x682.jpg");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}
</style>
'''
st.markdown(page_bg_img, unsafe_allow_html=True)

# Sidebar navigation
def sidebar():
    with st.sidebar:
        st.title("🏛️ HISTOFACT")
        st.markdown("### Explore History")
        
        # Navigation buttons
        if st.session_state.logged_in:
            if st.button("🏠 Home"):
                st.session_state.page = "Home"
            if st.button("📚 Quiz"):
                st.session_state.page = "Quiz"
                st.session_state.quiz_state = "welcome"
            if st.button("🔍 Dashboard"):
                st.session_state.page = "Dashboard"
            if st.button("🚪 Logout"):
                st.session_state.logged_in = False
                st.session_state.user_email = None
                st.session_state.page = "Sign-Up"
        else:
            st.info("Please login to access all features")

# Main application
def main():
    sidebar()
    
    # Routing based on session state
    if not st.session_state.logged_in:
        if st.session_state.page == "Sign-Up":
            create_user()
        elif st.session_state.page == "Sign-In":
            login_user()
    else:
        if st.session_state.page == "Home":
            dashboard()
        elif st.session_state.page == "Quiz":
            if st.session_state.quiz_state == "welcome":
                show_quiz_welcome()
            elif st.session_state.quiz_state == "quiz":
                show_quiz_page()
            elif st.session_state.quiz_state == "results":
                show_results_page()
        elif st.session_state.page == "Dashboard":
            # We'll import the dashboard functions directly in the main file
            # since the dashboard module has its own page structure
            st.session_state.page = 'home'  # Set to home page of dashboard
            # Import and run the dashboard module
            import pages.dashboard as dashboard_module
            dashboard_module.main()

if __name__ == "__main__":
    main()