"""
Achievements and gamification features for the fitness tracker.
"""
import streamlit as st
import sys
import pandas as pd
import plotly.express as px
from pathlib import Path
from datetime import datetime, date, timedelta
import random

# Add parent directory to path to import services
sys.path.append(str(Path(__file__).parent.parent))
from services.student_service import StudentService
from services.activity_service import ActivityService
from services.analytics_service import AnalyticsService

st.set_page_config(page_title="Achievements", page_icon="🏆")

st.title("Achievements & Rewards")
st.write("Track your progress and earn rewards for consistency and meeting goals.")

# Initialize achievements if they don't exist
if 'achievements' not in st.session_state:
    st.session_state.achievements = []

if 'points' not in st.session_state:
    st.session_state.points = 0

# Define all possible achievements
all_achievements = {
    'step_master': {
        'name': 'Step Master',
        'description': 'Logged over 10,000 steps in a single day',
        'icon': '👣',
        'points': 10
    },
    'steps_achiever': {
        'name': 'Steps Champion',
        'description': 'Achieved your steps goal on 80% of days',
        'icon': '🥇',
        'points': 20
    },
    'activity_achiever': {
        'name': 'Active Lifestyle Master',
        'description': 'Achieved your active minutes goal on 80% of days',
        'icon': '⏱️',
        'points': 20
    },
    'weight_progress': {
        'name': 'Halfway There',
        'description': 'Reached 50% of your weight goal',
        'icon': '⚖️',
        'points': 15
    },
    'consistent_logger': {
        'name': 'Consistent Logger',
        'description': 'Logged activity for 7 consecutive days',
        'icon': '📝',
        'points': 15
    },
    'data_analyst': {
        'name': 'Data Analyst',
        'description': 'Viewed all dashboard charts and analytics',
        'icon': '📊',
        'points': 5
    },
    'goal_setter': {
        'name': 'Goal Setter',
        'description': 'Set goals for steps, activity, and weight',
        'icon': '🎯',
        'points': 10
    },
    'early_adopter': {
        'name': 'Early Adopter',
        'description': 'One of the first to use the fitness tracker',
        'icon': '🚀',
        'points': 5
    }
}

# Header with total points
st.markdown(f"""
<div style="background-color:#f0f2f6; padding:20px; border-radius:10px; text-align:center; margin-bottom:20px;">
    <h2>Your Total Points: {st.session_state.points}</h2>
    <p>Keep tracking your activity to earn more points and unlock achievements!</p>
</div>
""", unsafe_allow_html=True)

# Tabs for different sections
tab1, tab2, tab3 = st.tabs(["Achievements", "Leaderboard", "Rewards"])

