"""
Export and PDF Generation Features for Car Advisor
Generate PDF reports of recommendations, comparisons, and reviews
"""
import streamlit as st
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from datetime import datetime
import io
import base64
from typing import Dict, List, Any
import json

class PDFExporter:
    """PDF export functionality for car recommendations and comparisons"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
    
    def setup_custom_styles(self):
        """Setup custom paragraph styles"""
        # Title style
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Title'],
            fontSize=24,
            spaceAfter=30,
            textColor=colors.darkblue,
            alignment=1  # Center alignment
        )
        
        # Subtitle style
        self.subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=self.styles['Heading1'],
            fontSize=16,
            spaceAfter=12,
            textColor=colors.darkgreen,
        )
        
        # Body style
        self.body_style = ParagraphStyle(
            'CustomBody',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=6,
            leading=14,
        )
        
        # Car name style
        self.car_style = ParagraphStyle(
            'CarName',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=8,
            textColor=colors.darkred,
        )
    
    def generate_recommendations_pdf(self, user_preferences: Dict, recommendations: List[Dict]) -> bytes:
        """Generate PDF report for car recommendations"""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
        
        # Build story (content)
        story = []
        
        # Title
        story.append(Paragraph("🚗 Car Recommendations Report", self.title_style))
        story.append(Spacer(1, 12))
        
        # Generated date
        date_str = datetime.now().strftime("%B %d, %Y at %I:%M %p")
        story.append(Paragraph(f"Generated on: {date_str}", self.styles['Normal']))
        story.append(Spacer(1, 20))
        
        # User preferences summary
        story.append(Paragraph("📋 Your Preferences Summary", self.subtitle_style))
        
        if user_preferences:
            prefs_data = []
            
            if 'budget' in user_preferences:
                budget_min, budget_max = user_preferences['budget']
                prefs_data.append(['Budget Range', f"₹{budget_min:,} - ₹{budget_max:,}"])
            
            if 'primary_use' in user_preferences:
                prefs_data.append(['Primary Use', user_preferences['primary_use']])
            
            if 'family_size' in user_preferences:
                prefs_data.append(['Family Size', user_preferences['family_size']])
            
            if 'fuel_preference' in user_preferences:
                prefs_data.append(['Fuel Preference', user_preferences['fuel_preference']])
            
            if 'driving_experience' in user_preferences:
                prefs_data.append(['Driving Experience', user_preferences['driving_experience']])
            
            if prefs_data:
                prefs_table = Table(prefs_data, colWidths=[2*inch, 3*inch])
                prefs_table.setStyle(TableStyle([
                    ('BACKGROUND', (0,0), (-1,0), colors.grey),
                    ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
                    ('ALIGN', (0,0), (-1,-1), 'LEFT'),
                    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0,0), (-1,0), 12),
                    ('BOTTOMPADDING', (0,0), (-1,0), 12),
                    ('BACKGROUND', (0,1), (-1,-1), colors.beige),
                    ('GRID', (0,0), (-1,-1), 1, colors.black)
                ]))
                story.append(prefs_table)
        
        story.append(Spacer(1, 20))
        
        # Recommendations
        story.append(Paragraph("🎯 AI-Recommended Cars", self.subtitle_style))
        story.append(Spacer(1, 12))
        
        for i, car in enumerate(recommendations, 1):
            # Car header
            car_name = f"{car.get('brand', 'Unknown')} {car.get('model', 'Unknown')}"
            story.append(Paragraph(f"Recommendation #{i}: {car_name}", self.car_style))
            
            # Basic info table
            car_data = [
                ['Price Range', car.get('price', 'Contact dealer')],
                ['Fuel Efficiency', car.get('fuel_efficiency', 'N/A')],
                ['Safety Rating', car.get('safety_rating', 'N/A')],
                ['Senior-Friendly Rating', f"{car.get('senior_friendly_rating', 'N/A')}/10"],
                ['Maintenance Cost', car.get('maintenance_cost', 'N/A')]
            ]
            
            car_table = Table(car_data, colWidths=[1.5*inch, 2.5*inch])
            car_table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (0,-1), colors.lightgrey),
                ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
                ('FONTSIZE', (0,0), (-1,-1), 10),
                ('ALIGN', (0,0), (-1,-1), 'LEFT'),
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('GRID', (0,0), (-1,-1), 0.5, colors.black)
            ]))
            story.append(car_table)
            story.append(Spacer(1, 8))
            
            # Why suitable
            if car.get('why_suitable'):
                story.append(Paragraph("Why This Car Suits You:", ParagraphStyle('Bold', parent=self.body_style, fontName='Helvetica-Bold')))
                story.append(Paragraph(car['why_suitable'], self.body_style))
                story.append(Spacer(1, 8))
            
            # Key features
            if car.get('key_features'):
                story.append(Paragraph("Key Features:", ParagraphStyle('Bold', parent=self.body_style, fontName='Helvetica-Bold')))
                for feature in car['key_features'][:5]:
                    story.append(Paragraph(f"• {feature}", self.body_style))
                story.append(Spacer(1, 8))
            
            # Pros and cons
            if car.get('pros') or car.get('cons'):
                pros_cons_data = []
                max_items = max(len(car.get('pros', [])), len(car.get('cons', [])))
                
                for j in range(max_items):
                    pro = car['pros'][j] if j < len(car.get('pros', [])) else ""
                    con = car['cons'][j] if j < len(car.get('cons', [])) else ""
                    pros_cons_data.append([f"✓ {pro}" if pro else "", f"⚠ {con}" if con else ""])
                
                if pros_cons_data:
                    pros_cons_table = Table([['Pros', 'Considerations']] + pros_cons_data, colWidths=[2*inch, 2*inch])
                    pros_cons_table.setStyle(TableStyle([
                        ('BACKGROUND', (0,0), (-1,0), colors.green),
                        ('BACKGROUND', (1,0), (1,0), colors.orange),
                        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
                        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                        ('FONTSIZE', (0,0), (-1,-1), 9),
                        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
                        ('VALIGN', (0,0), (-1,-1), 'TOP'),
                        ('GRID', (0,0), (-1,-1), 0.5, colors.black)
                    ]))
                    story.append(pros_cons_table)
            
            story.append(Spacer(1, 16))
        
        # Footer with recommendations
        story.append(PageBreak())
        story.append(Paragraph("💡 Additional Recommendations", self.subtitle_style))
        
        recommendations_text = [
            "• Visit authorized dealerships to test drive these recommended cars",
            "• Compare insurance quotes from multiple providers",
            "• Check service center locations in your area before finalizing",
            "• Consider extended warranty options for peace of mind",
            "• Negotiate for accessories and additional services",
            "• Verify all safety features are included in your chosen variant"
        ]
        
        for rec in recommendations_text:
            story.append(Paragraph(rec, self.body_style))
        
        story.append(Spacer(1, 20))
        story.append(Paragraph("Thank you for using Car Advisor! We hope this report helps you make an informed decision.", self.body_style))
        
        # Build PDF
        doc.build(story)
        
        buffer.seek(0)
        return buffer.getvalue()
    
    def generate_comparison_pdf(self, comparison_cars: List[Dict]) -> bytes:
        """Generate PDF report for car comparison"""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
        
        story = []
        
        # Title
        story.append(Paragraph("⚖️ Car Comparison Report", self.title_style))
        story.append(Spacer(1, 12))
        
        # Generated date
        date_str = datetime.now().strftime("%B %d, %Y at %I:%M %p")
        story.append(Paragraph(f"Generated on: {date_str}", self.styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Comparison summary
        story.append(Paragraph(f"Comparing {len(comparison_cars)} Cars", self.subtitle_style))
        
        # Create comparison table
        headers = ['Specification'] + [f"{car.get('brand', 'Unknown')} {car.get('model', 'Unknown')}" for car in comparison_cars]
        
        comparison_data = [headers]
        
        # Add rows for different specifications
        specs = [
            ('Price Range', 'price'),
            ('Fuel Efficiency', 'fuel_efficiency'),
            ('Safety Rating', 'safety_rating'),
            ('Senior-Friendly Rating', lambda x: f"{x.get('senior_friendly_rating', 'N/A')}/10"),
            ('Maintenance Cost', 'maintenance_cost')
        ]
        
        for spec_name, spec_key in specs:
            row = [spec_name]
            for car in comparison_cars:
                if callable(spec_key):
                    value = spec_key(car)
                else:
                    value = car.get(spec_key, 'N/A')
                row.append(str(value))
            comparison_data.append(row)
        
        # Create and style the table
        comparison_table = Table(comparison_data, colWidths=[1.5*inch] + [1.5*inch] * len(comparison_cars))
        comparison_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.darkblue),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,-1), 9),
            ('BOTTOMPADDING', (0,0), (-1,0), 12),
            ('BACKGROUND', (0,1), (0,-1), colors.lightgrey),
            ('GRID', (0,0), (-1,-1), 1, colors.black)
        ]))
        
        story.append(comparison_table)
        story.append(Spacer(1, 20))
        
        # Detailed comparison for each car
        for i, car in enumerate(comparison_cars, 1):
            story.append(Paragraph(f"Car {i}: {car.get('brand', 'Unknown')} {car.get('model', 'Unknown')}", self.car_style))
            
            if car.get('why_suitable'):
                story.append(Paragraph("Why Suitable:", ParagraphStyle('Bold', parent=self.body_style, fontName='Helvetica-Bold')))
                story.append(Paragraph(car['why_suitable'], self.body_style))
                story.append(Spacer(1, 8))
            
            # Features comparison
            if car.get('key_features'):
                story.append(Paragraph("Key Features:", ParagraphStyle('Bold', parent=self.body_style, fontName='Helvetica-Bold')))
                for feature in car['key_features'][:5]:
                    story.append(Paragraph(f"• {feature}", self.body_style))
                story.append(Spacer(1, 12))
        
        # Build PDF
        doc.build(story)
        
        buffer.seek(0)
        return buffer.getvalue()

def create_download_link(pdf_bytes: bytes, filename: str) -> str:
    """Create download link for PDF"""
    b64_pdf = base64.b64encode(pdf_bytes).decode()
    href = f'<a href="data:application/pdf;base64,{b64_pdf}" download="{filename}" target="_blank">📄 Download {filename}</a>'
    return href

def display_export_features():
    """Display export and sharing features"""
    st.markdown("## 📄 Export & Share")
    st.markdown("### *Download your recommendations and comparisons as PDF reports*")
    
    # Initialize PDF exporter
    exporter = PDFExporter()
    
    # Check what's available to export
    user_preferences = st.session_state.get('user_preferences', {})
    recommendations = st.session_state.get('recommendations', [])
    comparison_cars = st.session_state.get('comparison_cars', [])
    
    # Export options
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🎯 **Recommendations Report**")
        
        if recommendations and user_preferences:
            st.success(f"✅ **Ready to export {len(recommendations)} recommendations**")
            
            if st.button("📄 Generate Recommendations PDF", key="export_recommendations"):
                with st.spinner("🔄 **Generating PDF report...**"):
                    try:
                        pdf_bytes = exporter.generate_recommendations_pdf(user_preferences, recommendations)
                        filename = f"car_recommendations_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
                        
                        # Create download link
                        st.success("✅ **PDF generated successfully!**")
                        st.markdown(create_download_link(pdf_bytes, filename), unsafe_allow_html=True)
                        
                        st.info("""
                        **📋 Your PDF includes:**
                        - Your questionnaire preferences summary
                        - Detailed car recommendations with ratings
                        - Why each car suits your needs
                        - Pros and cons for each recommendation
                        - Additional buying tips and recommendations
                        """)
                        
                    except Exception as e:
                        st.error(f"❌ **Failed to generate PDF**: {str(e)}")
        else:
            st.warning("⚠️ **Complete the questionnaire and get recommendations first**")
            
            if st.button("📝 Go to Questionnaire", key="goto_quiz_export"):
                st.session_state.questionnaire_step = 0
                st.rerun()
    
    with col2:
        st.markdown("### ⚖️ **Comparison Report**")
        
        if comparison_cars:
            st.success(f"✅ **Ready to export comparison of {len(comparison_cars)} cars**")
            
            if st.button("📄 Generate Comparison PDF", key="export_comparison"):
                with st.spinner("🔄 **Generating comparison PDF...**"):
                    try:
                        pdf_bytes = exporter.generate_comparison_pdf(comparison_cars)
                        filename = f"car_comparison_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
                        
                        # Create download link
                        st.success("✅ **PDF generated successfully!**")
                        st.markdown(create_download_link(pdf_bytes, filename), unsafe_allow_html=True)
                        
                        st.info("""
                        **📋 Your PDF includes:**
                        - Side-by-side specification comparison
                        - Detailed analysis of each car
                        - Feature comparison matrix
                        - Pros and cons for each car
                        - Recommendation summary
                        """)
                        
                    except Exception as e:
                        st.error(f"❌ **Failed to generate PDF**: {str(e)}")
        else:
            st.warning("⚠️ **Add cars to comparison first**")
            
            if st.button("⚖️ Go to Comparison", key="goto_comparison_export"):
                st.rerun()
    
    # Additional export options
    st.markdown("---")
    st.markdown("### 📤 **Additional Export Options**")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 💬 **Chat History**")
        chat_history = st.session_state.get('chat_history', [])
        
        if chat_history:
            if st.button("📄 Export Chat as Text", key="export_chat"):
                # Create text export of chat history
                chat_text = "Car Advisor - Chat History\n"
                chat_text += f"Generated on: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}\n"
                chat_text += "=" * 50 + "\n\n"
                
                for i, chat in enumerate(chat_history, 1):
                    chat_text += f"Question {i}:\n{chat['user']}\n\n"
                    chat_text += f"AI Expert Response:\n{chat['assistant']}\n\n"
                    chat_text += "-" * 30 + "\n\n"
                
                # Create download link for text
                b64_text = base64.b64encode(chat_text.encode()).decode()
                filename = f"chat_history_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
                href = f'<a href="data:text/plain;base64,{b64_text}" download="{filename}">📄 Download Chat History</a>'
                
                st.success("✅ **Chat history ready for download!**")
                st.markdown(href, unsafe_allow_html=True)
        else:
            st.info("💬 No chat history available")
    
    with col2:
        st.markdown("#### 🔗 **Share Options**")
        st.info("🚧 **Coming Soon:**")
        st.write("• Email recommendations")
        st.write("• Share via WhatsApp")
        st.write("• Generate shareable links")
        
        if st.button("📧 Email Features", key="email_features", disabled=True):
            st.info("📧 Email functionality will be available in the next update!")
    
    with col3:
        st.markdown("#### 📊 **Data Export**")
        st.info("🚧 **Coming Soon:**")
        st.write("• Export as Excel/CSV")
        st.write("• JSON data format")
        st.write("• Import/Export preferences")
        
        if st.button("📊 Data Export", key="data_export", disabled=True):
            st.info("📊 Data export functionality will be available in the next update!")
    
    # Tips and information
    st.markdown("---")
    st.markdown("### 💡 **Export Tips**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **📄 PDF Features:**
        - 📱 **Mobile-friendly** - Easy to read on any device
        - 🖨️ **Print-ready** - High-quality printing layout
        - 📧 **Shareable** - Easy to email to family/friends
        - 💾 **Offline access** - No internet required to view
        """)
    
    with col2:
        st.markdown("""
        **🎯 Best Practices:**
        - 📝 **Complete questionnaire** for personalized reports
        - ⚖️ **Compare multiple cars** before exporting
        - 💬 **Use AI chat** to clarify doubts first
        - 🔄 **Update reports** as preferences change
        """)

if __name__ == "__main__":
    display_export_features()