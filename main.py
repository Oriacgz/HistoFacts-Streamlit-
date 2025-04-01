import streamlit as st
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the current directory to the path so we can import our modules
sys.path.append(os.path.dirname(__file__))

# Set page configuration
st.set_page_config(
    page_title="HISTOFACTS",
    page_icon="assets/icon.png",
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
if 'favorites' not in st.session_state:
    st.session_state.favorites = []
if 'bookmarks' not in st.session_state:
    st.session_state.bookmarks = []
if 'cached_events' not in st.session_state:
    st.session_state.cached_events = {}

# Import modules after initializing session state
from pages.login import create_user, login_user
from pages.quiz import show_welcome_page as show_quiz_welcome, show_quiz_page, show_results_page
import pages.dashboard as dashboard

# Apply background image only on login pages
def apply_background():
    page_bg_img = """
    <style>
    .stApp {
        background-image: url("https://unblast.com/wp-content/uploads/2021/01/Space-Background-Images-1024x682.jpg");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)

# Sidebar navigation
def sidebar():
    with st.sidebar:
        st.title("🏛️ HISTOFACTS")
        st.markdown("### Explore History")

        if st.session_state.logged_in:
            if st.button("🏠 Home", key="home_button"):
                st.session_state.page = "Dashboard"
                st.rerun()
            if st.button("📚 Quiz", key="quiz_button"):
                st.session_state.page = "Quiz"
                st.session_state.quiz_state = "welcome"
                st.rerun()
            if st.button("⭐ Favorites", key="favorites_button"):
                st.session_state.page = "Favorites"
                st.rerun()
            if st.button("🔖 Bookmarks", key="bookmarks_button"):
                st.session_state.page = "Bookmarks"
                st.rerun()
            if st.button("🚪 Logout", key="logout_button"):
                st.session_state.logged_in = False
                st.session_state.user_email = None
                st.session_state.page = "Sign-Up"
                st.rerun()

            st.markdown("---")
            st.info(f"Logged in as: {st.session_state.user_email}")
        else:
            st.info("Please login to access all features")

# Modified login function to redirect to Dashboard after login
def custom_login_user():
    login_successful = login_user()  # Call original login function
    if login_successful:
        st.session_state.logged_in = True
        st.session_state.page = "Dashboard"  # Redirect to Dashboard automatically
        st.rerun()  # Refresh the page immediately

# Main application
def main():
    sidebar()

    # Apply background image only on login pages
    if st.session_state.page in ["Sign-Up", "Sign-In"]:
        apply_background()

    # Routing logic
    if not st.session_state.logged_in:
        if st.session_state.page == "Sign-Up":
            create_user()
        elif st.session_state.page == "Sign-In":
            custom_login_user()  # Use modified login function
    else:
        if st.session_state.page == "Dashboard":
            dashboard.main()
        elif st.session_state.page == "Favorites":
            dashboard.show_favorites()
        elif st.session_state.page == "Bookmarks":
            dashboard.show_bookmarks()
        elif st.session_state.page == "Quiz":
            if st.session_state.quiz_state == "welcome":
                show_quiz_welcome()
            elif st.session_state.quiz_state == "quiz":
                show_quiz_page()
            elif st.session_state.quiz_state == "results":
                show_results_page()

if __name__ == "__main__":
    main()