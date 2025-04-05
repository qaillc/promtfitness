"""
Student model for representing student data in the application.
"""
from ..db_manager import db_manager

class Student:
    """
    Student model representing a student in the fitness tracker.
    Provides methods for CRUD operations on student data.
    """
    
    def __init__(self, id=None, name=None, age=None, grade=None, 
                 gender=None, fitness_level=None, height_cm=None):
        self.id = id
        self.name = name
        self.age = age
        self.grade = grade
        self.gender = gender
        self.fitness_level = fitness_level
        self.height_cm = height_cm
    
    @staticmethod
    def get_all():
        """Get all students from the database."""
        rows = db_manager.fetchall("SELECT * FROM students ORDER BY name")
        return [Student._row_to_student(row) for row in rows]
    
    @staticmethod
    def get_by_id(student_id):
        """Get a student by ID."""
        row = db_manager.fetchone("SELECT * FROM students WHERE id=?", (student_id,))
        if row:
            return Student._row_to_student(row)
        return None
    
    def save(self):
        """Save or update a student in the database."""
        if self.id:
            # Update existing student
            db_manager.execute(
                "UPDATE students SET name=?, age=?, grade=?, gender=?, fitness_level=?, height_cm=?, updated_at=CURRENT_TIMESTAMP WHERE id=?",
                (self.name, self.age, self.grade, self.gender, self.fitness_level, self.height_cm, self.id)
            )
        else:
            # Insert new student
            cursor = db_manager.execute(
                "INSERT INTO students (name, age, grade, gender, fitness_level, height_cm) VALUES (?, ?, ?, ?, ?, ?)",
                (self.name, self.age, self.grade, self.gender, self.fitness_level, self.height_cm)
            )
            self.id = cursor.lastrowid
        
        db_manager.commit()
        return self
    
    @staticmethod
    def delete(student_id):
        """Delete a student by ID."""
        db_manager.execute("DELETE FROM students WHERE id=?", (student_id,))
        db_manager.commit()
    
    @staticmethod
    def _row_to_student(row):
        """Convert a database row to a Student object."""
        return Student(
            id=row['id'],
            name=row['name'],
            age=row['age'],
            grade=row['grade'],
            gender=row['gender'],
            fitness_level=row['fitness_level'],
            height_cm=row['height_cm']
        )
    
    def to_dict(self):
        """Convert the student object to a dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'grade': self.grade,
            'gender': self.gender,
            'fitness_level': self.fitness_level,
            'height_cm': self.height_cm
        }
