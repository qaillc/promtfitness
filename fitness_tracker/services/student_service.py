"""
Student service for handling business logic related to student operations.
"""
import sys
from pathlib import Path

# Add parent directory to path to import models
sys.path.append(str(Path(__file__).parent.parent))
from database.models.student import Student

class StudentService:
    """Service class for student-related operations."""
    
    @staticmethod
    def get_all_students():
        """Get all students sorted by name."""
        return Student.get_all()
    
    @staticmethod
    def get_student_by_id(student_id):
        """Get a single student by ID."""
        return Student.get_by_id(student_id)
    
    @staticmethod
    def get_student_options_dict():
        """Get a dictionary of students for dropdown selection."""
        students = Student.get_all()
        return {f"{s.name} (ID: {s.id})": s.id for s in students}
    
    @staticmethod
    def add_student(name, age, grade, gender, fitness_level, height_cm):
        """Create and save a new student."""
        if not name:
            return False, "Student name is required"
        
        student = Student(
            name=name,
            age=age,
            grade=grade,
            gender=gender,
            fitness_level=fitness_level,
            height_cm=height_cm
        )
        student.save()
        return True, f"Student '{name}' added successfully!"
    
    @staticmethod
    def update_student(student_id, **kwargs):
        """Update an existing student."""
        student = Student.get_by_id(student_id)
        if not student:
            return False, f"Student with ID {student_id} not found"
        
        # Update only the provided fields
        for key, value in kwargs.items():
            if hasattr(student, key):
                setattr(student, key, value)
        
        student.save()
        return True, f"Student '{student.name}' updated successfully!"
    
    @staticmethod
    def delete_student(student_id):
        """Delete a student by ID."""
        student = Student.get_by_id(student_id)
        if not student:
            return False, f"Student with ID {student_id} not found"
        
        Student.delete(student_id)
        return True, f"Student '{student.name}' deleted successfully!"
