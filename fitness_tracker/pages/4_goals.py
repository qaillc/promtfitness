"""
Goals page for setting and tracking student fitness goals.
"""
import streamlit as st
import sys
import pandas as pd
import plotly.express as px
from pathlib import Path
from datetime import datetime, timedelta

# Add parent directory to path to import services
sys.path.append(str(Path(__file__).parent.parent))
from services.student_service import StudentService
from services.activity_service import ActivityService
from services.analytics_service import AnalyticsService

st.set_page_config(page_title="Fitness Goals", page_icon="🎯")

st.title("Fitness Goals")
st.write("Set and track fitness goals for students.")

# Initialize session state for goals
if 'goals' not in st.session_state:
    st.session_state.goals = {}

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

    # Create tabs for different goal types
    tab1, tab2, tab3 = st.tabs(["Steps Goals", "Activity Goals", "Weight Goals"])
    
    with tab1:
        st.subheader("Daily Steps Goal")
        
        # Get current goal from session state or set default
        current_steps_goal = 7500
        if student_id in st.session_state.goals and 'steps' in st.session_state.goals[student_id]:
            current_steps_goal = st.session_state.goals[student_id]['steps']
        
        # Set new goal
        col1, col2 = st.columns([3, 1])
        with col1:
            new_steps_goal = st.slider("Daily Steps Target", 1000, 20000, current_steps_goal, step=500)
        
        with col2:
            if st.button("Set Steps Goal", key="set_steps"):
                if student_id not in st.session_state.goals:
                    st.session_state.goals[student_id] = {}
                st.session_state.goals[student_id]['steps'] = new_steps_goal
                st.success(f"Steps goal set to {new_steps_goal:,} steps per day")
                
                # Add points for setting a goal
                if 'points' in st.session_state:
                    st.session_state.points += 2
                    st.success("You earned 2 points for setting a goal!")
        
        # Get activity data for this student
        student_data = AnalyticsService.get_student_metrics(student_id, days=30)
        if student_data and student_data["activity_data"]:
            activity_data = student_data["activity_data"]
            df_activity = pd.DataFrame(activity_data)
            if len(df_activity) > 0:
                df_activity["date"] = pd.to_datetime(df_activity["date"])
                df_activity = df_activity.sort_values("date")
                
                # Calculate goal achievement
                if student_id in st.session_state.goals and 'steps' in st.session_state.goals[student_id]:
                    goal = st.session_state.goals[student_id]['steps']
                    df_activity["goal_achieved"] = df_activity["steps"] >= goal
                    days_achieved = df_activity["goal_achieved"].sum()
                    total_days = len(df_activity)
                    achievement_rate = (days_achieved / total_days * 100) if total_days > 0 else 0
                    
                    # Display achievement metrics
                    st.metric(
                        label="Goal Achievement Rate", 
                        value=f"{achievement_rate:.1f}%",
                        delta=f"{days_achieved} of {total_days} days"
                    )
                    
                    # Create a goal progress chart
                    fig = px.line(
                        df_activity,
                        x="date",
                        y="steps",
                        title=f"Daily Steps vs. Goal ({goal:,} steps)",
                        labels={"date": "Date", "steps": "Steps"}
                    )
                    
                    # Add goal line
                    fig.add_shape(
                        type="line",
                        x0=df_activity["date"].min(),
                        y0=goal,
                        x1=df_activity["date"].max(),
                        y1=goal,
                        line=dict(color="red", width=2, dash="dash"),
                    )
                    
                    # Color code points based on goal achievement
                    fig.update_traces(
                        mode="markers+lines",
                        marker=dict(
                            size=10,
                            color=df_activity["steps"].apply(lambda x: "green" if x >= goal else "red")
                        )
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Progress bar 
                    st.progress(achievement_rate/100)
                    
                    # Achievement badges
                    if achievement_rate >= 80 and 'steps_achiever' not in st.session_state.achievements:
                        st.session_state.achievements.append('steps_achiever')
                        st.balloons()
                        st.success("🏆 Achievement Unlocked: Steps Champion!")
                        # Add bonus points
                        st.session_state.points += 20
                else:
                    st.info("Set a steps goal above to track progress.")
            else:
                st.info("No activity data available for goal tracking.")
        else:
            st.info("No activity data available. Log some activities to track goal progress.")
    
    with tab2:
        st.subheader("Active Minutes Goal")
        
        # Get current goal from session state or set default
        current_active_goal = 30
        if student_id in st.session_state.goals and 'active_minutes' in st.session_state.goals[student_id]:
            current_active_goal = st.session_state.goals[student_id]['active_minutes']
        
        # Set new goal
        col1, col2 = st.columns([3, 1])
        with col1:
            new_active_goal = st.slider("Daily Active Minutes Target", 10, 180, current_active_goal, step=5)
        
        with col2:
            if st.button("Set Activity Goal", key="set_active"):
                if student_id not in st.session_state.goals:
                    st.session_state.goals[student_id] = {}
                st.session_state.goals[student_id]['active_minutes'] = new_active_goal
                st.success(f"Activity goal set to {new_active_goal} minutes per day")
                
                # Add points for setting a goal
                if 'points' in st.session_state:
                    st.session_state.points += 2
        
        # Get activity data for this student
        student_data = AnalyticsService.get_student_metrics(student_id, days=30)
        if student_data and student_data["activity_data"]:
            activity_data = student_data["activity_data"]
            df_activity = pd.DataFrame(activity_data)
            if len(df_activity) > 0:
                df_activity["date"] = pd.to_datetime(df_activity["date"])
                df_activity = df_activity.sort_values("date")
                
                # Calculate goal achievement
                if student_id in st.session_state.goals and 'active_minutes' in st.session_state.goals[student_id]:
                    goal = st.session_state.goals[student_id]['active_minutes']
                    df_activity["goal_achieved"] = df_activity["active_minutes"] >= goal
                    days_achieved = df_activity["goal_achieved"].sum()
                    total_days = len(df_activity)
                    achievement_rate = (days_achieved / total_days * 100) if total_days > 0 else 0
                    
                    # Display achievement metrics
                    st.metric(
                        label="Goal Achievement Rate", 
                        value=f"{achievement_rate:.1f}%",
                        delta=f"{days_achieved} of {total_days} days"
                    )
                    
                    # Create a goal progress chart
                    fig = px.bar(
                        df_activity,
                        x="date",
                        y="active_minutes",
                        title=f"Daily Active Minutes vs. Goal ({goal} minutes)",
                        labels={"date": "Date", "active_minutes": "Active Minutes"}
                    )
                    
                    # Add goal line
                    fig.add_shape(
                        type="line",
                        x0=df_activity["date"].min(),
                        y0=goal,
                        x1=df_activity["date"].max(),
                        y1=goal,
                        line=dict(color="red", width=2, dash="dash"),
                    )
                    
                    # Color code bars based on goal achievement
                    fig.update_traces(
                        marker_color=df_activity["active_minutes"].apply(
                            lambda x: "green" if x >= goal else "red"
                        )
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Progress bar
                    st.progress(achievement_rate/100)
                    
                    # Achievement badges
                    if achievement_rate >= 80 and 'activity_achiever' not in st.session_state.achievements:
                        st.session_state.achievements.append('activity_achiever')
                        st.success("🏆 Achievement Unlocked: Active Lifestyle Master!")
                        # Add bonus points
                        st.session_state.points += 20
                else:
                    st.info("Set an activity goal above to track progress.")
            else:
                st.info("No activity data available for goal tracking.")
        else:
            st.info("No activity data available. Log some activities to track goal progress.")
    
    with tab3:
        st.subheader("Weight Goal")
        
        # Get activity data for this student to find current weight
        student_data = AnalyticsService.get_student_metrics(student_id, days=30)
        current_weight = None
        if student_data and student_data["metrics"]["latest_weight"]:
            current_weight = student_data["metrics"]["latest_weight"]
            
            # Get current goal from session state or set default based on current weight
            current_weight_goal = current_weight
            if student_id in st.session_state.goals and 'weight' in st.session_state.goals[student_id]:
                current_weight_goal = st.session_state.goals[student_id]['weight']
            
            # Set new goal
            col1, col2 = st.columns([3, 1])
            with col1:
                new_weight_goal = st.number_input(
                    "Target Weight (kg)",
                    min_value=20.0,
                    max_value=150.0,
                    value=float(current_weight_goal),
                    step=0.5
                )
            
            with col2:
                if st.button("Set Weight Goal", key="set_weight"):
                    if student_id not in st.session_state.goals:
                        st.session_state.goals[student_id] = {}
                    st.session_state.goals[student_id]['weight'] = new_weight_goal
                    st.success(f"Weight goal set to {new_weight_goal} kg")
                    
                    # Add points for setting a goal
                    if 'points' in st.session_state:
                        st.session_state.points += 2
            
            # Weight goal tracking
            if student_data and student_data["activity_data"]:
                activity_data = student_data["activity_data"]
                df_activity = pd.DataFrame(activity_data)
                if len(df_activity) > 0 and "weight_kg" in df_activity and df_activity["weight_kg"].notnull().any():
                    df_activity["date"] = pd.to_datetime(df_activity["date"])
                    df_activity = df_activity.sort_values("date")
                    
                    # Calculate goal progress
                    if student_id in st.session_state.goals and 'weight' in st.session_state.goals[student_id]:
                        goal = st.session_state.goals[student_id]['weight']
                        
                        # Get starting and current weight
                        starting_weight = df_activity["weight_kg"].iloc[0]
                        current_weight = df_activity["weight_kg"].iloc[-1]
                        
                        # Calculate progress
                        if starting_weight > goal:  # Weight loss goal
                            total_to_lose = starting_weight - goal
                            lost_so_far = starting_weight - current_weight
                            progress_pct = (lost_so_far / total_to_lose * 100) if total_to_lose > 0 else 0
                        else:  # Weight gain goal
                            total_to_gain = goal - starting_weight
                            gained_so_far = current_weight - starting_weight
                            progress_pct = (gained_so_far / total_to_gain * 100) if total_to_gain > 0 else 0
                        
                        # Cap progress at 100%
                        progress_pct = min(progress_pct, 100)
                        
                        # Display progress metrics
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric(
                                label="Starting Weight", 
                                value=f"{starting_weight:.1f} kg"
                            )
                        with col2:
                            st.metric(
                                label="Current Weight", 
                                value=f"{current_weight:.1f} kg",
                                delta=f"{current_weight - starting_weight:.1f} kg"
                            )
                        
                        st.metric(
                            label="Goal Weight", 
                            value=f"{goal:.1f} kg",
                            delta=f"{(current_weight - goal):.1f} kg to go"
                        )
                        
                        # Progress bar
                        st.progress(progress_pct/100)
                        st.write(f"Progress: {progress_pct:.1f}% complete")
                        
                        # Create a weight tracking chart
                        fig = px.line(
                            df_activity,
                            x="date",
                            y="weight_kg",
                            title=f"Weight Progress Towards Goal ({goal:.1f} kg)",
                            labels={"date": "Date", "weight_kg": "Weight (kg)"}
                        )
                        
                        # Add goal line
                        fig.add_shape(
                            type="line",
                            x0=df_activity["date"].min(),
                            y0=goal,
                            x1=df_activity["date"].max(),
                            y1=goal,
                            line=dict(color="green", width=2, dash="dash"),
                        )
                        
                        # Add starting line
                        fig.add_shape(
                            type="line",
                            x0=df_activity["date"].min(),
                            y0=starting_weight,
                            x1=df_activity["date"].max(),
                            y1=starting_weight,
                            line=dict(color="red", width=1, dash="dot"),
                        )
                        
                        fig.update_traces(mode="markers+lines")
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Achievement badges
                        if progress_pct >= 50 and 'weight_progress' not in st.session_state.achievements:
                            st.session_state.achievements.append('weight_progress')
                            st.balloons()
                            st.success("🏆 Achievement Unlocked: Halfway There!")
                            # Add bonus points
                            st.session_state.points += 15
                    else:
                        st.info("Set a weight goal above to track progress.")
                else:
                    st.info("No weight data available for this student.")
        else:
            st.info("No weight data available. Log some activities with weight measurements to track goal progress.")
    
    # Goal recommendations
    st.markdown("---")
    st.subheader("Goal Recommendations")
    
    student_data = AnalyticsService.get_student_metrics(student_id, days=30)
    if student_data and student_data["activity_data"]:
        metrics = student_data["metrics"]
        
        st.markdown("""
        <div style="background-color:#f0f2f6; padding:15px; border-radius:10px;">
        <h4>Recommended Goals</h4>
        <p>Based on your current activity levels, we suggest the following targets:</p>
        """, unsafe_allow_html=True)
        
        # Steps recommendation (10% increase from current average)
        if metrics["avg_steps"] > 0:
            recommended_steps = round(metrics["avg_steps"] * 1.1 / 500) * 500  # Round to nearest 500
            st.markdown(f"- **Steps Goal:** {recommended_steps:,} steps per day")
        
        # Active minutes recommendation
        if metrics["avg_active_minutes"] > 0:
            recommended_minutes = round(max(30, metrics["avg_active_minutes"] * 1.1) / 5) * 5  # Round to nearest 5
            st.markdown(f"- **Active Minutes Goal:** {recommended_minutes} minutes per day")
        
        # Weight goal based on BMI
        if metrics["bmi"] and metrics["latest_weight"]:
            if metrics["bmi"] > 25:  # Overweight or obese
                recommended_weight = round((metrics["latest_weight"] * 0.95) * 2) / 2  # 5% reduction, round to nearest 0.5
                st.markdown(f"- **Weight Goal:** {recommended_weight:.1f} kg (5% reduction)")
            elif metrics["bmi"] < 18.5:  # Underweight
                recommended_weight = round((metrics["latest_weight"] * 1.05) * 2) / 2  # 5% increase, round to nearest 0.5
                st.markdown(f"- **Weight Goal:** {recommended_weight:.1f} kg (5% increase)")
            else:
                st.markdown(f"- **Weight Goal:** Maintain current weight of {metrics['latest_weight']:.1f} kg")
        
        st.markdown("""
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("Log some activities to receive personalized goal recommendations.")
        
    # Mobile view tip
    st.markdown("""
    <div style="background-color:#F0F2F6; padding: 10px; border-radius: 5px; margin-top: 20px;">
    <strong>💡 Tip:</strong> Goals are saved for your session and will persist as you navigate through the app.
    </div>
    """, unsafe_allow_html=True)