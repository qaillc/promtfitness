"""
Activity service for handling business logic related to fitness activities.
"""
import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path to import models
sys.path.append(str(Path(__file__).parent.parent))
from database.models.activity import Activity

class ActivityService:
    """Service class for activity-related operations."""
    
    @staticmethod
    def get_activities_by_student(student_id, limit=None, date_from=None, date_to=None):
        """Get activities for a student with optional filtering."""
        return Activity.get_by_student(student_id, limit, date_from, date_to)
    
    @staticmethod
    def get_activity_by_id(activity_id):
        """Get a single activity by ID."""
        return Activity.get_by_id(activity_id)
    
    @staticmethod
    def log_activity(student_id, date_str, steps, active_minutes, distance, 
                    calories, heart_rate, weight_kg):
        """Create and save a new activity log."""
        try:
            # Validate required fields
            if not student_id:
                return False, "Student ID is required"
            
            if not date_str:
                return False, "Date is required"
            
            # Create and save the activity
            activity = Activity(
                student_id=student_id,
                date=date_str,
                steps=steps,
                active_minutes=active_minutes,
                distance=distance,
                calories=calories,
                heart_rate=heart_rate,
                weight_kg=weight_kg
            )
            activity.save()
            return True, "Activity logged successfully!"
        except Exception as e:
            return False, f"Error logging activity: {str(e)}"
    
    @staticmethod
    def update_activity(activity_id, **kwargs):
        """Update an existing activity."""
        activity = Activity.get_by_id(activity_id)
        if not activity:
            return False, f"Activity with ID {activity_id} not found"
        
        # Update only the provided fields
        for key, value in kwargs.items():
            if hasattr(activity, key):
                setattr(activity, key, value)
        
        activity.save()
        return True, "Activity updated successfully!"
    
    @staticmethod
    def delete_activity(activity_id):
        """Delete an activity by ID."""
        activity = Activity.get_by_id(activity_id)
        if not activity:
            return False, f"Activity with ID {activity_id} not found"
        
        Activity.delete(activity_id)
        return True, "Activity deleted successfully!"