with tab1:
    st.subheader("Your Achievements")
    
    # Display earned achievements
    if st.session_state.achievements:
        st.write("You've earned these achievements:")
        
        # Create a grid for achievements
        cols = st.columns(2)
        for i, achievement_id in enumerate(st.session_state.achievements):
            if achievement_id in all_achievements:
                achievement = all_achievements[achievement_id]
                with cols[i % 2]:
                    st.markdown(f"""
                    <div style="background-color:#e8f5e9; padding:15px; border-radius:10px; margin-bottom:10px;">
                        <h3>{achievement['icon']} {achievement['name']}</h3>
                        <p>{achievement['description']}</p>
                        <p><strong>+{achievement['points']} points</strong></p>
                    </div>
                    """, unsafe_allow_html=True)
    else:
        st.info("You haven't earned any achievements yet. Start logging activities and setting goals to earn achievements!")
    
    # Display locked achievements
    st.subheader("Achievements to Unlock")
    
    locked_achievements = [aid for aid in all_achievements if aid not in st.session_state.achievements]
    
    if locked_achievements:
        cols = st.columns(2)
        for i, achievement_id in enumerate(locked_achievements):
            achievement = all_achievements[achievement_id]
            with cols[i % 2]:
                st.markdown(f"""
                <div style="background-color:#f5f5f5; padding:15px; border-radius:10px; margin-bottom:10px; border:2px dashed #9e9e9e;">
                    <h3>🔒 {achievement['name']}</h3>
                    <p>{achievement['description']}</p>
                    <p><strong>+{achievement['points']} points</strong></p>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.success("Congratulations! You've unlocked all available achievements!")
    
    # Add "Claim Achievement" button for demo purposes
    st.markdown("---")
    st.subheader("Quick Achievement (Demo)")
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        # Create a dropdown of available achievements that haven't been claimed
        available_to_claim = [
            (aid, f"{achievement['name']} (+{achievement['points']} pts)") 
            for aid, achievement in all_achievements.items() 
            if aid not in st.session_state.achievements
        ]
        
        if available_to_claim:
            selected_achievement = st.selectbox(
                "Select an achievement to claim (for demonstration)",
                [item[1] for item in available_to_claim],
                index=0
            )
            selected_id = available_to_claim[[item[1] for item in available_to_claim].index(selected_achievement)][0]
        else:
            selected_id = None
            st.write("You've claimed all available achievements!")
    
    with col2:
        if selected_id and st.button("Claim Achievement"):
            # Add the achievement to the user's list
            st.session_state.achievements.append(selected_id)
            
            # Add the points
            st.session_state.points += all_achievements[selected_id]['points']
            
            st.success(f"🎉 Achievement claimed: {all_achievements[selected_id]['name']}")
            st.balloons()
    
    with col3:
        if st.button("Random Achievement"):
            # Select a random achievement that hasn't been claimed
            unclaimed = [aid for aid in all_achievements if aid not in st.session_state.achievements]
            
            if unclaimed:
                random_achievement = random.choice(unclaimed)
                
                # Add the achievement to the user's list
                st.session_state.achievements.append(random_achievement)
                
                # Add the points
                st.session_state.points += all_achievements[random_achievement]['points']
                
                st.success(f"🎉 Random achievement: {all_achievements[random_achievement]['name']}")
                st.balloons()
            else:
                st.info("You've already claimed all achievements!")

with tab2:
    st.subheader("Student Leaderboard")
    
    # Get all students
    students = StudentService.get_all_students()
    
    if students:
        # Generate random points for other students for demo purposes
        leaderboard_data = []
        
        for student in students:
            # Use actual points for the active student, random for others
            if 'current_student_id' in st.session_state and st.session_state.current_student_id == student.id:
                points = st.session_state.points
                achievements_count = len(st.session_state.achievements)
            else:
                # Generate random points and achievements for other students
                points = random.randint(5, 100)
                achievements_count = random.randint(0, len(all_achievements))
            
            leaderboard_data.append({
                "Student": student.name,
                "Points": points,
                "Achievements": achievements_count,
                "Level": 1 + (points // 20)  # Level up every 20 points
            })
        
        # Convert to DataFrame and sort
        df_leaderboard = pd.DataFrame(leaderboard_data)
        df_leaderboard = df_leaderboard.sort_values("Points", ascending=False)
        
        # Add rank column
        df_leaderboard.insert(0, "Rank", range(1, len(df_leaderboard) + 1))
        
        # Display the leaderboard
        st.dataframe(df_leaderboard, use_container_width=True, hide_index=True)
        
        # Visualize the leaderboard
        if len(df_leaderboard) > 1:
            st.subheader("Points Comparison")
            
            fig = px.bar(
                df_leaderboard,
                x="Student",
                y="Points",
                color="Points",
                color_continuous_scale="Viridis",
                title="Student Points Leaderboard"
            )
            
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No students found to display on the leaderboard.")

with tab3:
    st.subheader("Rewards Store")
    st.write("Spend your points to unlock rewards and special features.")
    
    # Create rewards that can be redeemed
    rewards = [
        {
            "name": "Custom Badge",
            "description": "Unlock a custom profile badge of your choice",
            "cost": 30,
            "icon": "🛡️"
        },
        {
            "name": "Dashboard Theme",
            "description": "Unlock a special color theme for your dashboard",
            "cost": 50,
            "icon": "🎨"
        },
        {
            "name": "Advanced Analytics",
            "description": "Unlock additional analytics features",
            "cost": 75,
            "icon": "📈"
        },
        {
            "name": "Virtual Trophy",
            "description": "A virtual trophy to display on your profile",
            "cost": 100,
            "icon": "🏆"
        }
    ]
    
    # Display available rewards
    cols = st.columns(2)
    for i, reward in enumerate(rewards):
        with cols[i % 2]:
            st.markdown(f"""
            <div style="background-color:#f0f2f6; padding:15px; border-radius:10px; margin-bottom:10px;">
                <h3>{reward['icon']} {reward['name']}</h3>
                <p>{reward['description']}</p>
                <p><strong>Cost: {reward['cost']} points</strong></p>
            </div>
            """, unsafe_allow_html=True)
            
            # Add redeem button
            can_afford = st.session_state.points >= reward['cost']
            
            if st.button(f"Redeem ({reward['cost']} pts)", key=f"redeem_{i}", disabled=not can_afford):
                if can_afford:
                    # Deduct points
                    st.session_state.points -= reward['cost']
                    st.success(f"🎉 You've redeemed: {reward['name']}!")
                    st.balloons()
                else:
                    st.error(f"Not enough points. You need {reward['cost'] - st.session_state.points} more points.")
    
    # Points history visualization
    st.subheader("Points History")
    
    # Generate fake points history for demonstration
    days = 14
    history_dates = [(date.today() - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(days)]
    
    # Create some random but realistic points data
    if 'points_history' not in st.session_state:
        base_points = max(0, st.session_state.points - random.randint(5, 20))
        daily_points = [random.randint(0, 5) for _ in range(days)]
        cumulative_points = [sum(daily_points[:i+1]) + base_points for i in range(days)]
        st.session_state.points_history = list(zip(history_dates, cumulative_points))
    
    # Create a DataFrame for the chart
    df_history = pd.DataFrame(st.session_state.points_history, columns=["Date", "Points"])
    df_history["Date"] = pd.to_datetime(df_history["Date"])
    df_history = df_history.sort_values("Date")
    
    # Plot the points history
    fig = px.line(
        df_history,
        x="Date",
        y="Points",
        title="Points History",
        markers=True
    )
    
    # Add today's points as the final point
    today = date.today().strftime("%Y-%m-%d")
    if today not in df_history["Date"].dt.strftime("%Y-%m-%d").values:
        fig.add_scatter(
            x=[today],
            y=[st.session_state.points],
            mode="markers",
            marker=dict(size=10, color="red"),
            name="Today"
        )
    
    st.plotly_chart(fig, use_container_width=True)

# Mobile view enhancement
st.markdown("""
<div style="background-color:#F0F2F6; padding: 10px; border-radius: 5px; margin-top: 20px;">
<strong>💡 Tip:</strong> Keep logging your activities consistently to earn more points and unlock achievements!
</div>
""", unsafe_allow_html=True)