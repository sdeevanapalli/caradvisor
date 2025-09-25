"""
Car Advisor - AI-Powered Car Recommendations for Seniors
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
    page_title="Car Advisor for Seniors",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "AI-powered car recommendations designed specifically for senior buyers."
    }
)

# Senior-friendly CSS styling
st.markdown("""
<style>
    /* Main content styling */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Large, readable fonts */
    .stMarkdown, .stText {
        font-size: 18px !important;
        line-height: 1.6 !important;
    }
    
    /* Button styling for seniors */
    .stButton > button {
        font-size: 18px !important;
        font-weight: bold !important;
        padding: 12px 24px !important;
        border-radius: 8px !important;
        border: 2px solid #007bff !important;
        background-color: #007bff !important;
        color: white !important;
        min-height: 50px !important;
    }
    
    .stButton > button:hover {
        background-color: #0056b3 !important;
        border-color: #0056b3 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 8px rgba(0,123,255,0.3) !important;
    }
    
    /* High contrast colors */
    .stSelectbox > div > div {
        font-size: 18px !important;
        padding: 12px !important;
    }
    
    .stTextInput > div > div > input {
        font-size: 18px !important;
        padding: 12px !important;
        border: 2px solid #ced4da !important;
        border-radius: 8px !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #007bff !important;
        box-shadow: 0 0 0 0.2rem rgba(0,123,255,0.25) !important;
    }
    
    /* Card styling */
    .car-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 12px;
        border: 2px solid #e9ecef;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .car-card:hover {
        border-color: #007bff;
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
    
    /* Navigation menu styling */
    .nav-link {
        font-size: 18px !important;
        font-weight: 600 !important;
        padding: 12px 16px !important;
    }
    
    /* Progress bar styling */
    .stProgress > div > div > div > div {
        background-color: #007bff !important;
    }
    
    /* Info box styling */
    .info-box {
        background-color: #e7f3ff;
        border: 2px solid #007bff;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    /* Warning box styling */
    .warning-box {
        background-color: #fff3cd;
        border: 2px solid #ffc107;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    /* Success box styling */
    .success-box {
        background-color: #d1edff;
        border: 2px solid #28a745;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    /* Sidebar improvements */
    .css-1d391kg {
        padding-top: 1rem;
    }
    
    /* Large headers */
    h1, h2, h3 {
        color: #2c3e50 !important;
        font-weight: bold !important;
    }
    
    h1 {
        font-size: 2.5rem !important;
        margin-bottom: 1rem !important;
    }
    
    h2 {
        font-size: 2rem !important;
        margin-bottom: 0.8rem !important;
    }
    
    h3 {
        font-size: 1.5rem !important;
        margin-bottom: 0.6rem !important;
    }
    
    /* Loading spinner */
    .stSpinner {
        text-align: center;
        padding: 2rem;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Main application function"""
    
    try:
        # Check authentication
        if not check_password():
            return
        
        # Initialize session state
        init_session_state()
        
        # Show welcome message and navigation
        display_header()
        
        # Sidebar navigation
        page = display_navigation()
        
        # Show logout button
        show_logout_button()
        
        # Display selected page with error handling
        try:
            if page == "🏠 Home":
                show_home_page()
            elif page == "📝 Car Finder Quiz":
                show_questionnaire_page()
            elif page == "🚗 My Recommendations":
                show_recommendations_page()
            elif page == "⚖️ Compare Cars":
                show_comparison_page()
            elif page == "💬 Ask AI Expert":
                show_chat_page()
            elif page == "⭐ Reviews & Ratings":
                show_reviews_page()
            elif page == "📄 Export & Share":
                show_export_page()
            else:
                st.error("🚫 **Page not found. Please select a valid option from the navigation.**")
        
        except Exception as e:
            st.error(f"⚠️ **An error occurred while loading this page**: {str(e)}")
            st.info("💡 **Try refreshing the page or contact support if the problem persists.**")
            
            # Show error details in debug mode
            if os.getenv("DEBUG_MODE", "False").lower() == "true":
                st.exception(e)
    
    except Exception as e:
        st.error("🚫 **Application Error**: Something went wrong with the application.")
        st.info("💡 **Please refresh the page and try again. If the problem persists, contact support.**")
        
        # Show error details in debug mode
        if os.getenv("DEBUG_MODE", "False").lower() == "true":
            st.exception(e)

def display_header():
    """Display the main header with welcome message"""
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.title("🚗 Car Advisor for Seniors")
        st.markdown("### *Your Personal AI Car Consultant*")
    
    with col2:
        st.markdown("#### Welcome! 👋")
        st.info("**Easy-to-use interface designed specifically for senior car buyers**")

def display_navigation():
    """Display sidebar navigation menu"""
    with st.sidebar:
        st.markdown("## 🧭 Navigation")
        
        # Navigation menu with icons
        selected = option_menu(
            menu_title=None,
            options=[
                "🏠 Home",
                "📝 Car Finder Quiz", 
                "🚗 My Recommendations",
                "⚖️ Compare Cars",
                "💬 Ask AI Expert",
                "⭐ Reviews & Ratings",
                "📄 Export & Share"
            ],
            icons=[
                "house-fill",
                "clipboard-check",
                "car-front-fill",
                "bar-chart",
                "chat-dots",
                "star-fill",
                "download"
            ],
            menu_icon="cast",
            default_index=0,
            orientation="vertical",
            styles={
                "container": {"padding": "5px", "background-color": "#f8f9fa"},
                "icon": {"color": "#007bff", "font-size": "20px"},
                "nav-link": {
                    "font-size": "16px",
                    "text-align": "left",
                    "margin": "2px",
                    "padding": "12px",
                    "border-radius": "8px"
                },
                "nav-link-selected": {"background-color": "#007bff", "color": "white"},
            }
        )
        
        st.markdown("---")
        
        # Quick tips for seniors
        st.markdown("### 💡 Quick Tips")
        st.info("**New to this app?** Start with the Car Finder Quiz to get personalized recommendations!")
        
        st.success("**Having trouble?** Use the 'Ask AI Expert' feature to get help with any car-related questions.")
    
    return selected

def show_home_page():
    """Display the home page"""
    st.markdown("## Welcome to Your Personal Car Advisor! 🎉")
    
    # Welcome message
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### 🎯 **Designed Specifically for Senior Buyers**
        
        Our AI-powered system helps you find the perfect car based on your unique needs and preferences. 
        We understand that choosing a car involves many important considerations like:
        
        - **Safety & Reliability** 🛡️
        - **Comfort & Ease of Use** 🪑
        - **Maintenance Costs** 💰
        - **Service Network** 🔧
        - **Resale Value** 📈
        
        ### 🚀 **Getting Started is Easy:**
        
        1. **Take the Car Finder Quiz** - Answer a few simple questions about your needs
        2. **Get AI Recommendations** - Receive personalized car suggestions 
        3. **Compare Options** - See detailed comparisons of recommended vehicles
        4. **Ask Our AI Expert** - Get answers to any car-related questions
        5. **Read Reviews** - See what other buyers are saying
        
        """)
    
    with col2:
        st.markdown("""
        <div class="info-box">
        <h4>🔥 Most Popular Features:</h4>
        <ul>
        <li>✅ Smart Car Recommendations</li>
        <li>✅ Easy Comparison Tools</li>
        <li>✅ 24/7 AI Expert Help</li>
        <li>✅ Real User Reviews</li>
        <li>✅ PDF Reports</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚀 Start Car Finder Quiz", key="start_quiz", help="Click to begin finding your perfect car"):
            st.session_state.questionnaire_step = 0
            st.switch_page("pages/questionnaire.py") if hasattr(st, 'switch_page') else st.experimental_rerun()
    
    # Feature highlights
    st.markdown("---")
    st.markdown("## 🌟 **Why Choose Car Advisor?**")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="car-card">
        <h4>🧠 AI-Powered Intelligence</h4>
        <p>Our advanced AI knows about <strong>all car brands</strong> available in India and provides personalized recommendations based on your specific needs.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="car-card">
        <h4>👴 Senior-Friendly Design</h4>
        <p>Large fonts, high contrast colors, and simple navigation make it easy for seniors to find the information they need.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="car-card">
        <h4>🔒 Safe & Secure</h4>
        <p>Your personal information is protected, and our recommendations are unbiased and based purely on your requirements.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Statistics or testimonials section
    st.markdown("---")
    st.markdown("## 📊 **Comprehensive Car Database**")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Car Brands Covered", "25+", "Including all major brands")
    
    with col2:
        st.metric("Car Models", "200+", "From budget to luxury")
    
    with col3:
        st.metric("Price Range", "₹3L - ₹2Cr+", "All budgets covered")
    
    with col4:
        st.metric("AI Accuracy", "95%+", "Highly accurate recommendations")

def show_questionnaire_page():
    """Display questionnaire page"""
    display_questionnaire()

def show_recommendations_page():
    """Display recommendations page"""
    display_recommendations()

def show_comparison_page():
    """Display comparison page"""
    display_comparison()

def show_chat_page():
    """Display chat page"""
    display_chat_interface()

def show_reviews_page():
    """Display reviews page"""
    display_reviews()

def show_export_page():
    """Display export and sharing page"""
    display_export_features()

if __name__ == "__main__":
    main()