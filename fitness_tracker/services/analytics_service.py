"""
Analytics service for calculating metrics and statistics.
"""
import pandas as pd
import sys
from pathlib import Path
from datetime import datetime, timedelta

# Add parent directory to path to import models and services
sys.path.append(str(Path(__file__).parent.parent))
from database.models.activity import Activity
from database.models.student import Student

class AnalyticsService:
    """Service class for analytics and metrics calculations."""
    
    @staticmethod
    def calculate_bmi(height_cm, weight_kg):
        """Calculate BMI from height and weight."""
        if not height_cm or not weight_kg or height_cm == 0:
            return None
        height_m = height_cm / 100
        return round(weight_kg / (height_m ** 2), 1)
    
    @staticmethod
    def get_bmi_category(bmi):
        """Get the BMI category based on BMI value."""
        if bmi is None:
            return "N/A"
        if bmi < 18.5:
            return "Underweight"
        elif 18.5 <= bmi < 25:
            return "Normal weight"
        elif 25 <= bmi < 30:
            return "Overweight"
        else:
            return "Obese"
    
    @staticmethod
    def get_student_metrics(student_id, days=30):
        """Get key metrics for a student over a specified time period."""
        # Get student info
        student = Student.get_by_id(student_id)
        if not student:
            return None
        
        # Get activity data for time period
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        activities = Activity.get_by_student(
            student_id, 
            date_from=start_date.strftime("%Y-%m-%d"),
            date_to=end_date.strftime("%Y-%m-%d")
        )
        
        # If no activities, return basic student info
        if not activities:
            return {
                "student": student.to_dict(),
                "metrics": {
                    "total_steps": 0,
                    "avg_steps": 0,
                    "total_calories": 0,
                    "avg_active_minutes": 0,
                    "latest_weight": None,
                    "bmi": None,
                    "bmi_category": "N/A"
                },
                "activity_data": []
            }
        
        # Convert to dataframe for easier analysis
        activity_dicts = [a.to_dict() for a in activities]
        df = pd.DataFrame(activity_dicts)
        
        # Calculate metrics
        latest_weight = df["weight_kg"].iloc[0] if "weight_kg" in df and len(df) > 0 else None
        bmi = AnalyticsService.calculate_bmi(student.height_cm, latest_weight)
        
        metrics = {
            "total_steps": df["steps"].sum() if "steps" in df else 0,
            "avg_steps": df["steps"].mean() if "steps" in df else 0,
            "total_calories": df["calories"].sum() if "calories" in df else 0,
            "avg_active_minutes": df["active_minutes"].mean() if "active_minutes" in df else 0,
            "latest_weight": latest_weight,
            "bmi": bmi,
            "bmi_category": AnalyticsService.get_bmi_category(bmi)
        }
        
        return {
            "student": student.to_dict(),
            "metrics": metrics,
            "activity_data": activity_dicts
        }
    
    @staticmethod
    def get_trend_data(student_id, metric, days=30):
        """Get trend data for a specific metric over time."""
        # Get activity data
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        activities = Activity.get_by_student(
            student_id, 
            date_from=start_date.strftime("%Y-%m-%d"),
            date_to=end_date.strftime("%Y-%m-%d")
        )
        
        if not activities:
            return []
        
        # Convert to dataframe
        activity_dicts = [a.to_dict() for a in activities]
        df = pd.DataFrame(activity_dicts)
        
        # Ensure date is in datetime format and sort
        if "date" in df:
            df["date"] = pd.to_datetime(df["date"])
            df = df.sort_values("date")
        
        # Get data for requested metric
        if metric in df:
            trend_data = df[["date", metric]].values.tolist()
            return trend_data
        
        return []
