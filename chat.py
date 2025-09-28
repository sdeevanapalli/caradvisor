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
            "What car should I buy for daily commuting?",
            "What's the difference between petrol and diesel cars?",
            "Which cars have the best safety features?",
            "Should I choose automatic or manual transmission?",
            "What are typical maintenance costs?",
            "What's the most fuel-efficient car in my budget?",
            "Which brands have the best service network in India?",
            "How do I choose between sedan and SUV?"
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
        base_prompt = """You are a knowledgeable car consultant helping people choose the right car in India. You have extensive knowledge of all car brands available in the Indian market including Maruti Suzuki, Hyundai, Tata, Honda, Toyota, Mahindra, Kia, MG, BMW, Mercedes, and many others.

Your expertise includes:
- Indian road conditions and driving patterns
- Maintenance costs, fuel efficiency, and service networks
- Safety features and reliability ratings
- Price comparisons and value for money
- Different car categories (hatchback, sedan, SUV, etc.)

Always prioritize:
- Safety and reliability
- Comfort and practicality
- Maintenance and service availability
- Value for money and fuel efficiency
- User-specific requirements

Communication style:
- Use clear, professional language
- Be thorough but concise in explanations
- Provide specific car model recommendations when appropriate
- Always explain the reasoning behind recommendations
- Focus on practical advice"""
        
        if user_context:
            context_info = f"""

USER CONTEXT:
Budget: ₹{user_context.get('budget_min', 'Not specified'):,} - ₹{user_context.get('budget_max', 'Not specified'):,}
Primary Use: {user_context.get('primary_use', 'Not specified')}
Fuel Preference: {user_context.get('fuel_preference', 'Not specified')}

Use this context for personalized advice."""
            
            base_prompt += context_info
        
        return base_prompt

def display_chat_interface():
    """Main function to display AI chat interface"""
    st.markdown("## Chat with AI Car Expert")
    
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
    for chat in st.session_state.chat_history:
        # User message
        with st.chat_message("user"):
            st.write(chat['user'])
        
        # AI response
        with st.chat_message("assistant"):
            st.write(chat['assistant'])
    
    # Chat input
    user_message = st.chat_input("Ask about cars...")
    
    if user_message:
        # Add user message to chat
        with st.chat_message("user"):
            st.write(user_message)
        
        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                ai_response = ai_expert.get_chat_response(
                    user_message, 
                    st.session_state.chat_history,
                    user_context
                )
                st.write(ai_response)
        
        # Add to chat history
        st.session_state.chat_history.append({
            "user": user_message,
            "assistant": ai_response,
            "timestamp": time.time()
        })
    
    # Clear chat button
    if st.session_state.chat_history and st.button("Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()

def display_welcome_section(ai_expert: AICarExpert):
    """Display welcome section with conversation starters"""
    st.markdown("### Welcome! Ask me anything about cars.")
    
    st.markdown("**Common questions:**")
    
    for i, starter in enumerate(ai_expert.conversation_starters):
        if st.button(starter, key=f"starter_{i}"):
            user_context = st.session_state.get('user_preferences', {})
            
            with st.spinner("Getting advice..."):
                ai_response = ai_expert.get_chat_response(starter, [], user_context)
                
                st.session_state.chat_history.append({
                    "user": starter,
                    "assistant": ai_response,
                    "timestamp": time.time()
                })
                
                st.rerun()

if __name__ == "__main__":
    display_chat_interface()