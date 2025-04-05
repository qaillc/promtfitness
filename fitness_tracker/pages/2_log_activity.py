"""
Page for logging student activity data.
"""
import streamlit as st
import sys
from datetime import date
from pathlib import Path

# Add parent directory to path to import services
sys.path.append(str(Path(__file__).parent.parent))
from services.student_service import StudentService
from services.activity_service import ActivityService

st.set_page_config(page_title="Log Activity", page_icon="📝")

st.title("Log Activity")
st.write("Record fitness activities for students.")

# Get list of students
students = StudentService.get_all_students()

if not students:
    st.warning("No students found in the system. Please add a student first.")
    st.page_link("1_Add_Student", label="Go to Add Student", icon="➕")
else:
    # Create a form for better mobile experience
    with st.form("log_activity_form"):
        # Student selection
        student_options = StudentService.get_student_options_dict()
        selected_student = st.selectbox("Select Student", list(student_options.keys()))
        student_id = student_options[selected_student]
        
        # Date and activity data
        col1, col2 = st.columns(2)
        
        with col1:
            activity_date = st.date_input("Date", value=date.today())
            steps = st.number_input("Steps", min_value=0, value=0)
            active_minutes = st.number_input("Active Minutes", min_value=0, value=0)
        
        with col2:
            distance = st.number_input("Distance (km)", min_value=0.0, value=0.0, format="%.2f")
            calories = st.number_input("Calories Burned", min_value=0.0, value=0.0, format="%.1f")
            heart_rate = st.number_input("Heart Rate (avg)", min_value=0, value=0)
        
        weight_kg = st.number_input("Weight (kg)", min_value=0.0, value=60.0, format="%.1f")
        
        submitted = st.form_submit_button("Log Activity")
        
        if submitted:
            success, message = ActivityService.log_activity(
                student_id, str(activity_date), steps, active_minutes, 
                distance, calories, heart_rate, weight_kg
            )
            if success:
                st.success(message)
                
                # Add gamification points based on activity level
                if 'points' in st.session_state:
                    # Award points based on steps
                    if steps > 10000:
                        points_earned = 10
                    elif steps > 5000:
                        points_earned = 5
                    else:
                        points_earned = 2
                    
                    st.session_state.points += points_earned
                    st.success(f"You earned {points_earned} points for logging activity!")
                    
                    # Check for achievements
                    if steps > 10000 and 'step_master' not in st.session_state.achievements:
                        st.session_state.achievements.append('step_master')
                        st.balloons()
                        st.success("🏆 Achievement Unlocked: Step Master!")
            else:
                st.error(message)

    # Display recent activity logs for the selected student
    if 'selected_student' in locals() and student_id:
        st.subheader(f"Recent Activity for {selected_student.split(' (ID')[0]}")
        
        activities = ActivityService.get_activities_by_student(student_id, limit=5)
        
        if activities:
            # Convert to a list of dictionaries for display
            activity_data = [
                {
                    "Date": a.date,
                    "Steps": a.steps,
                    "Active Min": a.active_minutes,
                    "Distance (km)": a.distance,
                    "Calories": a.calories,
                    "Heart Rate": a.heart_rate,
                    "Weight (kg)": a.weight_kg
                }
                for a in activities
            ]
            
            st.dataframe(activity_data, use_container_width=True)
            
            # Activity summary card
            latest_activity = activities[0]
            
            # Create a card-like container for the latest activity
            st.markdown("### Today's Activity Summary")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Steps", f"{latest_activity.steps:,}")
            
            with col2:
                st.metric("Active Minutes", f"{latest_activity.active_minutes}")
            
            with col3:
                st.metric("Calories", f"{latest_activity.calories:.1f}")
                
            # Mobile view tips
            st.markdown("""
            <div style="background-color:#F0F2F6; padding: 10px; border-radius: 5px; margin-top: 20px;">
            <strong>💡 Tip:</strong> For the best experience on mobile, rotate your device to landscape mode when viewing activity data.
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("No activity data available for this student yet.")