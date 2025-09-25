"""
AI Recommendation Engine for Car Advisor
OpenAI-powered car recommendations with comprehensive car knowledge
"""
import streamlit as st
import openai
import os
import json
import time
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class AICarRecommendationEngine:
    """AI-powered car recommendation system"""
    
    def __init__(self):
        self.client = None
        self._initialize_openai()
        self.car_database = self._load_car_database()
    
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
    
    def _load_car_database(self) -> Dict[str, Any]:
        """Load comprehensive car database for Indian market"""
        return {
            "brands": {
                "Maruti Suzuki": {
                    "strengths": "Largest service network, fuel efficient, affordable maintenance",
                    "popular_models": ["Swift", "Baleno", "Dzire", "Ertiga", "Vitara Brezza", "Alto", "WagonR", "Ciaz"],
                    "price_range": "₹3L - ₹15L",
                    "target_audience": "Budget-conscious, first-time buyers, reliable transportation"
                },
                "Hyundai": {
                    "strengths": "Feature-rich, good build quality, modern design, strong after-sales",
                    "popular_models": ["i20", "Creta", "Verna", "Venue", "Santro", "Grand i10 Nios", "Tucson"],
                    "price_range": "₹5L - ₹25L",
                    "target_audience": "Feature seekers, style-conscious buyers, premium experience"
                },
                "Tata": {
                    "strengths": "Indian brand, excellent safety ratings, modern interiors, competitive pricing",
                    "popular_models": ["Nexon", "Harrier", "Safari", "Altroz", "Tigor", "Punch", "Tiago"],
                    "price_range": "₹4L - ₹25L",
                    "target_audience": "Safety-conscious, patriotic buyers, premium features at value pricing"
                },
                "Honda": {
                    "strengths": "Reliable engines, fuel efficient, good resale value, refined driving",
                    "popular_models": ["City", "Amaze", "Jazz", "WR-V", "CR-V"],
                    "price_range": "₹6L - ₹35L",
                    "target_audience": "Reliability seekers, long-term ownership, smooth driving experience"
                },
                "Toyota": {
                    "strengths": "Legendary reliability, low maintenance, excellent resale value, hybrid technology",
                    "popular_models": ["Innova Crysta", "Fortuner", "Camry", "Glanza", "Urban Cruiser", "Vellfire"],
                    "price_range": "₹7L - ₹1Cr+",
                    "target_audience": "Reliability above all, premium buyers, commercial use"
                },
                "Mahindra": {
                    "strengths": "Rugged SUVs, good for rough terrain, spacious, strong build quality",
                    "popular_models": ["XUV700", "Thar", "Scorpio", "Bolero", "XUV300", "Marazzo"],
                    "price_range": "₹7L - ₹30L",
                    "target_audience": "Adventure enthusiasts, rural/semi-urban buyers, SUV lovers"
                },
                "Kia": {
                    "strengths": "Feature-loaded, long warranty, modern design, good value for money",
                    "popular_models": ["Seltos", "Sonet", "Carens", "Carnival"],
                    "price_range": "₹7L - ₹35L",
                    "target_audience": "Feature enthusiasts, style-conscious, tech-savvy buyers"
                },
                "MG Motor": {
                    "strengths": "Connected car technology, spacious interiors, competitive pricing, premium features",
                    "popular_models": ["Hector", "Astor", "ZS EV", "Gloster"],
                    "price_range": "₹10L - ₹40L",
                    "target_audience": "Tech enthusiasts, premium feature seekers, early adopters"
                },
                "BMW": {
                    "strengths": "Ultimate driving machine, luxury, performance, brand prestige",
                    "popular_models": ["3 Series", "5 Series", "X1", "X3", "X5", "7 Series"],
                    "price_range": "₹35L - ₹2Cr+",
                    "target_audience": "Luxury seekers, performance enthusiasts, status-conscious"
                },
                "Mercedes-Benz": {
                    "strengths": "Luxury, comfort, safety, brand prestige, advanced technology",
                    "popular_models": ["C-Class", "E-Class", "S-Class", "GLA", "GLC", "GLS"],
                    "price_range": "₹40L - ₹3Cr+",
                    "target_audience": "Ultimate luxury, comfort-focused, business executives"
                }
            },
            "categories": {
                "Hatchbacks": {
                    "characteristics": "Compact, easy to park, fuel efficient, affordable",
                    "ideal_for": "City driving, first-time buyers, parking constraints",
                    "examples": ["Maruti Swift", "Hyundai i20", "Tata Altroz"]
                },
                "Sedans": {
                    "characteristics": "Spacious rear seat, large boot, comfortable, prestigious",
                    "ideal_for": "Family use, highway driving, comfort priority",
                    "examples": ["Honda City", "Hyundai Verna", "Toyota Camry"]
                },
                "SUVs": {
                    "characteristics": "High seating, commanding view, rugged, spacious",
                    "ideal_for": "Rough roads, large families, adventure, status",
                    "examples": ["Tata Nexon", "Hyundai Creta", "Mahindra XUV700"]
                },
                "MPVs": {
                    "characteristics": "Maximum seating capacity, flexible interiors, family-focused",
                    "ideal_for": "Large families, commercial use, maximum space",
                    "examples": ["Toyota Innova", "Maruti Ertiga", "Kia Carens"]
                }
            }
        }
    
    def generate_recommendations(self, user_preferences: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate personalized car recommendations using AI"""
        if not self.client:
            return self._fallback_recommendations(user_preferences)
        
        try:
            # Create comprehensive prompt for AI
            prompt = self._create_recommendation_prompt(user_preferences)
            
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": self._get_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.7
            )
            
            # Parse and format response
            recommendations_text = response.choices[0].message.content
            recommendations = self._parse_ai_response(recommendations_text)
            
            return recommendations
            
        except Exception as e:
            st.error(f"AI recommendation failed: {str(e)}")
            return self._fallback_recommendations(user_preferences)
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt for AI recommendations"""
        return """You are an expert car consultant specializing in the Indian automotive market with deep knowledge of senior buyers' needs. You have comprehensive knowledge of ALL car brands available in India including Maruti Suzuki, Hyundai, Tata, Honda, Toyota, Mahindra, Kia, MG, Volkswagen, Skoda, Nissan, Renault, BMW, Mercedes-Benz, Audi, Volvo, Jaguar, Land Rover, and many others.

Your expertise includes:
- Understanding senior buyers' priorities: safety, comfort, ease of use, reliability, service network
- Knowledge of Indian road conditions and driving patterns
- Awareness of maintenance costs, fuel efficiency, and resale values
- Understanding of physical accessibility needs for senior drivers

Always provide recommendations that prioritize:
1. Safety features and build quality
2. Ease of driving and parking
3. Comfort and accessibility
4. Reliable after-sales service
5. Value for money and low maintenance

Format your response as a JSON array with exactly 5 car recommendations, each containing:
- model: Car name and variant
- brand: Manufacturer name
- price: Price range in Indian Rupees
- why_suitable: 2-3 sentences explaining why it's perfect for this senior buyer
- key_features: Array of 4-5 most relevant features
- pros: Array of 3-4 main advantages
- cons: Array of 2-3 honest limitations
- senior_friendly_rating: Number from 1-10 (10 being most senior-friendly)
- fuel_efficiency: Expected mileage
- safety_rating: Safety assessment
- maintenance_cost: Low/Medium/High assessment"""
    
    def _create_recommendation_prompt(self, preferences: Dict[str, Any]) -> str:
        """Create detailed prompt based on user preferences"""
        budget_min = preferences.get('budget_min', 300000)
        budget_max = preferences.get('budget_max', 1000000)
        
        prompt = f"""
Please recommend 5 cars for a senior buyer with these specific requirements:

BUDGET: ₹{budget_min:,} to ₹{budget_max:,}

PRIMARY USE: {preferences.get('primary_use', 'Not specified')}

FAMILY SIZE: {preferences.get('family_size', 'Not specified')}

DRIVING EXPERIENCE: {preferences.get('driving_experience', 'Not specified')}

FUEL PREFERENCE: {preferences.get('fuel_preference', 'No preference')}

IMPORTANT FEATURES: {', '.join(preferences.get('important_features', []))}

PHYSICAL CONSIDERATIONS: {', '.join(preferences.get('physical_considerations', []))}

BRAND PREFERENCES: {', '.join(preferences.get('brand_preference', []))}

ADDITIONAL REQUIREMENTS: {preferences.get('additional_requirements', 'None specified')}

Consider the Indian market, road conditions, service network availability, and senior-specific needs like easy entry/exit, simple controls, good visibility, and reliable after-sales support.

Provide a diverse mix covering different categories (hatchback, sedan, SUV, etc.) while staying within budget and matching the specific needs mentioned above.
"""
        return prompt
    
    def _parse_ai_response(self, response_text: str) -> List[Dict[str, Any]]:
        """Parse AI response and convert to structured format"""
        try:
            # Try to extract JSON from the response
            start_index = response_text.find('[')
            end_index = response_text.rfind(']')
            
            if start_index != -1 and end_index != -1:
                json_text = response_text[start_index:end_index + 1]
                recommendations = json.loads(json_text)
                
                # Validate and clean up recommendations
                cleaned_recommendations = []
                for rec in recommendations:
                    if all(key in rec for key in ['model', 'brand', 'price', 'why_suitable']):
                        cleaned_recommendations.append(rec)
                
                return cleaned_recommendations[:5]  # Limit to 5 recommendations
            
        except json.JSONDecodeError:
            pass
        
        # If JSON parsing fails, create structured response from text
        return self._parse_text_response(response_text)
    
    def _parse_text_response(self, response_text: str) -> List[Dict[str, Any]]:
        """Parse text response when JSON parsing fails"""
        # This is a simplified parser for when AI doesn't return proper JSON
        recommendations = []
        
        # Split by common patterns and extract car information
        lines = response_text.split('\n')
        current_car = {}
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Look for car model patterns
            if any(brand in line.upper() for brand in ['MARUTI', 'HYUNDAI', 'TATA', 'HONDA', 'TOYOTA']):
                if current_car and 'model' in current_car:
                    recommendations.append(current_car)
                    current_car = {}
                
                current_car['model'] = line
                current_car['brand'] = line.split()[0] if line else "Unknown"
                current_car['price'] = "Contact dealer for pricing"
                current_car['why_suitable'] = "Recommended based on your preferences"
                current_car['key_features'] = ["Feature information pending"]
                current_car['pros'] = ["Professional recommendation"]
                current_car['cons'] = ["Please verify specifications"]
                current_car['senior_friendly_rating'] = 8
                current_car['fuel_efficiency'] = "15-20 kmpl"
                current_car['safety_rating'] = "Good"
                current_car['maintenance_cost'] = "Medium"
        
        if current_car and 'model' in current_car:
            recommendations.append(current_car)
        
        return recommendations[:5]
    
    def _fallback_recommendations(self, preferences: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Provide fallback recommendations when AI is unavailable"""
        budget_min = preferences.get('budget_min', 300000)
        budget_max = preferences.get('budget_max', 1000000)
        
        # Basic rule-based recommendations
        fallback_cars = [
            {
                "model": "Maruti Suzuki Swift",
                "brand": "Maruti Suzuki", 
                "price": "₹6L - ₹9L",
                "why_suitable": "Excellent fuel efficiency, easy to drive, and extensive service network across India. Perfect for senior buyers who prioritize reliability.",
                "key_features": ["Excellent fuel efficiency", "Easy steering", "Compact size", "Trusted brand", "Wide service network"],
                "pros": ["Most fuel efficient", "Easy to park", "Low maintenance cost", "High resale value"],
                "cons": ["Limited rear space", "Road noise at high speeds"],
                "senior_friendly_rating": 9,
                "fuel_efficiency": "22-24 kmpl",
                "safety_rating": "4 stars",
                "maintenance_cost": "Low"
            },
            {
                "model": "Honda City",
                "brand": "Honda",
                "price": "₹11L - ₹16L", 
                "why_suitable": "Spacious and comfortable sedan with smooth automatic transmission option. Excellent for senior buyers who value comfort and refinement.",
                "key_features": ["Spacious interior", "Smooth CVT automatic", "Excellent build quality", "Good rear seat comfort", "Refined engine"],
                "pros": ["Very comfortable", "Smooth driving", "Good fuel efficiency", "Premium feel"],
                "cons": ["Higher price", "Limited ground clearance"],
                "senior_friendly_rating": 8,
                "fuel_efficiency": "17-19 kmpl",
                "safety_rating": "5 stars",
                "maintenance_cost": "Medium"
            },
            {
                "model": "Hyundai Creta",
                "brand": "Hyundai",
                "price": "₹11L - ₹18L",
                "why_suitable": "High seating position for easy entry/exit, loaded with safety features, and excellent visibility. Perfect SUV for senior buyers.",
                "key_features": ["High seating position", "360-degree camera", "Multiple airbags", "Automatic climate control", "Touchscreen infotainment"],
                "pros": ["Easy entry/exit", "Commanding view", "Feature loaded", "Good safety rating"],
                "cons": ["Slightly firm ride", "Higher fuel consumption"],
                "senior_friendly_rating": 8,
                "fuel_efficiency": "15-17 kmpl",
                "safety_rating": "5 stars",
                "maintenance_cost": "Medium"
            },
            {
                "model": "Toyota Innova Crysta",
                "brand": "Toyota", 
                "price": "₹17L - ₹25L",
                "why_suitable": "Legendary reliability, spacious for large families, and comfortable for long drives. Ideal for senior buyers who prioritize dependability.",
                "key_features": ["Legendary reliability", "Spacious 7-seater", "Comfortable ride", "Strong build quality", "Excellent resale value"],
                "pros": ["Ultra reliable", "Very spacious", "Comfortable seats", "Low depreciation"],
                "cons": ["High price", "Lower fuel efficiency"],
                "senior_friendly_rating": 9,
                "fuel_efficiency": "12-15 kmpl", 
                "safety_rating": "5 stars",
                "maintenance_cost": "Medium"
            },
            {
                "model": "Tata Nexon",
                "brand": "Tata",
                "price": "₹8L - ₹15L",
                "why_suitable": "Excellent safety rating, compact SUV with good features, and competitive pricing. Great choice for safety-conscious senior buyers.",
                "key_features": ["5-star safety rating", "Compact SUV design", "Good ground clearance", "Modern features", "Competitive pricing"],
                "pros": ["Safest car in segment", "Good value for money", "Compact yet spacious", "Modern design"],
                "cons": ["Engine noise", "Rear seat could be more spacious"],
                "senior_friendly_rating": 7,
                "fuel_efficiency": "16-18 kmpl",
                "safety_rating": "5 stars",
                "maintenance_cost": "Low"
            }
        ]
        
        # Filter by budget
        filtered_cars = []
        for car in fallback_cars:
            # Extract price range (simplified)
            price_text = car['price']
            if 'L' in price_text:
                try:
                    price_parts = price_text.replace('₹', '').replace('L', '').split(' - ')
                    min_price = float(price_parts[0]) * 100000
                    if min_price <= budget_max:
                        filtered_cars.append(car)
                except:
                    filtered_cars.append(car)  # Include if price parsing fails
        
        return filtered_cars[:5]

def display_recommendations():
    """Display AI-generated car recommendations"""
    st.markdown("## Car Recommendations")
    
    # Check if user has completed questionnaire
    if 'user_preferences' not in st.session_state or not st.session_state.user_preferences:
        st.info("Complete the questionnaire first to get personalized recommendations.")
        if st.button("Take Questionnaire", key="take_quiz_btn"):
            st.session_state.questionnaire_step = 0
            st.rerun()
        return
    
    # Initialize recommendation engine
    engine = AICarRecommendationEngine()
    
    # Generate recommendations if not already generated
    if 'recommendations' not in st.session_state or not st.session_state.recommendations:
        with st.spinner("Generating recommendations..."):
            recommendations = engine.generate_recommendations(st.session_state.user_preferences)
            st.session_state.recommendations = recommendations
    
    recommendations = st.session_state.recommendations
    
    if not recommendations:
        st.error("Unable to generate recommendations. Please try again.")
        return
    
    # Display recommendations
    st.markdown("### Recommended Cars:")
    
    for i, car in enumerate(recommendations, 1):
        with st.container():
            st.markdown(f"**{i}. {car.get('brand', 'N/A')} {car.get('model', 'Unknown Model')}**")
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.write(f"Price: {car.get('price', 'Contact dealer')}")
                st.write(car.get('why_suitable', 'Recommended based on your preferences.'))
                
                # Key features
                if 'key_features' in car and car['key_features']:
                    st.write("Key Features:")
                    for feature in car['key_features'][:3]:
                        st.write(f"• {feature}")
            
            with col2:
                # Quick specs
                if car.get('fuel_efficiency'):
                    st.write(f"Fuel Efficiency: {car.get('fuel_efficiency')}")
                if car.get('safety_rating'):
                    st.write(f"Safety Rating: {car.get('safety_rating')}")
                
                if st.button(f"Add to Compare", key=f"compare_{i}"):
                    if 'comparison_cars' not in st.session_state:
                        st.session_state.comparison_cars = []
                    if car not in st.session_state.comparison_cars:
                        st.session_state.comparison_cars.append(car)
                        st.success(f"Added {car.get('model', 'car')} to comparison!")
                    else:
                        st.info("Car already in comparison list.")
            
            # Pros and cons
            if 'pros' in car or 'cons' in car:
                col1, col2 = st.columns(2)
                
                with col1:
                    if 'pros' in car and car['pros']:
                        st.markdown("**👍 Pros:**")
                        for pro in car['pros']:
                            st.markdown(f"✅ {pro}")
                
                with col2:
                    if 'cons' in car and car['cons']:
                        st.markdown("**👎 Considerations:**")
                        for con in car['cons']:
                            st.markdown(f"⚠️ {con}")
            
            st.markdown("---")
    
    # Action buttons at the bottom
    st.markdown("### 🛠️ **What's Next?**")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🔄 New Recommendations", key="new_recs"):
            st.session_state.recommendations = []
            st.rerun()
    
    with col2:
        if st.button("⚖️ Compare Selected", key="compare_selected"):
            if st.session_state.get('comparison_cars', []):
                st.success(f"🎯 **Comparing {len(st.session_state.comparison_cars)} cars...**")
                st.info("🚧 **Comparison tool coming soon!**")
            else:
                st.warning("⚠️ **Please add cars to comparison first.**")
    
    with col3:
        if st.button("💬 Ask AI Expert", key="ask_ai_expert"):
            st.info("🚧 **AI Chat feature coming soon!**")
    
    with col4:
        if st.button("📄 Download Report", key="download_report"):
            st.info("🚧 **PDF export feature coming soon!**")

if __name__ == "__main__":
    display_recommendations()