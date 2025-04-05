"""
Personalized recommendations page for student fitness.
"""
import streamlit as st
import sys
import pandas as pd
from pathlib import Path
from datetime import datetime, date, timedelta

# Add parent directory to path to import services
sys.path.append(str(Path(__file__).parent.parent))
from services.student_service import StudentService
from services.activity_service import ActivityService
from services.analytics_service import AnalyticsService

st.set_page_config(page_title="Recommendations", page_icon="💡")

st.title("Personalized Recommendations")
st.write("Get tailored fitness recommendations based on activity history and goals.")

# Check if students exist
students = StudentService.get_all_students()
if not students:
    st.warning("No students found in the system. Please add students first.")
    st.page_link("1_Add_Student", label="Go to Add Student", icon="➕")
else:
    # Student selection
    student_options = StudentService.get_student_options_dict()
    selected_student = st.selectbox("Select Student", list(student_options.keys()))
    student_id = student_options[selected_student]
    student_name = selected_student.split(" (ID")[0]
    
    # Get student data
    student_data = AnalyticsService.get_student_metrics(student_id, days=30)
    
    if student_data and student_data["activity_data"]:
        # Extract data
        student = student_data["student"]
        metrics = student_data["metrics"]
        activity_data = student_data["activity_data"]
        
        # Convert to DataFrame for analysis
        df_activity = pd.DataFrame(activity_data)
        if len(df_activity) > 0:
            df_activity["date"] = pd.to_datetime(df_activity["date"])
            
            # Analyze activity patterns
            if len(df_activity) >= 5:
                # Calculate activity pattern stats
                df_activity["day_of_week"] = df_activity["date"].dt.day_name()
                dow_avg_steps = df_activity.groupby("day_of_week")["steps"].mean()
                best_day = dow_avg_steps.idxmax()
                worst_day = dow_avg_steps.idxmin()
                
                # Calculate time since last activity
                last_activity_date = df_activity["date"].max().date()
                days_since_last = (date.today() - last_activity_date).days
                
                # Header card with quick stats
                st.markdown(f"""
                <div style="background-color:#f0f2f6; padding:20px; border-radius:10px; margin-bottom:20px;">
                    <h3>Activity Overview for {student_name}</h3>
                    <p>Fitness level: <strong>{student['fitness_level']}</strong></p>
                    <p>Average daily steps: <strong>{metrics['avg_steps']:,.0f}</strong></p>
                    <p>Average active minutes: <strong>{metrics['avg_active_minutes']:.0f} min</strong></p>
                    <p>Most active day: <strong>{best_day}</strong></p>
                    <p>Least active day: <strong>{worst_day}</strong></p>
                </div>
                """, unsafe_allow_html=True)
                
                # Main recommendations section
                st.header("Your Personalized Recommendations")
                
                # Activity Pattern recommendations
                st.subheader("Activity Patterns")
                col1, col2 = st.columns(2)
                
                with col1:
                    if metrics['avg_steps'] < 5000:
                        activity_level = "low"
                        st.markdown("🔍 **Activity Level:** Your activity level is relatively low.")
                        st.markdown("Try to increase your daily steps by 500 each week until you reach at least 7,500 steps per day.")
                    elif metrics['avg_steps'] < 7500:
                        activity_level = "moderate"
                        st.markdown("🔍 **Activity Level:** Your activity level is moderate.")
                        st.markdown("You're on the right track! Try to reach 10,000 steps on at least 3 days per week.")
                    else:
                        activity_level = "high"
                        st.markdown("🔍 **Activity Level:** Your activity level is good!")
                        st.markdown("Great job maintaining an active lifestyle. Consider adding some strength training to complement your cardio activity.")
                
                with col2:
                    # Consistency recommendations
                    if days_since_last > 3:
                        st.markdown("⚠️ **Consistency Alert:**")
                        st.markdown(f"It's been {days_since_last} days since your last logged activity. Try to be more consistent with your routine.")
                    else:
                        st.markdown("✅ **Consistency:**")
                        st.markdown("You're doing well with tracking your activity regularly. Keep it up!")
                
                # Day-specific recommendations
                st.subheader("Day-Specific Recommendations")
                
                st.markdown(f"""
                <div style="background-color:#e8f4f9; padding:15px; border-radius:10px; margin-bottom:10px;">
                    <h4>💪 Best Day to Challenge Yourself</h4>
                    <p>Your most active day is <strong>{best_day}</strong>. This is a great day to push yourself a bit more or try new activities.</p>
                    <p><strong>Suggestion:</strong> On {best_day}s, try to add an extra 1,000 steps or 10 minutes of more intense activity.</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <div style="background-color:#fff3e0; padding:15px; border-radius:10px; margin-bottom:10px;">
                    <h4>🔋 Day to Focus On</h4>
                    <p>Your least active day is <strong>{worst_day}</strong>. This might be a good opportunity to add some easy activity.</p>
                    <p><strong>Suggestion:</strong> On {worst_day}s, schedule a 15-minute walk or light exercise session.</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Activity type recommendations based on fitness level
                st.subheader("Recommended Activities")
                
                if student['fitness_level'] == "Beginner":
                    st.markdown("""
                    As a beginner, focus on building a consistent routine with these activities:
                    
                    * **Walking:** Start with 15-20 minute walks and gradually increase duration
                    * **Light Stretching:** 5-10 minutes daily to improve flexibility
                    * **Chair Exercises:** If mobility is limited, try seated exercises
                    * **Water Activities:** Swimming or water walking for low-impact exercise
                    """)
                elif student['fitness_level'] == "Intermediate":
                    st.markdown("""
                    At your intermediate level, try adding variety to your routine:
                    
                    * **Brisk Walking or Light Jogging:** 20-30 minutes, 3-4 times per week
                    * **Bodyweight Exercises:** Push-ups, squats, and lunges
                    * **Cycling:** Great for cardio and lower body strength
                    * **Group Fitness Classes:** Try a beginner or intermediate class
                    """)
                else:  # Advanced
                    st.markdown("""
                    With your advanced fitness level, consider these challenging activities:
                    
                    * **Interval Training:** Mix high-intensity bursts with recovery periods
                    * **Strength Training:** Add weights to your routine 2-3 times per week
                    * **Running or Jogging:** Work up to 5K or longer distances
                    * **Sports Participation:** Join a local team or league
                    * **Advanced Classes:** HIIT, spinning, or boot camp style workouts
                    """)
                
                # BMI-based recommendations
                if metrics["bmi"]:
                    st.subheader("Body Composition Recommendations")
                    
                    bmi = metrics["bmi"]
                    bmi_category = metrics["bmi_category"]
                    
                    if bmi < 18.5:  # Underweight
                        st.markdown("""
                        Your BMI indicates you may be underweight. Consider:
                        
                        * Increasing caloric intake with nutrient-dense foods
                        * Adding strength training to build muscle mass
                        * Focusing on protein-rich foods after exercise
                        * Consulting with a healthcare provider about healthy weight gain
                        """)
                    elif 18.5 <= bmi < 25:  # Normal
                        st.markdown("""
                        Your BMI is in the healthy range. To maintain this:
                        
                        * Continue your balanced approach to activity
                        * Focus on maintaining strength and cardiovascular fitness
                        * Consider adding variety to your routine to stay engaged
                        * Pay attention to recovery and sleep quality
                        """)
                    elif 25 <= bmi < 30:  # Overweight
                        st.markdown("""
                        Your BMI indicates you may be overweight. Consider:
                        
                        * Gradually increasing activity levels, especially cardio
                        * Setting a goal of 150+ active minutes per week
                        * Adding strength training to build muscle and boost metabolism
                        * Focusing on nutrient-dense foods and portion awareness
                        """)
                    else:  # Obese
                        st.markdown("""
                        Your BMI indicates obesity. Consider:
                        
                        * Starting with low-impact activities like walking or swimming
                        * Building up gradually to avoid injury
                        * Setting realistic, small goals for daily activity
                        * Consulting with a healthcare provider about a safe approach
                        """)
                
                # Next steps and challenges
                st.subheader("Next Steps & Challenges")
                
                # Get current goals from session state if they exist
                has_goals = False
                if 'goals' in st.session_state and student_id in st.session_state.goals:
                    has_goals = True
                    steps_goal = st.session_state.goals[student_id].get('steps', 7500)
                    active_min_goal = st.session_state.goals[student_id].get('active_minutes', 30)
                    
                    if metrics['avg_steps'] >= steps_goal and metrics['avg_active_minutes'] >= active_min_goal:
                        # Exceeding goals
                        st.markdown("""
                        🌟 **Challenge Yourself!**
                        
                        You're exceeding your current goals - it might be time to set more challenging targets.
                        Consider increasing your step goal by 10% or adding a new type of activity to your routine.
                        """)
                    else:
                        # Working towards goals
                        st.markdown("""
                        🔄 **Keep Working Toward Your Goals**
                        
                        You're making progress! Keep focusing on consistency rather than perfection.
                        Try setting a "non-zero" day goal - do at least some activity every day, even if it's just a 5-minute walk.
                        """)
                else:
                    # No goals set yet
                    st.markdown("""
                    🎯 **Set Some Goals**
                    
                    You haven't set any specific goals yet. Setting clear, achievable goals can help motivate you
                    and give you something concrete to work toward.
                    """)
                    st.page_link("pages/4_goals.py", label="Set Goals Now", icon="🎯")
                
                # Weekly focus recommendation
                st.markdown("""
                <div style="background-color:#e8f5e9; padding:15px; border-radius:10px; margin:20px 0;">
                    <h4>💫 Your Weekly Focus</h4>
                    <p>Based on your recent activity, here's what to focus on this week:</p>
                """, unsafe_allow_html=True)
                
                # Different focus areas based on activity level
                if activity_level == "low":
                    st.markdown("""
                    **Consistency** - Try to be active every day, even if just for 10 minutes.
                    Add a 5-minute walk after each meal to easily increase your daily steps.
                    """)
                elif activity_level == "moderate":
                    st.markdown("""
                    **Intensity** - Add short bursts of higher intensity to your routine.
                    Try walking faster for 30 seconds, then normal pace for 2 minutes, and repeat.
                    """)
                else:
                    st.markdown("""
                    **Recovery** - Make sure you're balancing activity with proper rest.
                    Add some gentle stretching or yoga to help your muscles recover.
                    """)
                    
                st.markdown("</div>", unsafe_allow_html=True)
                
                # Gamification element - unlock a recommendation by logging activity
                st.subheader("Unlock Special Recommendation")
                
                if 'points' in st.session_state and st.session_state.points >= 30:
                    st.markdown("""
                    <div style="background-color:#e0f7fa; padding:15px; border-radius:10px; border:2px solid #4fc3f7;">
                        <h4>🌟 Premium Recommendation Unlocked!</h4>
                        <p><strong>Cross-Training Suggestion:</strong> Based on your activity patterns, you would benefit from adding 
                        variety to your routine. Try alternating between cardio days and strength days for the best 
                        overall fitness improvements. This approach helps prevent plateaus and reduces injury risk.</p>
                        <p>Specific workout ideas:</p>
                        <ul>
                            <li>Monday: Cardio - Walking/jogging</li>
                            <li>Tuesday: Strength - Upper body</li>
                            <li>Wednesday: Rest or light activity</li>
                            <li>Thursday: Cardio - Interval training</li>
                            <li>Friday: Strength - Lower body</li>
                            <li>Weekend: Active recovery (walking, swimming)</li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    points_needed = 30 - st.session_state.points if 'points' in st.session_state else 30
                    st.markdown(f"""
                    <div style="background-color:#f5f5f5; padding:15px; border-radius:10px; border:2px dashed #9e9e9e;">
                        <h4>🔒 Premium Recommendation</h4>
                        <p>Earn {points_needed} more points to unlock a special cross-training recommendation 
                        tailored to your activity patterns.</p>
                        <p>Log more activities or achieve your goals to earn points!</p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("We need at least 5 days of activity data to generate personalized recommendations. Please log more activities.")
        else:
            st.info("No activity data found. Log some activities to receive personalized recommendations.")
    else:
        st.info("No activity data available. Start logging activities to get personalized recommendations.")
    
    # Mobile view enhancement
    st.markdown("""
    <div style="background-color:#F0F2F6; padding: 10px; border-radius: 5px; margin-top: 20px;">
    <strong>💡 Tip:</strong> Recommendations are updated based on your most recent activity data.
    </div>
    """, unsafe_allow_html=True)