"""
Smart Questionnaire System for Car Advisor
Dynamic, AI-powered questionnaire that adapts based on user responses
"""
import streamlit as st
from typing import Dict, List, Any, Optional
import json

class CarQuestionnaire:
    """Smart questionnaire system for car recommendations"""
    
    def __init__(self):
        self.questions = self._initialize_questions()
        self.current_step = 0
        self.total_steps = len(self.questions)
    
    def _initialize_questions(self) -> List[Dict[str, Any]]:
        """Initialize the questionnaire structure"""
        return [
            {
                "id": "budget",
                "title": "What's your budget range?",
                "type": "budget_slider",
                "description": "Select your comfortable price range for the car",
                "required": True,
                "options": {
                    "min_value": 300000,
                    "max_value": 5000000,
                    "step": 50000,
                    "format": "₹%d"
                },
                "help_text": "💡 Consider total cost including insurance, registration, and initial maintenance"
            },
            {
                "id": "primary_use",
                "title": "What will be the primary use of your car?",
                "type": "single_select",
                "description": "This helps us understand your main driving needs",
                "required": True,
                "options": [
                    "Daily city commuting",
                    "Weekend leisure drives", 
                    "Long distance travel",
                    "Family outings and shopping",
                    "Medical appointments and errands",
                    "Occasional use (2-3 times per week)",
                    "Multiple purposes"
                ],
                "help_text": "💡 Your primary use affects recommendations for comfort, fuel efficiency, and features"
            },
            {
                "id": "family_size",
                "title": "How many people will regularly travel in the car?",
                "type": "single_select",
                "description": "Including yourself and regular passengers",
                "required": True,
                "options": [
                    "Just me (1 person)",
                    "Me and my spouse (2 people)",
                    "2-4 people regularly",
                    "5-7 people regularly",
                    "Need flexibility for varying numbers"
                ],
                "help_text": "💡 This determines seating capacity and interior space requirements"
            },
            {
                "id": "driving_experience",
                "title": "How would you describe your driving experience?",
                "type": "single_select", 
                "description": "This helps us recommend cars that match your comfort level",
                "required": True,
                "options": [
                    "New driver (less than 2 years)",
                    "Experienced city driver",
                    "Experienced highway driver", 
                    "Very experienced (30+ years)",
                    "Prefer easy-to-drive cars",
                    "Comfortable with any car type"
                ],
                "help_text": "💡 We'll recommend cars with appropriate ease of handling"
            },
            {
                "id": "fuel_preference",
                "title": "What fuel type do you prefer?",
                "type": "single_select",
                "description": "Consider fuel costs, availability, and environmental impact",
                "required": True,
                "options": [
                    "Petrol (easy maintenance)",
                    "Diesel (better mileage for long drives)",
                    "CNG (most economical)",
                    "Electric (eco-friendly, low running cost)",
                    "Hybrid (best of both worlds)",
                    "No preference (show me all options)"
                ],
                "help_text": "💡 Different fuel types have different benefits and costs"
            },
            {
                "id": "important_features",
                "title": "Which features are most important to you?",
                "type": "multi_select",
                "description": "Select all features that matter to you (you can choose multiple)",
                "required": True,
                "options": [
                    "🛡️ Advanced safety features (airbags, ABS, etc.)",
                    "❄️ Air conditioning (automatic climate control)",
                    "🎵 Good music system (touchscreen, bluetooth)",
                    "🪑 Comfortable seating (adjustable, cushioned)",
                    "🚗 Easy parking (parking sensors, camera)",
                    "⛽ Excellent fuel efficiency",
                    "🔧 Low maintenance cost",
                    "📱 Modern technology (navigation, smartphone connectivity)",
                    "🎒 Large boot/storage space",
                    "🏔️ Good ground clearance (for rough roads)"
                ],
                "help_text": "💡 We'll prioritize cars that have your preferred features"
            },
            {
                "id": "physical_considerations",
                "title": "Do you have any physical considerations for driving?",
                "type": "multi_select",
                "description": "This helps us recommend cars with appropriate accessibility features",
                "required": False,
                "options": [
                    "Need easy entry/exit (higher seating position)",
                    "Prefer power steering (light steering wheel)",
                    "Need good visibility (large windows, mirrors)",
                    "Require comfortable driver seat (adjustable)",
                    "Need automatic transmission (no clutch)",
                    "Prefer simple controls (easy-to-reach buttons)",
                    "None of the above"
                ],
                "help_text": "💡 We can recommend cars designed for comfort and accessibility"
            },
            {
                "id": "brand_preference",
                "title": "Do you have any brand preferences?",
                "type": "multi_select", 
                "description": "Based on your experience or service network preferences",
                "required": False,
                "options": [
                    "Maruti Suzuki (largest service network)",
                    "Hyundai (good features and reliability)",
                    "Tata (Indian brand with modern cars)",
                    "Honda (reliable and fuel efficient)",
                    "Toyota (low maintenance, high resale)",
                    "Mahindra (SUVs and rugged vehicles)",
                    "Kia (modern features and warranty)",
                    "MG (feature-rich cars)",
                    "Volkswagen/Skoda (European engineering)",
                    "Premium brands (BMW, Mercedes, Audi)",
                    "No preference (show me the best options)"
                ],
                "help_text": "💡 Different brands have different strengths and service networks"
            },
            {
                "id": "additional_requirements", 
                "title": "Any additional requirements or preferences?",
                "type": "text_area",
                "description": "Tell us anything else that's important for your car choice",
                "required": False,
                "placeholder": "E.g., 'Need a car that's easy to maintain', 'Must have good resale value', 'Prefer cars with local service center', etc.",
                "help_text": "💡 This helps our AI provide more personalized recommendations"
            }
        ]
    
    def display_progress(self, current_step: int):
        """Display progress bar and step information"""
        progress = (current_step + 1) / self.total_steps
        st.progress(progress)
        
        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown(f"**Step {current_step + 1} of {self.total_steps}**")
        with col2:
            st.markdown(f"**Progress: {int(progress * 100)}%**")
        
        st.markdown("---")
    
    def render_question(self, question: Dict[str, Any]) -> Any:
        """Render a single question based on its type"""
        st.markdown(f"### {question['title']}")
        st.markdown(f"*{question['description']}*")
        
        if question.get('help_text'):
            st.info(question['help_text'])
        
        question_id = question['id']
        
        if question['type'] == 'budget_slider':
            return self._render_budget_slider(question, question_id)
        elif question['type'] == 'single_select':
            return self._render_single_select(question, question_id)
        elif question['type'] == 'multi_select':
            return self._render_multi_select(question, question_id)
        elif question['type'] == 'text_area':
            return self._render_text_area(question, question_id)
        
        return None
    
    def _render_budget_slider(self, question: Dict[str, Any], question_id: str) -> tuple:
        """Render budget range slider"""
        options = question['options']
        
        # Get current values from session state
        current_min = st.session_state.user_preferences.get(f"{question_id}_min", options['min_value'])
        current_max = st.session_state.user_preferences.get(f"{question_id}_max", options['max_value'] // 2)
        
        # Create slider for budget range
        budget_range = st.slider(
            "Select your budget range (minimum to maximum)",
            min_value=options['min_value'],
            max_value=options['max_value'],
            value=(current_min, current_max),
            step=options['step'],
            format=options['format'],
            key=f"{question_id}_slider"
        )
        
        # Display selected range clearly
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Minimum Budget", f"₹{budget_range[0]:,}")
        with col2:
            st.metric("Maximum Budget", f"₹{budget_range[1]:,}")
        with col3:
            st.metric("Range", f"₹{budget_range[1] - budget_range[0]:,}")
        
        return budget_range
    
    def _render_single_select(self, question: Dict[str, Any], question_id: str) -> str:
        """Render single selection dropdown"""
        current_value = st.session_state.user_preferences.get(question_id, None)
        
        # Find index of current value
        index = 0
        if current_value and current_value in question['options']:
            index = question['options'].index(current_value)
        
        return st.selectbox(
            "Select your answer:",
            options=question['options'],
            index=index,
            key=f"{question_id}_select"
        )
    
    def _render_multi_select(self, question: Dict[str, Any], question_id: str) -> List[str]:
        """Render multi-selection checkboxes"""
        current_value = st.session_state.user_preferences.get(question_id, [])
        
        return st.multiselect(
            "Select all that apply:",
            options=question['options'],
            default=current_value,
            key=f"{question_id}_multiselect"
        )
    
    def _render_text_area(self, question: Dict[str, Any], question_id: str) -> str:
        """Render text area for additional input"""
        current_value = st.session_state.user_preferences.get(question_id, "")
        
        return st.text_area(
            "Your input:",
            value=current_value,
            placeholder=question.get('placeholder', 'Please share your thoughts...'),
            height=100,
            key=f"{question_id}_textarea"
        )
    
    def validate_answer(self, question: Dict[str, Any], answer: Any) -> bool:
        """Validate user's answer"""
        if question['required'] and not answer:
            return False
        
        if question['type'] == 'multi_select' and question['required'] and len(answer) == 0:
            return False
        
        return True
    
    def save_answer(self, question_id: str, answer: Any):
        """Save answer to session state"""
        if question_id == "budget":
            # Special handling for budget range
            st.session_state.user_preferences[f"{question_id}_min"] = answer[0]
            st.session_state.user_preferences[f"{question_id}_max"] = answer[1]
            st.session_state.user_preferences[question_id] = answer
        else:
            st.session_state.user_preferences[question_id] = answer
    
    def get_completion_summary(self) -> str:
        """Generate a summary of user preferences"""
        prefs = st.session_state.user_preferences
        
        summary_parts = []
        
        if 'budget' in prefs:
            budget_min, budget_max = prefs['budget']
            summary_parts.append(f"Budget: ₹{budget_min:,} - ₹{budget_max:,}")
        
        if 'primary_use' in prefs:
            summary_parts.append(f"Primary use: {prefs['primary_use']}")
        
        if 'family_size' in prefs:
            summary_parts.append(f"Family size: {prefs['family_size']}")
        
        if 'fuel_preference' in prefs:
            summary_parts.append(f"Fuel preference: {prefs['fuel_preference']}")
        
        if 'important_features' in prefs and prefs['important_features']:
            features = ', '.join(prefs['important_features'][:3])  # Show first 3 features
            if len(prefs['important_features']) > 3:
                features += f" (and {len(prefs['important_features']) - 3} more)"
            summary_parts.append(f"Key features: {features}")
        
        return " | ".join(summary_parts)

def display_questionnaire():
    """Main function to display the questionnaire"""
    st.markdown("## 📝 Car Finder Questionnaire")
    st.markdown("### *Let's find your perfect car in just a few steps!*")
    
    # Initialize questionnaire
    questionnaire = CarQuestionnaire()
    
    # Get current step from session state
    if 'questionnaire_step' not in st.session_state:
        st.session_state.questionnaire_step = 0
    
    current_step = st.session_state.questionnaire_step
    
    # Check if questionnaire is complete
    if current_step >= len(questionnaire.questions):
        display_completion_page(questionnaire)
        return
    
    # Display progress
    questionnaire.display_progress(current_step)
    
    # Get current question
    current_question = questionnaire.questions[current_step]
    
    # Render question
    answer = questionnaire.render_question(current_question)
    
    # Navigation buttons
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if current_step > 0:
            if st.button("⬅️ Previous", key="prev_btn", help="Go to previous question"):
                st.session_state.questionnaire_step -= 1
                st.rerun()
    
    with col3:
        if st.button("Next ➡️" if current_step < len(questionnaire.questions) - 1 else "Complete ✅", 
                    key="next_btn", help="Continue to next question"):
            
            # Validate answer
            if questionnaire.validate_answer(current_question, answer):
                # Save answer
                questionnaire.save_answer(current_question['id'], answer)
                
                # Move to next step
                st.session_state.questionnaire_step += 1
                st.rerun()
            else:
                st.error("❌ **Please answer this required question before proceeding.**")
    
    with col2:
        st.markdown(f"<div style='text-align: center; padding-top: 8px;'>Question {current_step + 1} of {len(questionnaire.questions)}</div>", 
                   unsafe_allow_html=True)

def display_completion_page(questionnaire: CarQuestionnaire):
    """Display questionnaire completion page"""
    st.markdown("## 🎉 Questionnaire Complete!")
    st.markdown("### Thank you for providing your preferences!")
    
    # Display summary
    st.markdown("### 📋 Your Preferences Summary:")
    summary = questionnaire.get_completion_summary()
    st.success(summary)
    
    # Show detailed preferences
    with st.expander("📊 View Detailed Preferences"):
        prefs = st.session_state.user_preferences
        for key, value in prefs.items():
            if key.endswith('_min') or key.endswith('_max'):
                continue  # Skip individual budget components
            st.write(f"**{key.replace('_', ' ').title()}:** {value}")
    
    # Action buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Retake Quiz", key="retake_quiz", help="Start questionnaire over"):
            # Clear preferences and reset
            st.session_state.user_preferences = {}
            st.session_state.questionnaire_step = 0
            st.rerun()
    
    with col2:
        if st.button("🚗 Get Recommendations", key="get_recommendations", 
                    help="Generate AI recommendations based on your preferences"):
            st.session_state.show_recommendations = True
            st.success("🎯 **Generating your personalized car recommendations...**")
            st.info("💡 **Tip:** This may take a moment as our AI analyzes your preferences against our car database.")
    
    with col3:
        if st.button("💬 Ask AI Expert", key="ask_expert", help="Chat with our AI car expert"):
            st.info("🚧 **Coming Soon:** AI Chat feature will be available shortly!")

if __name__ == "__main__":
    display_questionnaire()