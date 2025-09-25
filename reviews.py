"""
Review System for Car Advisor
User reviews, ratings, and AI-powered analysis
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time
from typing import Dict, List, Any
import json
import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ReviewSystem:
    """Car review and rating system"""
    
    def __init__(self):
        self.client = None
        self._initialize_openai()
        self.review_categories = [
            "Overall Experience",
            "Comfort & Interior", 
            "Performance & Driving",
            "Fuel Efficiency",
            "Safety Features",
            "Ease of Use",
            "Value for Money",
            "Service & Maintenance"
        ]
        self.sample_reviews = self._load_sample_reviews()
    
    def _initialize_openai(self):
        """Initialize OpenAI client for review analysis"""
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            try:
                self.client = openai.OpenAI(api_key=api_key)
            except Exception as e:
                st.error(f"Failed to initialize OpenAI for review analysis: {str(e)}")
    
    def _load_sample_reviews(self) -> List[Dict[str, Any]]:
        """Load sample reviews for demonstration"""
        return [
            {
                "id": 1,
                "car_brand": "Maruti Suzuki",
                "car_model": "Swift",
                "reviewer_name": "Rajesh Kumar (62 years)",
                "rating": 4.5,
                "review_text": "Excellent car for senior citizens! Very easy to drive and park. The automatic variant is perfect for city traffic. Service network is outstanding - I can get it serviced anywhere in India. Fuel efficiency is amazing, giving me 18+ kmpl in city. Only complaint is that rear seat could be more spacious.",
                "pros": ["Excellent fuel efficiency", "Easy to drive", "Wide service network", "Compact size for parking"],
                "cons": ["Limited rear space", "Road noise on highways"],
                "category_ratings": {
                    "Overall Experience": 4.5,
                    "Comfort & Interior": 4.0,
                    "Performance & Driving": 4.5, 
                    "Fuel Efficiency": 5.0,
                    "Safety Features": 4.0,
                    "Ease of Use": 5.0,
                    "Value for Money": 4.5,
                    "Service & Maintenance": 5.0
                },
                "date": datetime.now() - timedelta(days=15),
                "verified": True,
                "helpful_votes": 23,
                "senior_recommended": True
            },
            {
                "id": 2,
                "car_brand": "Honda",
                "car_model": "City",
                "reviewer_name": "Sunita Sharma (68 years)",
                "rating": 4.8,
                "review_text": "Bought this for my retirement years and absolutely loving it! The CVT automatic transmission is so smooth - no jerks at all. Rear seat is very comfortable for passengers. Build quality feels premium and solid. AC cools very well. The only issue is that it's slightly expensive compared to others, but the refinement justifies the price.",
                "pros": ["Smooth CVT transmission", "Excellent build quality", "Spacious interior", "Premium feel"],
                "cons": ["Higher price", "Slightly expensive maintenance"],
                "category_ratings": {
                    "Overall Experience": 4.8,
                    "Comfort & Interior": 5.0,
                    "Performance & Driving": 4.5,
                    "Fuel Efficiency": 4.5,
                    "Safety Features": 4.8,
                    "Ease of Use": 4.8,
                    "Value for Money": 4.0,
                    "Service & Maintenance": 4.5
                },
                "date": datetime.now() - timedelta(days=8),
                "verified": True,
                "helpful_votes": 31,
                "senior_recommended": True
            },
            {
                "id": 3,
                "car_brand": "Hyundai",
                "car_model": "Creta",
                "reviewer_name": "Ashok Mehta (65 years)",
                "rating": 4.3,
                "review_text": "Good SUV for senior citizens. High seating position makes it easy to get in and out - very important for people with joint issues. Visibility is excellent from driver seat. Loaded with features and safety systems. However, the ride is a bit firm on bad roads and fuel efficiency could be better for city driving.",
                "pros": ["High seating position", "Easy entry/exit", "Feature loaded", "Good safety"],
                "cons": ["Firm ride quality", "Lower city fuel efficiency"],
                "category_ratings": {
                    "Overall Experience": 4.3,
                    "Comfort & Interior": 4.5,
                    "Performance & Driving": 4.2,
                    "Fuel Efficiency": 3.8,
                    "Safety Features": 4.8,
                    "Ease of Use": 4.5,
                    "Value for Money": 4.2,
                    "Service & Maintenance": 4.0
                },
                "date": datetime.now() - timedelta(days=22),
                "verified": True,
                "helpful_votes": 18,
                "senior_recommended": True
            },
            {
                "id": 4,
                "car_brand": "Toyota",
                "car_model": "Innova Crysta",
                "reviewer_name": "Dr. Ramesh Gupta (71 years)",
                "rating": 4.9,
                "review_text": "Purchased this for our large joint family and it's been fantastic! Extremely reliable - never had any major issues in 2 years. Very comfortable for long drives to visit relatives. All 7 seats are usable and comfortable. Maintenance cost is reasonable considering the build quality. Highly recommend for senior families who prioritize reliability over everything else.",
                "pros": ["Ultra reliable", "Spacious 7-seater", "Comfortable long drives", "Strong build quality"],
                "cons": ["Higher fuel consumption", "Premium price point"],
                "category_ratings": {
                    "Overall Experience": 4.9,
                    "Comfort & Interior": 4.8,
                    "Performance & Driving": 4.5,
                    "Fuel Efficiency": 3.5,
                    "Safety Features": 4.8,
                    "Ease of Use": 4.5,
                    "Value for Money": 4.5,
                    "Service & Maintenance": 5.0
                },
                "date": datetime.now() - timedelta(days=30),
                "verified": True,
                "helpful_votes": 45,
                "senior_recommended": True
            },
            {
                "id": 5,
                "car_brand": "Tata",
                "car_model": "Nexon",
                "reviewer_name": "Priya Nair (63 years)",
                "rating": 4.1,
                "review_text": "Bought this after reading about its 5-star safety rating. As a single senior woman, safety was my top priority. The car feels very solid and well-built. Modern features like touchscreen and reverse camera are helpful. However, the engine is a bit noisy and rear seat space is just adequate for my grandchildren visits.",
                "pros": ["Excellent safety rating", "Solid build quality", "Modern features", "Good value"],
                "cons": ["Engine noise", "Limited rear space"],
                "category_ratings": {
                    "Overall Experience": 4.1,
                    "Comfort & Interior": 3.8,
                    "Performance & Driving": 4.0,
                    "Fuel Efficiency": 4.2,
                    "Safety Features": 5.0,
                    "Ease of Use": 4.0,
                    "Value for Money": 4.5,
                    "Service & Maintenance": 4.0
                },
                "date": datetime.now() - timedelta(days=12),
                "verified": True,
                "helpful_votes": 27,
                "senior_recommended": True
            }
        ]
    
    def add_review(self, review_data: Dict[str, Any]) -> bool:
        """Add a new review to the system"""
        try:
            # In a real app, this would save to database
            if 'reviews' not in st.session_state:
                st.session_state.reviews = []
            
            # Add review ID and timestamp
            review_data['id'] = len(st.session_state.reviews) + len(self.sample_reviews) + 1
            review_data['date'] = datetime.now()
            review_data['helpful_votes'] = 0
            review_data['verified'] = False  # Would need verification process
            
            st.session_state.reviews.append(review_data)
            return True
        except Exception as e:
            st.error(f"Failed to add review: {str(e)}")
            return False
    
    def get_all_reviews(self) -> List[Dict[str, Any]]:
        """Get all reviews (sample + user reviews)"""
        user_reviews = st.session_state.get('reviews', [])
        all_reviews = self.sample_reviews + user_reviews
        return sorted(all_reviews, key=lambda x: x['date'], reverse=True)
    
    def get_car_reviews(self, brand: str, model: str) -> List[Dict[str, Any]]:
        """Get reviews for a specific car"""
        all_reviews = self.get_all_reviews()
        return [r for r in all_reviews if r['car_brand'].lower() == brand.lower() and r['car_model'].lower() == model.lower()]
    
    def calculate_average_rating(self, reviews: List[Dict[str, Any]]) -> Dict[str, float]:
        """Calculate average ratings from reviews"""
        if not reviews:
            return {}
        
        total_reviews = len(reviews)
        overall_rating = sum(r['rating'] for r in reviews) / total_reviews
        
        # Calculate category averages
        category_averages = {}
        for category in self.review_categories:
            ratings = [r['category_ratings'][category] for r in reviews if category in r.get('category_ratings', {})]
            if ratings:
                category_averages[category] = sum(ratings) / len(ratings)
        
        return {
            'overall': overall_rating,
            'total_reviews': total_reviews,
            'categories': category_averages
        }
    
    def analyze_review_sentiment(self, review_text: str) -> Dict[str, Any]:
        """Analyze review sentiment using AI"""
        if not self.client:
            return {"sentiment": "neutral", "confidence": 0.5, "summary": "Analysis unavailable"}
        
        try:
            prompt = f"""Analyze the sentiment of this car review and provide insights:

