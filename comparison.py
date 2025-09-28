"""
Car Comparison Tools for Car Advisor
Visual comparison interface with charts and feature matrix
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import Dict, List, Any
import numpy as np

class CarComparisonEngine:
    """Car comparison and visualization engine"""
    
    def __init__(self):
        self.comparison_categories = {
            "💰 Price & Value": ["price", "maintenance_cost", "fuel_efficiency", "resale_value"],
            "🛡️ Safety & Reliability": ["safety_rating", "build_quality", "reliability_score"],
            "🪑 Comfort & Convenience": ["interior_space", "seat_comfort", "ease_of_use", "features"],
            "🚗 Performance & Efficiency": ["engine_power", "fuel_efficiency", "handling", "ride_quality"],
            "🔧 Maintenance & Service": ["maintenance_cost", "service_network", "parts_availability"]
        }
    
    def create_comparison_matrix(self, cars: List[Dict[str, Any]]) -> pd.DataFrame:
        """Create a comparison matrix for selected cars"""
        if not cars:
            return pd.DataFrame()
        
        # Define comparison attributes
        attributes = [
            "Model",
            "Brand", 
            "Price Range",
            "Fuel Efficiency",
            "Safety Rating",
            "Maintenance Cost",
            "Senior Friendly Rating",
            "Key Features Count"
        ]
        
        comparison_data = {}
        
        for i, car in enumerate(cars):
            car_name = f"{car.get('brand', 'Unknown')} {car.get('model', 'Unknown')}"
            comparison_data[car_name] = [
                car.get('model', 'N/A'),
                car.get('brand', 'N/A'),
                car.get('price', 'N/A'),
                car.get('fuel_efficiency', 'N/A'),
                car.get('safety_rating', 'N/A'),
                car.get('maintenance_cost', 'N/A'),
                f"{car.get('senior_friendly_rating', 'N/A')}/10",
                len(car.get('key_features', []))
            ]
        
        df = pd.DataFrame(comparison_data, index=attributes)
        return df.transpose()
    
    def create_radar_chart(self, cars: List[Dict[str, Any]]) -> go.Figure:
        """Create radar chart for car comparison"""
        if not cars:
            return go.Figure()
        
        # Define criteria for radar chart (normalized to 0-10 scale)
        criteria = [
            "Safety Rating",
            "Senior Friendly",
            "Fuel Efficiency", 
            "Value for Money",
            "Comfort Level",
            "Ease of Use",
            "Feature Richness"
        ]
        
        fig = go.Figure()
        
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#98D8C8']
        
        for i, car in enumerate(cars):
            # Simulate scores based on car data (in real app, these would be calculated)
            scores = self._calculate_radar_scores(car)
            
            fig.add_trace(go.Scatterpolar(
                r=scores,
                theta=criteria,
                fill='toself',
                name=f"{car.get('brand', 'Unknown')} {car.get('model', 'Unknown')}",
                line_color=colors[i % len(colors)],
                fillcolor=colors[i % len(colors)],
                opacity=0.3
            ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 10]
                )),
            showlegend=True,
            title="Car Comparison Radar Chart",
            title_x=0.5,
            height=500
        )
        
        return fig
    
    def _calculate_radar_scores(self, car: Dict[str, Any]) -> List[float]:
        """Calculate normalized scores for radar chart"""
        # This is a simplified scoring system - in reality, you'd have more sophisticated calculations
        
        # Safety Rating (convert star ratings to 0-10 scale)
        safety_text = str(car.get('safety_rating', '3')).lower()
        if '5' in safety_text or 'excellent' in safety_text:
            safety_score = 10
        elif '4' in safety_text or 'good' in safety_text:
            safety_score = 8
        elif '3' in safety_text or 'average' in safety_text:
            safety_score = 6
        else:
            safety_score = 5
        
        # Senior Friendly Rating
        senior_friendly = car.get('senior_friendly_rating', 5)
        
        # Fuel Efficiency (convert kmpl to 0-10 scale)
        fuel_text = str(car.get('fuel_efficiency', '15')).lower()
        fuel_num = 15  # default
        try:
            # Extract number from text like "15-20 kmpl"
            import re
            numbers = re.findall(r'\d+', fuel_text)
            if numbers:
                fuel_num = int(numbers[0])
        except:
            pass
        
        fuel_score = min(10, max(0, (fuel_num - 5) / 2))  # Scale 5-25 kmpl to 0-10
        
        # Value for Money (based on price and features)
        features_count = len(car.get('key_features', []))
        value_score = min(10, features_count)
        
        # Comfort Level (based on car type and description)
        comfort_keywords = ['comfortable', 'spacious', 'luxury', 'smooth', 'refined']
        comfort_score = 6  # default
        description = str(car.get('why_suitable', '')).lower()
        for keyword in comfort_keywords:
            if keyword in description:
                comfort_score += 1
        comfort_score = min(10, comfort_score)
        
        # Ease of Use (higher for automatic, smaller cars, etc.)
        ease_score = 7  # default
        if 'automatic' in description or 'easy' in description:
            ease_score += 2
        if 'compact' in description or 'small' in description:
            ease_score += 1
        ease_score = min(10, ease_score)
        
        # Feature Richness
        feature_score = min(10, len(car.get('key_features', [])) * 2)
        
        return [safety_score, senior_friendly, fuel_score, value_score, comfort_score, ease_score, feature_score]
    
    def create_price_comparison(self, cars: List[Dict[str, Any]]) -> go.Figure:
        """Create price comparison bar chart"""
        if not cars:
            return go.Figure()
        
        car_names = []
        price_ranges = []
        colors = []
        
        for car in cars:
            car_name = f"{car.get('brand', 'Unknown')}<br>{car.get('model', 'Unknown')}"
            car_names.append(car_name)
            
            # Extract price range (simplified)
            price_text = car.get('price', '₹10L - ₹15L')
            try:
                # Extract numbers from price text
                import re
                numbers = re.findall(r'\d+', price_text.replace('₹', '').replace('L', '').replace('Cr', '00'))
                if len(numbers) >= 2:
                    min_price = int(numbers[0])
                    max_price = int(numbers[1])
                    if 'Cr' in price_text:
                        min_price *= 100
                        max_price *= 100
                    avg_price = (min_price + max_price) / 2
                else:
                    avg_price = 10  # default
            except:
                avg_price = 10  # default
            
            price_ranges.append(avg_price)
            
            # Color based on price range
            if avg_price <= 8:
                colors.append('#27AE60')  # Green for budget
            elif avg_price <= 20:
                colors.append('#F39C12')  # Orange for mid-range
            else:
                colors.append('#E74C3C')  # Red for premium
        
        fig = go.Figure(data=[
            go.Bar(
                x=car_names,
                y=price_ranges,
                marker_color=colors,
                text=[f"₹{price}L" for price in price_ranges],
                textposition='auto',
            )
        ])
        
        fig.update_layout(
            title="Price Comparison (Average Price)",
            xaxis_title="Cars",
            yaxis_title="Price (in Lakhs ₹)",
            showlegend=False,
            height=400
        )
        
        return fig
    
    def create_feature_comparison(self, cars: List[Dict[str, Any]]) -> pd.DataFrame:
        """Create detailed feature comparison table"""
        if not cars:
            return pd.DataFrame()
        
        # Collect all unique features
        all_features = set()
        for car in cars:
            features = car.get('key_features', [])
            all_features.update(features)
        
        # Create comparison matrix
        feature_data = {}
        for car in cars:
            car_name = f"{car.get('brand', '')} {car.get('model', '')}"
            car_features = car.get('key_features', [])
            
            feature_status = []
            for feature in sorted(all_features):
                if feature in car_features:
                    feature_status.append('✅')
                else:
                    feature_status.append('❌')
            
            feature_data[car_name] = feature_status
        
        df = pd.DataFrame(feature_data, index=sorted(all_features))
        return df

def display_comparison():
    """Main function to display car comparison interface"""
    st.markdown("## Car Comparison")
    
    # Check if there are cars to compare
    comparison_cars = st.session_state.get('comparison_cars', [])
    
    if not comparison_cars:
        st.info("No cars added for comparison yet.")
        st.markdown("""
        **To add cars for comparison:**
        1. Complete the questionnaire
        2. View recommendations
        3. Click "Add to Compare" on cars you like
        """)
        return
    
    # Display comparison table
    st.markdown(f"Comparing {len(comparison_cars)} cars:")
    
    # Simple comparison table
    for i, car in enumerate(comparison_cars):
        st.markdown(f"**{car.get('brand', 'Unknown')} {car.get('model', 'Unknown')}**")
        col1, col2 = st.columns([2, 1])
        with col1:
            st.write(f"Price: {car.get('price', 'N/A')}")
            st.write(f"Fuel Efficiency: {car.get('fuel_efficiency', 'N/A')}")
            st.write(f"Safety Rating: {car.get('safety_rating', 'N/A')}")
        with col2:
            if st.button(f"Remove", key=f"remove_{i}"):
                st.session_state.comparison_cars.remove(car)
                st.rerun()
        st.markdown("---")
    
    if st.button("Clear All"):
        st.session_state.comparison_cars = []
        st.rerun()
    


if __name__ == "__main__":
    display_comparison()