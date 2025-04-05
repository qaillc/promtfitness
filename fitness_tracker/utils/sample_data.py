"""
Utility for generating sample data for the fitness tracker application.
"""
import random
import sys
from pathlib import Path
from datetime import date, timedelta

# Add parent directory to path to import models and services
sys.path.append(str(Path(__file__).parent.parent))
from database.models.student import Student
from database.models.activity import Activity

def load_sample_data():
    """Load sample students and activity data into the database."""
    # Sample students
    sample_students = [
        {"name": "Alice", "age": 15, "grade": "10", "gender": "Female", "fitness_level": "Beginner", "height_cm": 165},
        {"name": "Bob", "age": 16, "grade": "11", "gender": "Male", "fitness_level": "Intermediate", "height_cm": 175},
        {"name": "Charlie", "age": 14, "grade": "9", "gender": "Other", "fitness_level": "Advanced", "height_cm": 160}
    ]
    
    # Add sample students
    student_ids = []
    for student_data in sample_students:
        # Check if student already exists
        existing_students = Student.get_all()
        if any(s.name == student_data["name"] for s in existing_students):
            # Find the existing student ID
            for s in existing_students:
                if s.name == student_data["name"]:
                    student_ids.append(s.id)
        else:
            # Create new student
            student = Student(**student_data)
            student.save()
            student_ids.append(student.id)
    
    # Generate 30 days of activity data for each student
    num_days = 30
    start_date = date.today() - timedelta(days=num_days - 1)
    
    for student_id in student_ids:
        # Get student to determine baseline weight
        student = Student.get_by_id(student_id)
        base_weight = 55.0 if student.name == "Alice" else 65.0 if student.name == "Bob" else 50.0
        
        for i in range(num_days):
            current_day = start_date + timedelta(days=i)
            
            # Generate random activity data with some patterns
            steps = random.randint(3000, 15000)
            active_minutes = random.randint(10, 120)
            distance = round(random.uniform(2, 10), 2)
            calories = round(random.uniform(100, 800), 1)
            heart_rate = random.randint(60, 160)
            weight = round(base_weight + random.uniform(-0.5, 0.5), 1)
            
            # Check if activity already exists for this student and date
            activities = Activity.get_by_student(
                student_id, 
                date_from=current_day.isoformat(),
                date_to=current_day.isoformat()
            )
            
            if not activities:
                # Create activity record
                Activity(
                    student_id=student_id,
                    date=current_day.isoformat(),
                    steps=steps,
                    active_minutes=active_minutes,
                    distance=distance,
                    calories=calories,
                    heart_rate=heart_rate,
                    weight_kg=weight
                ).save()
    
    return len(student_ids)