Review: "{review_text}"

Please provide:
1. Sentiment (positive/negative/neutral)
2. Confidence score (0-1)
3. Key insights for senior car buyers
4. Summary of main points

Format as JSON."""
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert at analyzing car reviews for senior buyers."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.3
            )
            
            # Parse response (simplified)
            analysis = {
                "sentiment": "positive" if "positive" in response.choices[0].message.content.lower() else "neutral",
                "confidence": 0.8,
                "summary": "AI analysis completed"
            }
            
            return analysis
            
        except Exception as e:
            return {"sentiment": "neutral", "confidence": 0.5, "summary": f"Analysis failed: {str(e)}"}

def display_reviews():
    """Main function to display review system"""
    st.markdown("## ⭐ Reviews & Ratings")
    st.markdown("### *Real experiences from senior car buyers*")
    
    # Initialize review system
    review_system = ReviewSystem()
    
    # Tabs for different review sections
    tab1, tab2, tab3, tab4 = st.tabs(["📖 Browse Reviews", "✍️ Write Review", "📊 Rating Analytics", "🔍 Search Reviews"])
    
    with tab1:
        display_browse_reviews(review_system)
    
    with tab2:
        display_write_review(review_system)
    
    with tab3:
        display_rating_analytics(review_system)
    
    with tab4:
        display_search_reviews(review_system)

def display_browse_reviews(review_system: ReviewSystem):
    """Display browse reviews interface"""
    st.markdown("### 📖 **Browse Car Reviews**")
    
    all_reviews = review_system.get_all_reviews()
    
    # Filter options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        brands = sorted(list(set(r['car_brand'] for r in all_reviews)))
        selected_brand = st.selectbox("Filter by Brand", ["All Brands"] + brands)
    
    with col2:
        if selected_brand != "All Brands":
            models = sorted(list(set(r['car_model'] for r in all_reviews if r['car_brand'] == selected_brand)))
            selected_model = st.selectbox("Filter by Model", ["All Models"] + models)
        else:
            selected_model = "All Models"
    
    with col3:
        rating_filter = st.selectbox("Minimum Rating", ["All Ratings", "4+ Stars", "3+ Stars"])
    
    # Apply filters
    filtered_reviews = all_reviews
    
    if selected_brand != "All Brands":
        filtered_reviews = [r for r in filtered_reviews if r['car_brand'] == selected_brand]
    
    if selected_model != "All Models":
        filtered_reviews = [r for r in filtered_reviews if r['car_model'] == selected_model]
    
    if rating_filter == "4+ Stars":
        filtered_reviews = [r for r in filtered_reviews if r['rating'] >= 4.0]
    elif rating_filter == "3+ Stars":
        filtered_reviews = [r for r in filtered_reviews if r['rating'] >= 3.0]
    
    # Display results
    st.markdown(f"**Showing {len(filtered_reviews)} reviews**")
    
    if not filtered_reviews:
        st.info("🔍 **No reviews found matching your filters. Try adjusting the filters above.**")
        return
    
    # Display reviews
    for review in filtered_reviews:
        with st.container():
            # Review header
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                st.markdown(f"### 🚗 **{review['car_brand']} {review['car_model']}**")
                st.markdown(f"👤 **{review['reviewer_name']}**")
            
            with col2:
                # Rating display
                stars = "⭐" * int(review['rating']) + "☆" * (5 - int(review['rating']))
                st.markdown(f"**Rating:** {stars} ({review['rating']}/5)")
                
                if review.get('verified'):
                    st.success("✅ Verified Purchase")
            
            with col3:
                days_ago = (datetime.now() - review['date']).days
                st.markdown(f"📅 **{days_ago} days ago**")
                st.markdown(f"👍 **{review['helpful_votes']} helpful**")
            
            # Review content
            st.markdown("**📝 Review:**")
            st.write(review['review_text'])
            
            # Pros and cons
            col1, col2 = st.columns(2)
            
            with col1:
                if review.get('pros'):
                    st.markdown("**👍 Pros:**")
                    for pro in review['pros']:
                        st.markdown(f"✅ {pro}")
            
            with col2:
                if review.get('cons'):
                    st.markdown("**👎 Considerations:**")
                    for con in review['cons']:
                        st.markdown(f"⚠️ {con}")
            
            # Senior recommendation badge
            if review.get('senior_recommended'):
                st.success("🏆 **Recommended for Senior Buyers**")
            
            # Category ratings (if available)
            if review.get('category_ratings'):
                with st.expander("📊 Detailed Category Ratings"):
                    for category, rating in review['category_ratings'].items():
                        progress = rating / 5.0
                        st.progress(progress, text=f"{category}: {rating}/5")
            
            # Action buttons
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button(f"👍 Helpful", key=f"helpful_{review['id']}"):
                    st.success("✅ **Thank you for your feedback!**")
            
            with col2:
                if st.button(f"💬 Discuss", key=f"discuss_{review['id']}"):
                    st.info("🚧 **Discussion feature coming soon!**")
            
            with col3:
                if st.button(f"📤 Share", key=f"share_{review['id']}"):
                    st.info("🚧 **Share feature coming soon!**")
            
            st.markdown("---")

def display_write_review(review_system: ReviewSystem):
    """Display write review interface"""
    st.markdown("### ✍️ **Share Your Car Experience**")
    st.markdown("*Help fellow senior buyers make informed decisions*")
    
    # Review form
    with st.form("write_review_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            car_brand = st.selectbox("Car Brand*", [
                "Maruti Suzuki", "Hyundai", "Tata", "Honda", "Toyota", "Mahindra", 
                "Kia", "MG Motor", "Volkswagen", "Skoda", "BMW", "Mercedes-Benz", "Other"
            ])
        
        with col2:
            car_model = st.text_input("Car Model*", placeholder="e.g., Swift, City, Creta")
        
        # Reviewer details
        reviewer_name = st.text_input("Your Name (optional)", placeholder="e.g., Rajesh Kumar (65 years)")
        
        # Overall rating
        st.markdown("**Overall Rating***")
        overall_rating = st.slider("Rate your overall experience", 1.0, 5.0, 4.0, 0.1)
        
        # Category ratings
        st.markdown("**Detailed Category Ratings** (optional)")
        category_ratings = {}
        
        col1, col2 = st.columns(2)
        
        with col1:
            category_ratings["Comfort & Interior"] = st.slider("Comfort & Interior", 1.0, 5.0, 4.0, 0.1, key="comfort")
            category_ratings["Performance & Driving"] = st.slider("Performance & Driving", 1.0, 5.0, 4.0, 0.1, key="performance")
            category_ratings["Fuel Efficiency"] = st.slider("Fuel Efficiency", 1.0, 5.0, 4.0, 0.1, key="fuel")
            category_ratings["Safety Features"] = st.slider("Safety Features", 1.0, 5.0, 4.0, 0.1, key="safety")
        
        with col2:
            category_ratings["Ease of Use"] = st.slider("Ease of Use", 1.0, 5.0, 4.0, 0.1, key="ease")
            category_ratings["Value for Money"] = st.slider("Value for Money", 1.0, 5.0, 4.0, 0.1, key="value")
            category_ratings["Service & Maintenance"] = st.slider("Service & Maintenance", 1.0, 5.0, 4.0, 0.1, key="service")
        
        # Review text
        review_text = st.text_area(
            "Your Review*",
            placeholder="Share your experience with this car. What do you like? What could be better? How is it for senior drivers?",
            height=150
        )
        
        # Pros and cons
        col1, col2 = st.columns(2)
        
        with col1:
            pros_text = st.text_area("Main Advantages", placeholder="List the best things about this car (one per line)", height=100)
        
        with col2:
            cons_text = st.text_area("Areas for Improvement", placeholder="List any drawbacks or areas for improvement (one per line)", height=100)
        
        # Senior recommendation
        senior_recommended = st.checkbox("Would you recommend this car to other senior buyers?", value=True)
        
        # Submit button
        submitted = st.form_submit_button("📤 Submit Review")
        
        if submitted:
            # Validate required fields
            if not car_brand or not car_model or not review_text:
                st.error("❌ **Please fill in all required fields (marked with *)**")
            else:
                # Process pros and cons
                pros = [p.strip() for p in pros_text.split('\n') if p.strip()] if pros_text else []
                cons = [c.strip() for c in cons_text.split('\n') if c.strip()] if cons_text else []
                
                # Create review data
                review_data = {
                    "car_brand": car_brand,
                    "car_model": car_model,
                    "reviewer_name": reviewer_name or "Anonymous Senior Buyer",
                    "rating": overall_rating,
                    "review_text": review_text,
                    "pros": pros,
                    "cons": cons,
                    "category_ratings": category_ratings,
                    "senior_recommended": senior_recommended
                }
                
                # Add review
                if review_system.add_review(review_data):
                    st.success("✅ **Thank you! Your review has been submitted successfully.**")
                    st.balloons()
                    
                    # Show what happens next
                    st.info("""
                    **What happens next:**
                    - Your review will be published immediately
                    - Other senior buyers can see and find it helpful
                    - You can view it in the 'Browse Reviews' section
                    - Thank you for helping the senior car buying community!
                    """)
                else:
                    st.error("❌ **Failed to submit review. Please try again.**")

def display_rating_analytics(review_system: ReviewSystem):
    """Display rating analytics and insights"""
    st.markdown("### 📊 **Rating Analytics & Insights**")
    
    all_reviews = review_system.get_all_reviews()
    
    if not all_reviews:
        st.info("📊 **No reviews available for analysis yet.**")
        return
    
    # Overall statistics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_reviews = len(all_reviews)
        st.metric("Total Reviews", total_reviews)
    
    with col2:
        avg_rating = sum(r['rating'] for r in all_reviews) / len(all_reviews)
        st.metric("Average Rating", f"{avg_rating:.1f}⭐")
    
    with col3:
        senior_recommended = len([r for r in all_reviews if r.get('senior_recommended', False)])
        st.metric("Senior Recommended", f"{senior_recommended}/{total_reviews}")
    
    with col4:
        verified_reviews = len([r for r in all_reviews if r.get('verified', False)])
        st.metric("Verified Reviews", f"{verified_reviews}/{total_reviews}")
    
    # Brand-wise analysis
    st.markdown("---")
    st.markdown("### 🏆 **Brand-wise Performance**")
    
    # Calculate brand averages
    brand_data = {}
    for review in all_reviews:
        brand = review['car_brand']
        if brand not in brand_data:
            brand_data[brand] = {'ratings': [], 'count': 0}
        brand_data[brand]['ratings'].append(review['rating'])
        brand_data[brand]['count'] += 1
    
    # Create brand comparison chart
    brands = []
    avg_ratings = []
    review_counts = []
    
    for brand, data in brand_data.items():
        if data['count'] >= 1:  # Only show brands with at least 1 review
            brands.append(brand)
            avg_ratings.append(sum(data['ratings']) / len(data['ratings']))
            review_counts.append(data['count'])
    
    if brands:
        # Rating chart
        fig_rating = px.bar(
            x=brands,
            y=avg_ratings,
            title="Average Rating by Brand",
            labels={'x': 'Brand', 'y': 'Average Rating'},
            color=avg_ratings,
            color_continuous_scale='RdYlGn'
        )
        fig_rating.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig_rating, use_container_width=True)
        
        # Review count chart
        fig_count = px.pie(
            values=review_counts,
            names=brands,
            title="Review Distribution by Brand"
        )
        fig_count.update_layout(height=400)
        st.plotly_chart(fig_count, use_container_width=True)
    
    # Category-wise analysis
    st.markdown("---")
    st.markdown("### 🎯 **Category Performance Analysis**")
    
    # Calculate category averages across all reviews
    category_stats = {}
    for category in review_system.review_categories:
        ratings = []
        for review in all_reviews:
            if category in review.get('category_ratings', {}):
                ratings.append(review['category_ratings'][category])
        
        if ratings:
            category_stats[category] = {
                'average': sum(ratings) / len(ratings),
                'count': len(ratings)
            }
    
    if category_stats:
        categories = list(category_stats.keys())
        averages = [category_stats[cat]['average'] for cat in categories]
        
        # Category radar chart
        fig_radar = go.Figure()
        
        fig_radar.add_trace(go.Scatterpolar(
            r=averages,
            theta=categories,
            fill='toself',
            name='Average Ratings',
            line_color='#1f77b4'
        ))
        
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 5]
                )),
            showlegend=False,
            title="Average Performance by Category",
            height=500
        )
        
        st.plotly_chart(fig_radar, use_container_width=True)
        
        # Top and bottom performing categories
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🏆 **Strongest Categories**")
            sorted_cats = sorted(category_stats.items(), key=lambda x: x[1]['average'], reverse=True)
            for i, (cat, stats) in enumerate(sorted_cats[:3]):
                st.write(f"{i+1}. **{cat}**: {stats['average']:.1f}⭐ ({stats['count']} reviews)")
        
        with col2:
            st.markdown("#### 📈 **Areas for Improvement**")
            for i, (cat, stats) in enumerate(sorted_cats[-3:]):
                st.write(f"{i+1}. **{cat}**: {stats['average']:.1f}⭐ ({stats['count']} reviews)")

def display_search_reviews(review_system: ReviewSystem):
    """Display search and filter reviews interface"""
    st.markdown("### 🔍 **Search & Filter Reviews**")
    
    all_reviews = review_system.get_all_reviews()
    
    # Search interface
    col1, col2 = st.columns([2, 1])
    
    with col1:
        search_query = st.text_input("🔍 Search reviews", placeholder="e.g., 'automatic transmission', 'fuel efficiency', 'senior friendly'")
    
    with col2:
        search_in = st.selectbox("Search in", ["Review Text", "Pros & Cons", "All Fields"])
    
    # Advanced filters
    with st.expander("🔧 Advanced Filters"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            min_rating = st.slider("Minimum Rating", 1.0, 5.0, 1.0, 0.1)
            max_rating = st.slider("Maximum Rating", 1.0, 5.0, 5.0, 0.1)
        
        with col2:
            date_range = st.selectbox("Review Age", ["All Time", "Last 7 days", "Last 30 days", "Last 90 days"])
            verified_only = st.checkbox("Verified reviews only")
        
        with col3:
            senior_recommended_only = st.checkbox("Senior recommended only")
            sort_by = st.selectbox("Sort by", ["Newest First", "Oldest First", "Highest Rating", "Lowest Rating", "Most Helpful"])
    
    # Apply filters
    filtered_reviews = all_reviews.copy()
    
    # Text search
    if search_query:
        search_query = search_query.lower()
        if search_in == "Review Text":
            filtered_reviews = [r for r in filtered_reviews if search_query in r['review_text'].lower()]
        elif search_in == "Pros & Cons":
            filtered_reviews = [r for r in filtered_reviews if 
                              any(search_query in pro.lower() for pro in r.get('pros', [])) or
                              any(search_query in con.lower() for con in r.get('cons', []))]
        else:  # All Fields
            filtered_reviews = [r for r in filtered_reviews if 
                              search_query in r['review_text'].lower() or
                              search_query in r['car_brand'].lower() or
                              search_query in r['car_model'].lower() or
                              any(search_query in pro.lower() for pro in r.get('pros', [])) or
                              any(search_query in con.lower() for con in r.get('cons', []))]
    
    # Rating filter
    filtered_reviews = [r for r in filtered_reviews if min_rating <= r['rating'] <= max_rating]
    
    # Date filter
    if date_range != "All Time":
        days_map = {"Last 7 days": 7, "Last 30 days": 30, "Last 90 days": 90}
        cutoff_date = datetime.now() - timedelta(days=days_map[date_range])
        filtered_reviews = [r for r in filtered_reviews if r['date'] >= cutoff_date]
    
    # Other filters
    if verified_only:
        filtered_reviews = [r for r in filtered_reviews if r.get('verified', False)]
    
    if senior_recommended_only:
        filtered_reviews = [r for r in filtered_reviews if r.get('senior_recommended', False)]
    
    # Sort results
    if sort_by == "Newest First":
        filtered_reviews.sort(key=lambda x: x['date'], reverse=True)
    elif sort_by == "Oldest First":
        filtered_reviews.sort(key=lambda x: x['date'])
    elif sort_by == "Highest Rating":
        filtered_reviews.sort(key=lambda x: x['rating'], reverse=True)
    elif sort_by == "Lowest Rating":
        filtered_reviews.sort(key=lambda x: x['rating'])
    elif sort_by == "Most Helpful":
        filtered_reviews.sort(key=lambda x: x['helpful_votes'], reverse=True)
    
    # Display results
    st.markdown(f"**Found {len(filtered_reviews)} reviews matching your criteria**")
    
    if not filtered_reviews:
        st.info("🔍 **No reviews found. Try adjusting your search criteria.**")
        return
    
    # Display search results (simplified view)
    for review in filtered_reviews[:10]:  # Show first 10 results
        with st.container():
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"**🚗 {review['car_brand']} {review['car_model']}** - ⭐ {review['rating']}/5")
                
                # Highlight search terms in review text
                display_text = review['review_text'][:200] + "..." if len(review['review_text']) > 200 else review['review_text']
                if search_query:
                    # Simple highlighting (in a real app, you'd use more sophisticated highlighting)
                    display_text = display_text.replace(search_query, f"**{search_query}**")
                
                st.write(f"👤 {review['reviewer_name']}: {display_text}")
            
            with col2:
                days_ago = (datetime.now() - review['date']).days
                st.write(f"📅 {days_ago} days ago")
                
                if review.get('verified'):
                    st.success("✅ Verified")
                
                if review.get('senior_recommended'):
                    st.info("🏆 Senior Rec.")
            
            st.markdown("---")
    
    if len(filtered_reviews) > 10:
        st.info(f"📄 **Showing first 10 of {len(filtered_reviews)} results. Refine your search to see more specific results.**")

if __name__ == "__main__":
    display_reviews()