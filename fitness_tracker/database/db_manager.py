"""
Database connection manager for the Fitness Tracker application.
Handles connection pooling and database operations.
"""
import sqlite3
import os
import sys
from pathlib import Path

# Add the parent directory to path to import config
sys.path.append(str(Path(__file__).parent.parent))
import config

class DatabaseManager:
    _instance = None
    
    def __new__(cls):
        """Singleton pattern to ensure only one database connection is created."""
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            cls._instance.conn = None
        return cls._instance
    
    def connect(self):
        """Create or get the existing database connection."""
        if self.conn is None:
            self.conn = sqlite3.connect(config.DB_PATH, check_same_thread=False)
            self.conn.row_factory = sqlite3.Row  # Return rows as dictionaries
        return self.conn
    
    def get_cursor(self):
        """Get a cursor from the connection."""
        return self.connect().cursor()
    
    def execute(self, query, params=None):
        """Execute a query with optional parameters."""
        cursor = self.get_cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        return cursor
    
    def executemany(self, query, params_list):
        """Execute a query with multiple sets of parameters."""
        cursor = self.get_cursor()
        cursor.executemany(query, params_list)
        return cursor
    
    def fetchone(self, query, params=None):
        """Execute a query and fetch one result."""
        cursor = self.execute(query, params)
        return cursor.fetchone()
    
    def fetchall(self, query, params=None):
        """Execute a query and fetch all results."""
        cursor = self.execute(query, params)
        return cursor.fetchall()
    
    def commit(self):
        """Commit changes to the database."""
        if self.conn:
            self.conn.commit()
    
    def close(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()
            self.conn = None

# Singleton instance to be imported elsewhere
db_manager = DatabaseManager()
