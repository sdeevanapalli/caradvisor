"""
Car Advisor - AI-Powered Car Recommendations
Main Application
"""
import streamlit as st
import os
from auth import check_password, show_logout_button, init_session_state
from streamlit_option_menu import option_menu
from questionnaire import display_questionnaire
from recommendations import display_recommendations
from comparison import display_comparison
from chat import display_chat_interface
from reviews import display_reviews
from export_features import display_export_features

# Page configuration - must be first Streamlit command
st.set_page_config(
    page_title="Car Advisor",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'About': "AI-powered car recommendations and consultation."
    }
)

# Clean CSS styling
st.markdown("""
<style>
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    
    .car-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #e9ecef;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Main application function"""
    
    # Check authentication
    if not check_password():
        return
    
    # Initialize session state
    init_session_state()
    
    # Simple header
    st.title("Car Advisor")
    
    # Main content in chronological order
    tab1, tab2, tab3, tab4 = st.tabs(["Chat", "Questionnaire", "Recommendations", "Compare"])
    
    with tab1:
        display_chat_interface()
    
    with tab2:
        display_questionnaire()
    
    with tab3:
        display_recommendations()
    
    with tab4:
        display_comparison()
    
    # Show logout button in sidebar
    with st.sidebar:
        show_logout_button()

# Page display functions removed - using tabs instead

if __name__ == "__main__":
    main()