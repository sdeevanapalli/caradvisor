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
    st.markdown("## ⚖️ Car Comparison Tool")
    st.markdown("### *Compare your shortlisted cars side-by-side*")
    
    # Check if there are cars to compare
    comparison_cars = st.session_state.get('comparison_cars', [])
    
    if not comparison_cars:
        st.info("🚗 **No cars added for comparison yet.**")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("""
            ### How to Add Cars for Comparison:
            1. 📝 **Complete the Car Finder Quiz**
            2. 🎯 **View Your Recommendations**
            3. ⚖️ **Click "Add to Compare" on cars you like**
            4. 🔄 **Return here to see detailed comparisons**
            """)
            
            if st.button("📝 Go to Car Finder Quiz", key="goto_quiz"):
                st.session_state.questionnaire_step = 0
                st.rerun()
        
        # Show sample comparison interface
        st.markdown("---")
        st.markdown("### 👀 **Preview: What You'll See When Comparing Cars**")
        
        # Sample data for demonstration
        sample_cars = [
            {
                "model": "Swift",
                "brand": "Maruti Suzuki",
                "price": "₹6L - ₹9L",
                "fuel_efficiency": "22-24 kmpl",
                "safety_rating": "4 stars",
                "maintenance_cost": "Low",
                "senior_friendly_rating": 9,
                "key_features": ["Excellent fuel efficiency", "Easy steering", "Compact size", "Wide service network"],
                "why_suitable": "Perfect for city driving and easy parking"
            },
            {
                "model": "City",
                "brand": "Honda", 
                "price": "₹11L - ₹16L",
                "fuel_efficiency": "17-19 kmpl",
                "safety_rating": "5 stars", 
                "maintenance_cost": "Medium",
                "senior_friendly_rating": 8,
                "key_features": ["Spacious interior", "Smooth CVT automatic", "Excellent build quality", "Premium feel"],
                "why_suitable": "Ideal for comfort and long drives"
            }
        ]
        
        engine = CarComparisonEngine()
        
        # Show sample radar chart
        st.markdown("#### 📊 **Sample Radar Chart Comparison**")
        sample_radar = engine.create_radar_chart(sample_cars)
        st.plotly_chart(sample_radar, use_container_width=True)
        
        return
    
    # Main comparison interface
    st.success(f"✅ **Comparing {len(comparison_cars)} cars**")
    
    # Car selection management
    with st.expander("🔧 Manage Cars in Comparison"):
        st.markdown("**Currently comparing:**")
        
        cars_to_remove = []
        for i, car in enumerate(comparison_cars):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"🚗 **{car.get('brand', 'Unknown')} {car.get('model', 'Unknown')}** - {car.get('price', 'N/A')}")
            with col2:
                if st.button("❌ Remove", key=f"remove_car_{i}"):
                    cars_to_remove.append(car)
        
        # Remove selected cars
        if cars_to_remove:
            for car in cars_to_remove:
                comparison_cars.remove(car)
            st.session_state.comparison_cars = comparison_cars
            st.rerun()
        
        if st.button("🔄 Clear All", key="clear_all_comparison"):
            st.session_state.comparison_cars = []
            st.rerun()
    
    # Initialize comparison engine
    engine = CarComparisonEngine()
    
    # Tabs for different comparison views
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "🎯 Radar Chart", "💰 Price Analysis", "✨ Features"])
    
    with tab1:
        st.markdown("### 📋 **Quick Comparison Overview**")
        
        # Create comparison matrix
        comparison_df = engine.create_comparison_matrix(comparison_cars)
        
        if not comparison_df.empty:
            st.dataframe(comparison_df, use_container_width=True)
            
            # Highlight recommendations
            st.markdown("### 🎯 **AI Analysis & Recommendations**")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 🏆 **Best For Seniors:**")
                # Find car with highest senior-friendly rating
                best_senior_car = max(comparison_cars, key=lambda x: x.get('senior_friendly_rating', 0))
                st.success(f"**{best_senior_car.get('brand')} {best_senior_car.get('model')}** - {best_senior_car.get('senior_friendly_rating', 'N/A')}/10 rating")
                st.write(f"💡 {best_senior_car.get('why_suitable', 'Highly recommended for senior buyers.')}")
            
            with col2:
                st.markdown("#### 💰 **Best Value:**")
                # Simple value calculation based on features vs price
                best_value_car = comparison_cars[0]  # Simplified
                st.info(f"**{best_value_car.get('brand')} {best_value_car.get('model')}** - Great features for the price")
                st.write(f"💰 Price: {best_value_car.get('price', 'N/A')}")
        
        else:
            st.error("Unable to create comparison matrix. Please try again.")
    
    with tab2:
        st.markdown("### 🎯 **Performance Radar Chart**")
        st.markdown("*Compare cars across multiple criteria*")
        
        radar_chart = engine.create_radar_chart(comparison_cars)
        st.plotly_chart(radar_chart, use_container_width=True)
        
        st.markdown("""
        **How to read this chart:**
        - 🎯 **Larger area** = Better overall performance
        - 🛡️ **Safety Rating** = Higher is safer
        - 👴 **Senior Friendly** = Ease of use for seniors
        - ⛽ **Fuel Efficiency** = Better mileage
        - 💰 **Value for Money** = Features per rupee spent
        """)
    
    with tab3:
        st.markdown("### 💰 **Price Analysis**")
        
        price_chart = engine.create_price_comparison(comparison_cars)
        st.plotly_chart(price_chart, use_container_width=True)
        
        # Price insights
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Find cheapest car
            cheapest_car = min(comparison_cars, key=lambda x: len(x.get('price', '₹999L')))
            st.metric("💚 Most Affordable", 
                     f"{cheapest_car.get('brand', 'N/A')} {cheapest_car.get('model', 'N/A')}", 
                     cheapest_car.get('price', 'N/A'))
        
        with col2:
            # Find most fuel efficient
            most_efficient = comparison_cars[0]  # Simplified
            st.metric("⛽ Most Fuel Efficient", 
                     f"{most_efficient.get('brand', 'N/A')} {most_efficient.get('model', 'N/A')}", 
                     most_efficient.get('fuel_efficiency', 'N/A'))
        
        with col3:
            # Find lowest maintenance
            low_maintenance = next((car for car in comparison_cars if car.get('maintenance_cost') == 'Low'), comparison_cars[0])
            st.metric("🔧 Lowest Maintenance", 
                     f"{low_maintenance.get('brand', 'N/A')} {low_maintenance.get('model', 'N/A')}", 
                     low_maintenance.get('maintenance_cost', 'N/A'))
    
    with tab4:
        st.markdown("### ✨ **Detailed Feature Comparison**")
        
        feature_df = engine.create_feature_comparison(comparison_cars)
        
        if not feature_df.empty:
            st.dataframe(feature_df, use_container_width=True)
            
            # Feature insights
            st.markdown("### 📊 **Feature Analysis**")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 🏆 **Most Feature-Rich**")
                feature_counts = [(len(car.get('key_features', [])), car) for car in comparison_cars]
                most_features = max(feature_counts, key=lambda x: x[0])
                st.success(f"**{most_features[1].get('brand')} {most_features[1].get('model')}** - {most_features[0]} key features")
            
            with col2:
                st.markdown("#### 🔍 **Common Features**")
                # Find features present in all cars
                common_features = set(comparison_cars[0].get('key_features', []))
                for car in comparison_cars[1:]:
                    common_features &= set(car.get('key_features', []))
                
                if common_features:
                    for feature in list(common_features)[:3]:
                        st.write(f"✅ {feature}")
                else:
                    st.write("No common features across all cars")
        
        else:
            st.error("Unable to create feature comparison. Please check car data.")
    
    # Action buttons
    st.markdown("---")
    st.markdown("### 🛠️ **Next Steps**")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("💬 Ask AI Expert", key="ask_ai_about_comparison"):
            st.info("🚧 **AI Chat coming soon!** You'll be able to ask specific questions about these cars.")
    
    with col2:
        if st.button("📄 Export Comparison", key="export_comparison"):
            st.info("🚧 **PDF export coming soon!** You'll be able to download this comparison as a PDF.")
    
    with col3:
        if st.button("🔄 Get New Recommendations", key="new_recommendations"):
            st.session_state.recommendations = []
            st.success("🎯 **Generating fresh recommendations...**")
    
    with col4:
        if st.button("📝 Retake Quiz", key="retake_quiz_comparison"):
            st.session_state.user_preferences = {}
            st.session_state.questionnaire_step = 0
            st.success("🔄 **Starting fresh questionnaire...**")

if __name__ == "__main__":
    display_comparison()