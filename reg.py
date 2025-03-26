# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 10:49:20 2025

@author: pande
"""

import streamlit as st
import sqlite3

# SQLite setup
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Create users table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
''')
conn.commit()
def switch_page(page_name):
    st.session_state.page = page_name
    st.rerun()

# Helper functions
def add_user_to_db(name, phone, email, password):
    try:
        cursor.execute('INSERT INTO users (name, phone, email, password) VALUES (?, ?, ?, ?)', (name, phone, email, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def check_user_in_db(email, password):
    cursor.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password))
    return cursor.fetchone()




# CSS Styles
styles = {
    "light": """
    <style>
        body {
            background-color: black; 
            color: black;
            font-family: Arial, sans-serif;
            font-size: 12px; 
        }
        .stApp {
            background-color: grey;
            padding: 30px;
            border-radius: 10px;
        }
        .form-btn {
            background-color: #007BFF; 
            color: #061f38; 
            padding: 10px;
            border: none;
        }
        input[type="text"], input[type="password"] {
            color: #061f38 !important;  
            background-color: #ffffff !important; 
            border: 1px solid #003366 !important; 
            padding: 8px;
            border-radius: 5px;
        }
        h1, h2, h3, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
            color: #061f38 !important; 
        }
    </style>
    """,
    "dark": """
    <style>
        body {
            background-color: #121212; 
            color: white;
            font-family: Arial, sans-serif;
        }
        .stApp {
            background-color: #333; 
            padding: 30px; 
            border-radius: 10px;
        }
        .form-btn {
            background-color: #BB86FC;
            color: white;
            padding: 10px;
            border: none;
        }
        h1, h2, h3, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
            color: #BB86FC !important;
        }
    </style>
    """,
    "modern": """
    <style>
        body {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #944ae8; 
            font-family: Arial, sans-serif;
        }
        .stApp {
            background-color: #944ae8; 
            padding: 30px;
            border-radius: 10px;
        }
        .form-btn {
            background-color: #ff4081; 
            color: white; 
            padding: 10px;
            border: none;
        }
        h1, h2, h3, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
            color: #ffcc00 !important; 
        }
    </style>
    """
} 

# Login Page
def login_page():
    st.markdown(styles[selected_style], unsafe_allow_html=True)
    st.title("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login", key='login_btn', help='Click to log in'):
        user = check_user_in_db(email, password)
        if user:
            st.success(f"Welcome back, {user[1]}!")
            import subprocess
            subprocess.run(['streamlit', 'run', 'p.py'])
        else:
            st.error("Invalid credentials")

# Register Page
def register_page():
    st.markdown(styles[selected_style], unsafe_allow_html=True)
    st.title("Register")
    name = st.text_input("Name")
    phone = st.text_input("Phone Number")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    
    if st.button("Register", key='register_btn', help='Click to register'):
        
        if not name or not phone or not email or not password or not confirm_password:
            st.error("All fields are required!")
        elif password != confirm_password:
            st.error("Passwords do not match")
        else:
            if add_user_to_db(name, phone, email, password):
                st.success("Account created! You can now login.")
                
            else:
                st.error("Email already exists. Please use a different email.")
   
# Page Navigation
def main():
    global selected_style
    selected_style = st.sidebar.selectbox("Select Style", ["light", "dark", "modern"])
    page = st.sidebar.selectbox("Select a page", ["Register", "Login"])
    
    if page == "Login":
        login_page()
    elif page == "Register":
        register_page()

if __name__ == "__main__":
    main()