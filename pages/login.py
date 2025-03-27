import streamlit as st 
import mysql.connector
import pymysql
import bcrypt 
import re

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

def validate_email(email):
    # Regular expression for email validation
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(pattern, email):
        return True
    return False

def validate_password(password):
    # Password must be at least 8 characters long
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    # Password must contain at least one uppercase letter
    if not any(char.isupper() for char in password):
        return False, "Password must contain at least one uppercase letter"
    
    # Password must contain at least one lowercase letter
    if not any(char.islower() for char in password):
        return False, "Password must contain at least one lowercase letter"
    
    # Password must contain at least one digit
    if not any(char.isdigit() for char in password):
        return False, "Password must contain at least one digit"
    
    # Password must contain at least one special character
    special_chars = "!@#$%^&*()-_=+[]{}|;:'\",.<>/?"
    if not any(char in special_chars for char in password):
        return False, "Password must contain at least one special character"
    
    return True, "Password is valid"
    
def insert_user(username, email, password):
    conn = create_connection()
    if conn is None:
        st.error("Database connection failed!")
        return False
    
    cursor = conn.cursor()
    hashed_pw = hash_password(password)
    
    try:
        cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", 
                      (username, email, hashed_pw))
        conn.commit()
        st.success("Account created successfully")
        cursor.close()
        conn.close()
        return True
    except pymysql.IntegrityError:
        st.error("❌ Email already exists! Choose a different Email")
        cursor.close()
        conn.close()
        return False

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
                confirm_password = st.text_input("Confirm Password", type="password")
                agree = st.checkbox("I agree to the Terms and Conditions")
                
                c1, c2, c3 = st.columns([6, 3, 6])
                with c2:
                    submit = st.form_submit_button("Submit")

                if submit:
                    if name and email and password and confirm_password and agree:
                        # Validate email
                        if not validate_email(email):
                            st.error("Please enter a valid email address")
                        # Validate password
                        elif password != confirm_password:
                            st.error("Passwords do not match")
                        else:
                            is_valid, message = validate_password(password)
                            if not is_valid:
                                st.error(message)
                            else:
                                # Insert user into database
                                if insert_user(name, email, password):
                                    # Auto-login after successful registration
                                    if check_login(email, password):
                                        st.session_state.logged_in = True
                                        st.session_state.user_email = email
                                        st.session_state.page = "Home"
                                        st.rerun()
                    elif not name:
                        st.error("Please enter your name")
                    elif not email:
                        st.error("Please enter your email")
                    elif not password:
                        st.error("Please enter a password")
                    elif not confirm_password:
                        st.error("Please confirm your password")
                    elif not agree:
                        st.error("You must agree to the Terms and Conditions before registering")
                    else:
                        st.error("Please fill in all required fields")

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
                    submit1 = st.form_submit_button("Submit")

                if submit1:
                    if email and password:
                        if check_login(email, password):
                            st.success(f"Welcome TO HISTOFACTS!!!")
                            st.session_state.logged_in = True
                            st.session_state.user_email = email
                            st.session_state.page = "dashboard"
                            st.rerun()
                        else:
                            st.error("❌ Invalid email and password")
                    elif not email:
                        st.error("Please Enter your Email ID")
                    elif not password:
                        st.error("Please Enter your Password")    
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