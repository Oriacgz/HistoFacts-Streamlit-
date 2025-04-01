import pymysql
import bcrypt
import streamlit as st

def create_connection():
    """Create a connection to the MySQL database"""
    try:
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='@nirmala2005',
            database='mini'
        )
        print("Connection established")
        return conn
    except pymysql.MySQLError as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def hash_password(password):
    """Hash a password for storing in the database"""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def check_password(password, hashed_password):
    """Check if a password matches the hashed version"""
    return bcrypt.checkpw(password.encode(), hashed_password.encode())

def save_user_data(user_email, data_type, data):
    """Save user data (favorites, bookmarks, etc.) to the database"""
    conn = create_connection()
    if conn is None:
        st.error("Database connection failed!")
        return False
        
    cursor = conn.cursor()
    try:
        # Check if user already has data of this type
        cursor.execute("SELECT id FROM user_data WHERE email = %s AND data_type = %s", 
                      (user_email, data_type))
        result = cursor.fetchone()
        
        if result:
            # Update existing data
            cursor.execute("UPDATE user_data SET data = %s WHERE email = %s AND data_type = %s", 
                          (data, user_email, data_type))
        else:
            # Insert new data
            cursor.execute("INSERT INTO user_data (email, data_type, data) VALUES (%s, %s, %s)", 
                          (user_email, data_type, data))
        
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Error saving user data: {str(e)}")
        cursor.close()
        conn.close()
        return False

def load_user_data(user_email, data_type):
    """Load user data (favorites, bookmarks, etc.) from the database"""
    conn = create_connection()
    if conn is None:
        st.error("Database connection failed!")
        return None
        
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT data FROM user_data WHERE email = %s AND data_type = %s", 
                      (user_email, data_type))
        result = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if result:
            return result[0]
        else:
            return None
    except Exception as e:
        st.error(f"Error loading user data: {str(e)}")
        cursor.close()
        conn.close()
        return None