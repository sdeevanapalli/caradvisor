"""
AI Chat Interface for Car Advisor
Interactive car consultation with OpenAI
"""
import streamlit as st
import openai
import os
import time
from typing import List, Dict, Any
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

class AICarExpert:
    """AI-powered car consultation chatbot"""
    
    def __init__(self):
        self.client = None
        self._initialize_openai()
        self.conversation_starters = [
            "Which car would be best for a 65-year old with knee problems?",
            "What's the difference between petrol and diesel cars?",
            "Which cars have the best safety features for seniors?",
            "How do I choose between automatic and manual transmission?",
            "What should I consider for maintenance costs?",
            "Which cars are easiest to get in and out of?",
            "What's the most fuel-efficient car in my budget?",
            "Which brands have the best service network in India?"
        ]
    
    def _initialize_openai(self):
        """Initialize OpenAI client"""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            st.error("⚠️ OpenAI API key not found. Please set OPENAI_API_KEY in your .env file.")
            return
        
        try:
            self.client = openai.OpenAI(api_key=api_key)
        except Exception as e:
            st.error(f"Failed to initialize OpenAI client: {str(e)}")
    
    def get_chat_response(self, message: str, chat_history: List[Dict], user_context: Dict = None) -> str:
        """Get response from AI car expert"""
        if not self.client:
            return "I'm sorry, I'm currently unavailable. Please try again later or contact support."
        
        try:
            # Create system prompt with context
            system_prompt = self._create_system_prompt(user_context)
            
            # Prepare conversation history
            messages = [{"role": "system", "content": system_prompt}]
            
            # Add chat history
            for chat in chat_history[-10:]:  # Keep last 10 messages for context
                messages.append({"role": "user", "content": chat["user"]})
                messages.append({"role": "assistant", "content": chat["assistant"]})
            
            # Add current message
            messages.append({"role": "user", "content": message})
            
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=800,
                temperature=0.7
            )
            
            return response.choices[0].message.content
        
        except Exception as e:
            return f"I apologize, but I encountered an error: {str(e)}. Please try asking your question in a different way."
    
    def _create_system_prompt(self, user_context: Dict = None) -> str:
        """Create system prompt for AI car expert"""
        base_prompt = """You are a friendly, knowledgeable car consultant specializing in helping senior buyers (60+ years) choose the perfect car in India. You have extensive knowledge of all car brands available in the Indian market including Maruti Suzuki, Hyundai, Tata, Honda, Toyota, Mahindra, Kia, MG, BMW, Mercedes, and many others.

Your expertise includes:
- Senior-friendly features and accessibility considerations
- Indian road conditions and driving patterns
- Maintenance costs, fuel efficiency, and service networks
- Safety features and reliability ratings
- Price comparisons and value for money
- Physical accessibility for senior drivers

Always prioritize:
🛡️ Safety and reliability above all
🪑 Comfort and ease of access
🔧 Low maintenance and service availability
💰 Value for money and fuel efficiency
🎯 Simple, user-friendly features

Communication style:
- Use simple, clear language (avoid technical jargon)
- Be patient and thorough in explanations
- Provide specific car model recommendations when appropriate
- Always explain WHY something is recommended for seniors
- Use emojis to make responses friendly and easy to read
- Break down complex information into digestible points"""
        
        if user_context:
            context_info = f"""

USER CONTEXT:
Budget Range: ₹{user_context.get('budget_min', 'Not specified'):,} - ₹{user_context.get('budget_max', 'Not specified'):,}
Primary Use: {user_context.get('primary_use', 'Not specified')}
Family Size: {user_context.get('family_size', 'Not specified')}
Fuel Preference: {user_context.get('fuel_preference', 'Not specified')}
Important Features: {', '.join(user_context.get('important_features', [])) if user_context.get('important_features') else 'Not specified'}
Physical Considerations: {', '.join(user_context.get('physical_considerations', [])) if user_context.get('physical_considerations') else 'None specified'}

Use this context to provide more personalized advice."""
            
            base_prompt += context_info
        
        return base_prompt

