"""
Main entry point for the Fitness Tracker Streamlit application.
"""
import streamlit as st
import sys
from pathlib import Path

# Import configuration
from config import APP_TITLE, APP_LAYOUT

# Import database setup
sys.path.insert(0, str(Path(__file__).parent))
from database.db_manager import db_manager
from database.schema import init_schema

# Import services
from services.student_service import StudentService
from services.activity_service import ActivityService
from services.analytics_service import AnalyticsService

# Import utilities
from utils.sample_data import load_sample_data

# Initialize database schema
init_schema()

# Streamlit page configuration
st.set_page_config(
    page_title=APP_TITLE,
    layout=APP_LAYOUT,
    page_icon="🏃",
    initial_sidebar_state="expanded"
)

# Add CSS for mobile responsiveness and better UI
st.markdown("""
<style>
    /* Mobile responsive adjustments */
    @media (max-width: 768px) {
        .stApp {
            max-width: 100%;
        }
        
        .stButton>button {
            width: 100%;
        }
        
        .stSelectbox>div {
            width: 100%;
        }
        
        .element-container {
            padding: 0.5rem 0;
        }
    }
    
    /* Custom styling for better appearance */
    .achievement-card {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 10px;
    }
    
    .metric-container {
        padding: 10px;
        border-radius: 5px;
        background-color: #f0f2f6;
        margin-bottom: 10px;
        text-align: center;
    }
    
    /* Gamification elements */
    .badge {
        display: inline-block;
        border-radius: 50%;
        width: 60px;
        height: 60px;
        line-height: 60px;
        text-align: center;
        background-color: #4CAF50;
        color: white;
        margin: 5px;
    }
    
    .badge-locked {
        background-color: #9e9e9e;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for various features
if 'points' not in st.session_state:
    st.session_state.points = 0

if 'achievements' not in st.session_state:
    st.session_state.achievements = []

# Main page content
st.title(APP_TITLE)
st.markdown("Welcome to the Fitness Tracker App! Use the sidebar to navigate through different pages.")

# Home page content
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Getting Started")
    st.markdown("""
    This application helps track and visualize fitness progress for students.
    
    **Key Features:**
    - Track steps, active minutes, and other fitness metrics
    - Visualize progress with interactive charts
    - Set fitness goals and track achievements
    - Get personalized recommendations
    - Earn points and badges for consistent activity
    """)

with col2:
    st.subheader("Quick Actions")
    if st.button("Load Sample Data"):
        num_students = load_sample_data()
        st.success(f"Sample data loaded for {num_students} students!")
    
    st.markdown("---")
    st.subheader("Gamification")
    st.markdown(f"**Current Points:** {st.session_state.points}")
    
    # Simple achievement badges
    st.markdown("**Badges:**")
    badges_html = """
    <div style="display: flex; flex-wrap: wrap; justify-content: center;">
        <div class="badge">🏆</div>
        <div class="badge badge-locked">🏅</div>
        <div class="badge badge-locked">🎯</div>
    </div>
    """
    st.markdown(badges_html, unsafe_allow_html=True)

# Sidebar info
with st.sidebar:
    st.subheader("About")
    st.info("Navigate through the pages using the menu above.")
    
    st.markdown("---")
    st.subheader("Features")
    st.markdown("✅ Student Management")
    st.markdown("✅ Activity Logging")
    st.markdown("✅ Interactive Dashboard")
    st.markdown("✅ Goal Setting")
    st.markdown("✅ Personalized Recommendations")
    st.markdown("✅ Achievement Tracking")

# Close database connection when the app exits
def on_shutdown():
    db_manager.close()

import atexit
atexit.register(on_shutdown)
