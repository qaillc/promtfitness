"""
Enhanced Dashboard page with advanced analytics and visualizations.
"""
import streamlit as st
import sys
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import date, timedelta
from pathlib import Path

# Add parent directory to path to import services
sys.path.append(str(Path(__file__).parent.parent))
from services.student_service import StudentService
from services.activity_service import ActivityService
from services.analytics_service import AnalyticsService

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")

st.title("Student Fitness Dashboard")
st.write("Visualize and analyze student fitness data with interactive charts.")

students = StudentService.get_all_students()
if not students:
    st.warning("No students found in the system. Please add students first.")
    st.page_link("1_Add_Student", label="Go to Add Student", icon="➕")
else:
    # Student selection with tabs for multiple students
    student_options = StudentService.get_student_options_dict()
    col1, col2 = st.columns([3, 1])
    
    with col1:
        selected_student = st.selectbox("Select Student", list(student_options.keys()))
        student_id = student_options[selected_student]
    
    with col2:
        # Time period selection
        time_period = st.selectbox("Time Period", ["Last 7 days", "Last 30 days", "Last 90 days"])
        if time_period == "Last 7 days":
            days = 7
        elif time_period == "Last 30 days":
            days = 30
        else:
            days = 90
    
    # Get student metrics
    student_data = AnalyticsService.get_student_metrics(student_id, days=days)
    
    if not student_data:
        st.error("Failed to load student data.")
    else:
        student = student_data["student"]
        metrics = student_data["metrics"]
        activity_data = student_data["activity_data"]
        
        # Convert to DataFrame for easier manipulation
        df_activity = pd.DataFrame(activity_data)
        if len(df_activity) > 0:
            df_activity["date"] = pd.to_datetime(df_activity["date"])
        
        # Student profile and key metrics section
        st.markdown("## Student Profile")
        
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            # Student info card
            st.markdown(f"""
            <div style="background-color:#f0f2f6; padding:20px; border-radius:10px;">
                <h3>{student['name']}</h3>
                <p><strong>Age:</strong> {student['age']} | <strong>Grade:</strong> {student['grade']} | <strong>Gender:</strong> {student['gender']}</p>
                <p><strong>Fitness Level:</strong> {student['fitness_level']}</p>
                <p><strong>Height:</strong> {student['height_cm']} cm</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # Weight and BMI info
            st.markdown("### Weight & BMI")
            st.metric(
                label="Current Weight", 
                value=f"{metrics['latest_weight']:.1f} kg" if metrics['latest_weight'] else "N/A"
            )
            st.metric(
                label="BMI", 
                value=f"{metrics['bmi']:.1f}" if metrics['bmi'] else "N/A",
                delta=metrics['bmi_category']
            )
        
        with col3:
            # Activity streak and points
            st.markdown("### Engagement")
            
            # Calculate streak (consecutive days with activity)
            streak = 0
            if len(df_activity) > 0:
                # Sort by date descending
                df_sorted = df_activity.sort_values("date", ascending=False)
                
                # Get today and previous days
                today = date.today()
                
                # Check for consecutive days
                current_date = today
                for _, row in df_sorted.iterrows():
                    activity_date = row["date"].date()
                    # If this is the next consecutive day
                    if activity_date == current_date or activity_date == current_date - timedelta(days=1):
                        if activity_date != current_date:  # Only move the date pointer if it's different
                            current_date = activity_date
                        streak += 1
                    else:
                        break
            
            st.metric(label="Activity Streak", value=f"{streak} days")
            # Display points from session state
            st.metric(label="Total Points", value=st.session_state.points)
        
        # Key metrics section
        st.markdown("## Key Metrics")
        
        metric_cols = st.columns(4)
        
        with metric_cols[0]:
            st.metric(
                label="Avg. Daily Steps", 
                value=f"{metrics['avg_steps']:,.0f}",
                delta=f"{metrics['avg_steps'] - 7500:,.0f} from target" if metrics['avg_steps'] > 0 else None
            )
        
        with metric_cols[1]:
            st.metric(
                label="Avg. Active Minutes",
                value=f"{metrics['avg_active_minutes']:.1f}",
                delta=f"{metrics['avg_active_minutes'] - 30:.1f} from target" if metrics['avg_active_minutes'] > 0 else None
            )
        
        with metric_cols[2]:
            # Calculate average daily calories
            avg_daily_calories = metrics['total_calories'] / days if metrics['total_calories'] > 0 else 0
            st.metric(
                label="Avg. Daily Calories",
                value=f"{avg_daily_calories:.1f}"
            )
        
        with metric_cols[3]:
            # Calculate consistency (% of days with activity)
            days_with_activity = len(df_activity["date"].dt.date.unique()) if len(df_activity) > 0 else 0
            consistency = (days_with_activity / days) * 100 if days > 0 else 0
            st.metric(
                label="Consistency",
                value=f"{consistency:.1f}%"
            )
        
        # Enhanced data visualization section
        st.markdown("## Activity Trends")
        
        if len(df_activity) > 0:
            tab1, tab2, tab3, tab4 = st.tabs(["Steps", "Weight", "Activity Minutes", "Custom"])
            
            with tab1:
                # Steps visualization with target line
                fig_steps = px.line(
                    df_activity.sort_values("date"), 
                    x="date", 
                    y="steps",
                    title="Daily Steps Over Time",
                    labels={"date": "Date", "steps": "Steps"},
                    markers=True
                )
                
                # Add target line at 7,500 steps
                fig_steps.add_shape(
                    type="line",
                    x0=df_activity["date"].min(),
                    y0=7500,
                    x1=df_activity["date"].max(),
                    y1=7500,
                    line=dict(
                        color="green",
                        width=2,
                        dash="dash",
                    )
                )
                
                fig_steps.add_annotation(
                    x=df_activity["date"].max(),
                    y=7500,
                    text="Target: 7,500 steps",
                    showarrow=False,
                    yshift=10
                )
                
                # Color code based on target
                fig_steps.update_traces(
                    mode="markers+lines",
                    marker=dict(
                        size=10,
                        color=df_activity["steps"].apply(lambda x: "green" if x >= 7500 else "red")
                    )
                )
                
                st.plotly_chart(fig_steps, use_container_width=True)
                
                # Steps distribution
                fig_steps_dist = px.histogram(
                    df_activity,
                    x="steps",
                    nbins=10,
                    title="Steps Distribution",
                    labels={"steps": "Steps", "count": "Frequency"}
                )
                
                st.plotly_chart(fig_steps_dist, use_container_width=True)
            
            with tab2:
                # Weight trend
                if "weight_kg" in df_activity and df_activity["weight_kg"].notnull().any():
                    fig_weight = px.line(
                        df_activity.sort_values("date"),
                        x="date",
                        y="weight_kg",
                        title="Weight Over Time",
                        labels={"date": "Date", "weight_kg": "Weight (kg)"},
                        markers=True
                    )
                    
                    fig_weight.update_traces(mode="markers+lines")
                    
                    st.plotly_chart(fig_weight, use_container_width=True)
                    
                    # BMI Gauge
                    if metrics["bmi"]:
                        fig_gauge = go.Figure(go.Indicator(
                            mode="gauge+number",
                            value=metrics["bmi"],
                            title={'text': f"BMI: {metrics['bmi_category']}"},
                            gauge={
                                'axis': {'range': [0, 40]},
                                'bar': {'color': "blue"},
                                'steps': [
                                    {'range': [0, 18.5], 'color': "lightblue"},
                                    {'range': [18.5, 25], 'color': "lightgreen"},
                                    {'range': [25, 30], 'color': "orange"},
                                    {'range': [30, 40], 'color': "red"}
                                ],
                            }
                        ))
                        
                        st.plotly_chart(fig_gauge, use_container_width=True)
                else:
                    st.info("No weight data available for this student.")
            
            with tab3:
                # Active minutes visualization
                fig_active = px.bar(
                    df_activity.sort_values("date"),
                    x="date",
                    y="active_minutes",
                    title="Active Minutes Per Day",
                    labels={"date": "Date", "active_minutes": "Active Minutes"}
                )
                
                # Add target line at 30 minutes
                fig_active.add_shape(
                    type="line",
                    x0=df_activity["date"].min(),
                    y0=30,
                    x1=df_activity["date"].max(),
                    y1=30,
                    line=dict(
                        color="green",
                        width=2,
                        dash="dash",
                    )
                )
                
                fig_active.add_annotation(
                    x=df_activity["date"].max(),
                    y=30,
                    text="Target: 30 minutes",
                    showarrow=False,
                    yshift=10
                )
                
                # Color code based on target
                fig_active.update_traces(
                    marker_color=df_activity["active_minutes"].apply(
                        lambda x: "green" if x >= 30 else "orange" if x >= 15 else "red"
                    )
                )
                
                st.plotly_chart(fig_active, use_container_width=True)
                
                # Active minutes vs. calories scatter plot
                fig_scatter = px.scatter(
                    df_activity,
                    x="active_minutes",
                    y="calories",
                    title="Active Minutes vs. Calories Burned",
                    labels={"active_minutes": "Active Minutes", "calories": "Calories Burned"},
                    trendline="ols"  # Add trend line
                )
                
                st.plotly_chart(fig_scatter, use_container_width=True)
            
            with tab4:
                # Custom chart builder
                st.subheader("Custom Chart Builder")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    chart_type = st.selectbox(
                        "Chart Type",
                        ["Line", "Bar", "Scatter", "Box Plot"]
                    )
                
                with col2:
                    metrics_options = ["steps", "active_minutes", "distance", "calories", "heart_rate"]
                    if "weight_kg" in df_activity and df_activity["weight_kg"].notnull().any():
                        metrics_options.append("weight_kg")
                    
                    y_axis = st.selectbox("Select Metric", metrics_options)
                
                # Generate the selected chart type
                if chart_type == "Line":
                    custom_fig = px.line(
                        df_activity.sort_values("date"),
                        x="date",
                        y=y_axis,
                        title=f"{y_axis.replace('_', ' ').title()} Over Time",
                        markers=True
                    )
                elif chart_type == "Bar":
                    custom_fig = px.bar(
                        df_activity.sort_values("date"),
                        x="date",
                        y=y_axis,
                        title=f"{y_axis.replace('_', ' ').title()} Per Day"
                    )
                elif chart_type == "Scatter":
                    custom_fig = px.scatter(
                        df_activity.sort_values("date"),
                        x="date",
                        y=y_axis,
                        title=f"{y_axis.replace('_', ' ').title()} Distribution"
                    )
                elif chart_type == "Box Plot":
                    custom_fig = px.box(
                        df_activity,
                        y=y_axis,
                        title=f"{y_axis.replace('_', ' ').title()} Distribution"
                    )
                
                st.plotly_chart(custom_fig, use_container_width=True)
        else:
            st.info("No activity data available for this student. Log some activities to see visualizations.")
        
        # Weekly summary table
        st.markdown("## Weekly Summary")
        
        if len(df_activity) > 0:
            # Add week number to dataframe
            df_activity["week"] = df_activity["date"].dt.isocalendar().week
            
            # Group by week
            weekly_summary = df_activity.groupby("week").agg({
                "steps": "sum",
                "active_minutes": "sum",
                "distance": "sum",
                "calories": "sum"
            }).reset_index()
            
            # Format the summary for display
            weekly_summary_display = pd.DataFrame({
                "Week": weekly_summary["week"],
                "Total Steps": weekly_summary["steps"].apply(lambda x: f"{x:,}"),
                "Active Minutes": weekly_summary["active_minutes"],
                "Distance (km)": weekly_summary["distance"].round(2),
                "Calories Burned": weekly_summary["calories"].round(1)
            })
            
            st.dataframe(weekly_summary_display, use_container_width=True)
        else:
            st.info("No activity data available for weekly summary.")
        
        # Mobile view enhancements
        st.markdown("""
        <div style="background-color:#F0F2F6; padding: 10px; border-radius: 5px; margin-top: 20px;">
        <strong>💡 Tip:</strong> For the best experience on mobile, rotate your device to landscape mode when viewing charts and tables.
        </div>
        """, unsafe_allow_html=True)