def display_chat_interface():
    """Main function to display AI chat interface"""
    st.markdown("## 💬 Ask Our AI Car Expert")
    st.markdown("### *Get instant answers to all your car-related questions*")
    
    # Initialize AI expert
    ai_expert = AICarExpert()
    
    # Initialize chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Get user context if available
    user_context = st.session_state.get('user_preferences', {})
    
    # Display welcome message and suggestions
    if not st.session_state.chat_history:
        display_welcome_section(ai_expert)
    
    # Chat history display
    if st.session_state.chat_history:
        st.markdown("### 💭 **Chat History**")
        
        # Create a container for chat messages
        chat_container = st.container()
        
        with chat_container:
            for i, chat in enumerate(st.session_state.chat_history):
                # User message
                st.markdown(f"""
                <div style="background-color: #e3f2fd; padding: 12px; border-radius: 10px; margin: 8px 0; border-left: 4px solid #2196f3;">
                <strong>🙋 You:</strong><br>{chat['user']}
                </div>
                """, unsafe_allow_html=True)
                
                # AI response
                st.markdown(f"""
                <div style="background-color: #f1f8e9; padding: 12px; border-radius: 10px; margin: 8px 0; border-left: 4px solid #4caf50;">
                <strong>🤖 AI Car Expert:</strong><br>{chat['assistant']}
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("---")
    
    # Chat input section
    st.markdown("### 💬 **Ask Your Question**")
    
    # Input methods
    col1, col2 = st.columns([3, 1])
    
    with col1:
        user_message = st.text_area(
            "Type your car-related question here:",
            placeholder="E.g., 'Which automatic car under ₹12 lakhs is best for seniors with joint problems?'",
            height=100,
            key="user_input"
        )
    
    with col2:
        st.markdown("**💡 Quick Tips:**")
        st.info("Be specific about your needs, budget, and any physical requirements for the best recommendations!")
        
        if st.button("🧹 Clear Chat", key="clear_chat", help="Start a fresh conversation"):
            st.session_state.chat_history = []
            st.rerun()
    
    # Send button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Ask AI Expert", key="send_message", help="Get expert advice from our AI"):
            if user_message.strip():
                # Show processing message
                with st.spinner("🤖 **AI Expert is thinking...**"):
                    # Simulate thinking time
                    time.sleep(1)
                    
                    # Get AI response
                    ai_response = ai_expert.get_chat_response(
                        user_message, 
                        st.session_state.chat_history,
                        user_context
                    )
                    
                    # Add to chat history
                    st.session_state.chat_history.append({
                        "user": user_message,
                        "assistant": ai_response,
                        "timestamp": time.time()
                    })
                    
                    # Clear input and refresh
                    st.session_state.user_input = ""
                    st.rerun()
            else:
                st.warning("⚠️ **Please enter a question before sending.**")
    
    # Quick action buttons
    if st.session_state.chat_history:
        st.markdown("---")
        st.markdown("### 🛠️ **Quick Actions**")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("📝 Retake Quiz", key="retake_quiz_chat"):
                st.session_state.user_preferences = {}
                st.session_state.questionnaire_step = 0
                st.success("🔄 **Starting fresh questionnaire...**")
        
        with col2:
            if st.button("🚗 View Recommendations", key="view_recs_chat"):
                if st.session_state.get('recommendations'):
                    st.success("🎯 **Showing your recommendations...**")
                else:
                    st.info("📝 **Please complete the quiz first to get recommendations.**")
        
        with col3:
            if st.button("⚖️ Compare Cars", key="compare_cars_chat"):
                if st.session_state.get('comparison_cars'):
                    st.success(f"📊 **Comparing {len(st.session_state.comparison_cars)} cars...**")
                else:
                    st.info("🚗 **Please add cars to comparison first.**")
        
        with col4:
            if st.button("📄 Export Chat", key="export_chat"):
                st.info("🚧 **Chat export coming soon!**")

def display_welcome_section(ai_expert: AICarExpert):
    """Display welcome section with conversation starters"""
    st.markdown("""
    ### 👋 **Welcome to Your Personal AI Car Expert!**
    
    I'm here to help you with all your car-related questions. Whether you're confused about which car to choose, 
    want to understand different features, or need advice on maintenance - just ask!
    """)
    
    # Conversation starters
    st.markdown("### 🎯 **Popular Questions from Senior Buyers:**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        for i, starter in enumerate(ai_expert.conversation_starters[:4]):
            if st.button(f"💡 {starter}", key=f"starter_{i}", help="Click to ask this question"):
                # Add this question to chat
                user_context = st.session_state.get('user_preferences', {})
                
                with st.spinner("🤖 **Getting expert advice...**"):
                    ai_response = ai_expert.get_chat_response(starter, [], user_context)
                    
                    st.session_state.chat_history.append({
                        "user": starter,
                        "assistant": ai_response,
                        "timestamp": time.time()
                    })
                    
                    st.rerun()
    
    with col2:
        for i, starter in enumerate(ai_expert.conversation_starters[4:], 4):
            if st.button(f"💡 {starter}", key=f"starter_{i}", help="Click to ask this question"):
                # Add this question to chat
                user_context = st.session_state.get('user_preferences', {})
                
                with st.spinner("🤖 **Getting expert advice...**"):
                    ai_response = ai_expert.get_chat_response(starter, [], user_context)
                    
                    st.session_state.chat_history.append({
                        "user": starter,
                        "assistant": ai_response,
                        "timestamp": time.time()
                    })
                    
                    st.rerun()
    
    # Show user context if available
    user_context = st.session_state.get('user_preferences', {})
    if user_context:
        st.markdown("---")
        st.success("✅ **I have your quiz preferences and can provide personalized advice!**")
        
        with st.expander("👁️ Your Quiz Results (helps me give better advice)"):
            if 'budget' in user_context:
                budget_min, budget_max = user_context['budget']
                st.write(f"**Budget:** ₹{budget_min:,} - ₹{budget_max:,}")
            
            for key, value in user_context.items():
                if key not in ['budget', 'budget_min', 'budget_max'] and value:
                    display_key = key.replace('_', ' ').title()
                    if isinstance(value, list):
                        st.write(f"**{display_key}:** {', '.join(value)}")
                    else:
                        st.write(f"**{display_key}:** {value}")
    else:
        st.info("💡 **Tip:** Complete the Car Finder Quiz first to get more personalized advice!")

if __name__ == "__main__":
    display_chat_interface()