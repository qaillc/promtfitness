"""
Activity model for representing fitness activity data in the application.
"""
from datetime import datetime
from ..db_manager import db_manager

class Activity:
    """
    Activity model representing fitness data for a student.
    Provides methods for CRUD operations on activity data.
    """
    
    def __init__(self, id=None, student_id=None, date=None, steps=None,
                 active_minutes=None, distance=None, calories=None, 
                 heart_rate=None, weight_kg=None):
        self.id = id
        self.student_id = student_id
        self.date = date
        self.steps = steps
        self.active_minutes = active_minutes
        self.distance = distance
        self.calories = calories
        self.heart_rate = heart_rate
        self.weight_kg = weight_kg
    
    @staticmethod
    def get_by_student(student_id, limit=None, date_from=None, date_to=None):
        """Get activities for a specific student with optional filtering."""
        query = "SELECT * FROM activity WHERE student_id=?"
        params = [student_id]
        
        if date_from:
            query += " AND date >= ?"
            params.append(date_from)
        
        if date_to:
            query += " AND date <= ?"
            params.append(date_to)
        
        query += " ORDER BY date DESC"
        
        if limit:
            query += f" LIMIT {int(limit)}"
        
        rows = db_manager.fetchall(query, tuple(params))
        return [Activity._row_to_activity(row) for row in rows]
    
    @staticmethod
    def get_by_id(activity_id):
        """Get an activity by ID."""
        row = db_manager.fetchone("SELECT * FROM activity WHERE id=?", (activity_id,))
        if row:
            return Activity._row_to_activity(row)
        return None
    
    def save(self):
        """Save or update an activity in the database."""
        if self.id:
            # Update existing activity
            db_manager.execute(
                """UPDATE activity SET student_id=?, date=?, steps=?, 
                active_minutes=?, distance=?, calories=?, heart_rate=?, weight_kg=? 
                WHERE id=?""",
                (self.student_id, self.date, self.steps, self.active_minutes,
                 self.distance, self.calories, self.heart_rate, self.weight_kg, self.id)
            )
        else:
            # Insert new activity
            cursor = db_manager.execute(
                """INSERT INTO activity 
                (student_id, date, steps, active_minutes, distance, calories, heart_rate, weight_kg) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (self.student_id, self.date, self.steps, self.active_minutes,
                 self.distance, self.calories, self.heart_rate, self.weight_kg)
            )
            self.id = cursor.lastrowid
        
        db_manager.commit()
        return self
    
    @staticmethod
    def delete(activity_id):
        """Delete an activity by ID."""
        db_manager.execute("DELETE FROM activity WHERE id=?", (activity_id,))
        db_manager.commit()
    
    @staticmethod
    def _row_to_activity(row):
        """Convert a database row to an Activity object."""
        return Activity(
            id=row['id'],
            student_id=row['student_id'],
            date=row['date'],
            steps=row['steps'],
            active_minutes=row['active_minutes'],
            distance=row['distance'],
            calories=row['calories'],
            heart_rate=row['heart_rate'],
            weight_kg=row['weight_kg']
        )
    
    def to_dict(self):
        """Convert the activity object to a dictionary."""
        return {
            'id': self.id,
            'student_id': self.student_id,
            'date': self.date,
            'steps': self.steps,
            'active_minutes': self.active_minutes,
            'distance': self.distance,
            'calories': self.calories,
            'heart_rate': self.heart_rate,
            'weight_kg': self.weight_kg
        }
