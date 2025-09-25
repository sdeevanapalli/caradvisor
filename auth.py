"""
Authentication utilities for Car Advisor App
"""
import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_password() -> bool:
    """
    Returns True if the user had the correct password.
    """
    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == os.getenv("LOGIN_PASSWORD", "senior_car_guide_2024"):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.markdown("## 🔐 Car Advisor Login")
        st.markdown("Welcome to your personal AI car consultant!")
        
        # Senior-friendly styling
        st.markdown("""
        <style>
        .login-container {
            background-color: #f8f9fa;
            padding: 2rem;
            border-radius: 10px;
            border: 2px solid #e9ecef;
            margin: 1rem 0;
        }
        .stTextInput > div > div > input {
            font-size: 18px !important;
            padding: 12px !important;
        }
        .stButton > button {
            background-color: #007bff;
            color: white;
            font-size: 18px;
            font-weight: bold;
            padding: 12px 24px;
            border-radius: 8px;
            border: none;
            width: 100%;
        }
        .stButton > button:hover {
            background-color: #0056b3;
        }
        </style>
        """, unsafe_allow_html=True)
        
        with st.container():
            st.markdown('<div class="login-container">', unsafe_allow_html=True)
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.text_input("Enter Password", 
                             type="password", 
                             on_change=password_entered, 
                             key="password",
                             help="Please enter your access password")
                
                st.info("💡 **For Senior Users**: This is a secure area. Enter your password to access personalized car recommendations.")
            st.markdown('</div>', unsafe_allow_html=True)
        
        return False
        
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.markdown("## 🔐 Car Advisor Login")
        
        st.markdown("""
        <style>
        .login-container {
            background-color: #f8f9fa;
            padding: 2rem;
            border-radius: 10px;
            border: 2px solid #e9ecef;
            margin: 1rem 0;
        }
        .stTextInput > div > div > input {
            font-size: 18px !important;
            padding: 12px !important;
        }
        .stButton > button {
            background-color: #007bff;
            color: white;
            font-size: 18px;
            font-weight: bold;
            padding: 12px 24px;
            border-radius: 8px;
            border: none;
            width: 100%;
        }
        </style>
        """, unsafe_allow_html=True)
        
        with st.container():
            st.markdown('<div class="login-container">', unsafe_allow_html=True)
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.error("❌ **Access Denied**: Incorrect password. Please try again.")
                st.text_input("Enter Password", 
                             type="password", 
                             on_change=password_entered, 
                             key="password",
                             help="Please enter your access password")
                
                st.warning("🔒 **Security Notice**: Please make sure you have the correct password to access this application.")
            st.markdown('</div>', unsafe_allow_html=True)
        
        return False
    else:
        # Password correct.
        return True

def logout():
    """
    Logout function to clear session state
    """
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

def show_logout_button():
    """
    Display logout button in sidebar
    """
    with st.sidebar:
        st.markdown("---")
        if st.button("🚪 Logout", key="logout_btn", help="Click to log out and return to login page"):
            logout()

def init_session_state():
    """
    Initialize session state variables
    """
    if 'user_preferences' not in st.session_state:
        st.session_state.user_preferences = {}
    
    if 'questionnaire_step' not in st.session_state:
        st.session_state.questionnaire_step = 0
    
    if 'recommendations' not in st.session_state:
        st.session_state.recommendations = []
    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    if 'comparison_cars' not in st.session_state:
        st.session_state.comparison_cars = []
    
    if 'reviews' not in st.session_state:
        st.session_state.reviews = []