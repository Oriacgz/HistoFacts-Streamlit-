import streamlit as st 
import mysql.connector
import pymysql
import bcrypt 

def create_connection():
    try:
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='@nirmala2005',
            database='mini'
        )
        print("Connection established")
        return conn  # Return the connection
    except pymysql.MySQLError as e:
        print(f"Error connecting to MySQL: {e}")
        return None
    
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def check_password(password, hashed_password):
    return bcrypt.checkpw(password.encode(), hashed_password.encode())

def check_login(email, password):
    conn = create_connection()
    if conn is None:
        st.error("Database connection failed!")
        return False
        
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE email = %s", (email,))
    result = cursor.fetchone()
    conn.close()

    if result and check_password(password, result[0]):
        return True
    return False
    
def insert_user(username, email, password):
    conn = create_connection()
    if conn is None:
        st.error("Database connection failed!")
        return
    
    cursor = conn.cursor()
    hashed_pw = hash_password(password)
    
    try:
        cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", 
                      (username, email, hashed_pw))
        conn.commit()
        st.success("Account created successfully")
    except pymysql.IntegrityError:
        st.error("❌ Email already exists! Choose a different Email")

    cursor.close()
    conn.close()

def dashboard():
    transparent_button = """
    <style>
    div.stButton > button {
        background-color: rgba(0,0,0,0); /* Transparent */
        color: white;
        border: 2px solid white;
        padding: 10px 20px;
        font-size: 16px;
        cursor: pointer;
    }
    div.stButton > button:hover {
        background-color: rgba(255,255,255,0.2); /* Slight transparency on hover */
    }
    </style>
    """

    st.markdown(transparent_button, unsafe_allow_html=True)

    col_nav1, col_nav2, col_nav3, col_nav4 = st.columns([8, 1, 1, 1])

    with col_nav2:
        st.button("🏠 Home")
    with col_nav3:
        st.button("ℹ️ About")
    with col_nav4:
        st.button("📞 Help")

    st.header("Welcome to HISTOFACT")
    st.subheader("Explore the rich tapestry of history")
    
    # Display options to navigate to other pages
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Take a History Quiz", key="goto_quiz"):
            st.session_state.page = "Quiz"
            st.session_state.quiz_state = "welcome"
            st.rerun()
    with col2:
        if st.button("Explore Historical Facts", key="goto_dashboard"):
            st.session_state.page = "Dashboard"
            st.rerun()

def create_user():
    st.markdown("# HISTOFACTS")
    st.write("---")
    # Layout for login/signup
    c1, c2, c3 = st.columns([2, 3, 2])
    with c2:
        with st.container():
            st.markdown("### *Sign Up*", unsafe_allow_html=True)
    
            with st.form(key="sign-up-form"):
                name = st.text_input("Full Name")
                email = st.text_input("Email")
                password = st.text_input("Password", type="password")
                agree = st.checkbox("I agree to the Terms and Conditions")
                
                c1, c2, c3 = st.columns([6, 3, 6])
                with c2:
                    submit = st.form_submit_button("Submit")

                if submit:
                    if name and email and password and agree:
                        insert_user(name, email, password)
                        # Auto-login after successful registration
                        if check_login(email, password):
                            st.session_state.logged_in = True
                            st.session_state.user_email = email
                            st.session_state.page = "Home"
                            st.rerun()
                    elif email and password and agree:
                        st.error("Please Enter your name")
                    elif name and password and agree:
                        st.error("Please Enter your Email ID")
                    elif name and email and agree:
                        st.error("Please Enter Password")
                    elif name and email and password:
                        st.error("You must agree to the Terms and Conditions before registering.")
                    else:
                        st.error("Please enter your details")

    c1, c2, c3 = st.columns([14, 1, 14])
    with c1:
        st.write("--------")
    with c3:
        st.write("------")
    with c2:
        st.subheader("OR")

    c1, c2, c3 = st.columns([6, 2, 6])
    with c2:
        st.write("Already have an account?")

    c1, c2, c3 = st.columns([6, 1, 6])
    with c2:
        login = st.button("Login", key="go_to_login")

    if login:
        st.session_state.page = "Sign-In"
        st.rerun()

def login_user():
    st.markdown("# HISTOFACTS")
    st.write("---")
    # Layout for login/signup
    c1, c2, c3 = st.columns([2, 3, 2])
    with c2:
        with st.container():
            st.markdown("### *Sign In*", unsafe_allow_html=True)
    
            with st.form(key="sign-in-form"):
                email = st.text_input("Email")
                password = st.text_input("Password", type="password")
    
                c1, c2, c3 = st.columns([6, 3, 6])
                with c2:
                    submit = st.form_submit_button("Submit")

                if submit:
                    if email and password:
                        if check_login(email, password):
                            st.success(f"Welcome TO HISTOFACTS!!!")
                            st.session_state.logged_in = True
                            st.session_state.user_email = email
                            st.session_state.page = "Home"
                            st.rerun()
                        else:
                            st.error("❌ Invalid email and password")
                    elif email:
                        st.error("Please Enter your Password")
                    elif password:
                        st.error("Please Enter your Email ID")    
                    else:
                        st.error("Please enter your details")

    c1, c2, c3 = st.columns([14, 1, 14])
    with c1:
        st.write("--------")
    with c3:
        st.write("------")
    with c2:
        st.subheader("OR")

    c1, c2, c3 = st.columns([6, 2, 6])
    with c2:
        st.write("Don't have an account?")

    c1, c2, c3 = st.columns([6, 1, 6])
    with c2:
        signup = st.button("Create Account", key="go_to_signup")

    if signup:
        st.session_state.page = "Sign-Up"
        st.rerun()