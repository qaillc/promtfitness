"""
Database schema definitions for the Fitness Tracker application.
Defines table structures and creation methods.
"""
from .db_manager import db_manager

class Schema:
    """Class to handle database schema creation and migrations."""
    
    @staticmethod
    def create_tables():
        """Create the necessary tables if they don't exist."""
        # Create students table with flexible schema for future additions
        db_manager.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER,
                grade TEXT,
                gender TEXT,
                fitness_level TEXT,
                height_cm REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                -- Add additional fields here as needed
            )
        ''')
        
        # Create activity table with flexible schema for future additions
        db_manager.execute('''
            CREATE TABLE IF NOT EXISTS activity (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER,
                date TEXT,
                steps INTEGER,
                active_minutes INTEGER,
                distance REAL,
                calories REAL,
                heart_rate INTEGER,
                weight_kg REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(student_id) REFERENCES students(id)
                -- Add additional fields here as needed
            )
        ''')
        
        # Create metadata table for storing app-level information
        db_manager.execute('''
            CREATE TABLE IF NOT EXISTS metadata (
                key TEXT PRIMARY KEY,
                value TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create user_preferences table for future personalization
        db_manager.execute('''
            CREATE TABLE IF NOT EXISTS user_preferences (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER,
                preference_key TEXT,
                preference_value TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(student_id) REFERENCES students(id),
                UNIQUE(student_id, preference_key)
            )
        ''')
        
        # Commit the changes
        db_manager.commit()
    
    @staticmethod
    def add_column_if_not_exists(table_name, column_name, column_type):
        """
        Add a new column to an existing table if it doesn't already exist.
        This method allows for schema evolution.
        """
        # SQLite doesn't have a direct way to check if column exists, so we use PRAGMA
        cursor = db_manager.execute(f"PRAGMA table_info({table_name})")
        columns = [row[1] for row in cursor.fetchall()]
        
        if column_name not in columns:
            db_manager.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}")
            db_manager.commit()
            return True
        return False

# Initialize the schema
def init_schema():
    Schema.create_tables()
