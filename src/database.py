"""
Database connection and management
Handles all database operations
"""

import sqlite3
from contextlib import contextmanager
from src.config import DATABASE_CONFIG


class Database:
    """Database connection handler for SQLite"""
    
    def __init__(self):
        self.db_path = DATABASE_CONFIG['database']
    
    @contextmanager
    def get_connection(self):
        """
        Context manager for database connections
        Automatically handles commit/rollback and connection closing
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Return rows as dictionaries
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(f" Database error: {e}")
            raise e
        finally:
            conn.close()
    
    def execute_query(self, query, params=None):
        """
        Execute a SELECT query and return results
        
        Args:
            query (str): SQL SELECT query
            params (tuple): Query parameters (optional)
            
        Returns:
            list: Query results as list of dictionaries
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor.fetchall()
    
    def execute_update(self, query, params=None):
        """
        Execute INSERT/UPDATE/DELETE query
        
        Args:
            query (str): SQL INSERT/UPDATE/DELETE query
            params (tuple): Query parameters (optional)
            
        Returns:
            int: Last inserted row ID (for INSERT) or affected rows
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor.lastrowid
    
    def initialize_database(self):
        """
        Create all tables from schema.sql
        This should be run once when setting up the system
        """
        try:
            # Read schema file
            with open('database/schema.sql', 'r') as f:
                schema = f.read()
            
            # Execute schema
            with self.get_connection() as conn:
                conn.executescript(schema)
            
            print(" Database initialized successfully!")
            print(f" Database file: {self.db_path}")
            
        except FileNotFoundError:
            print(" Error: database/schema.sql file not found!")
            print("Make sure you're running from the project root directory.")
        except Exception as e:
            print(f" Error initializing database: {e}")
    
    def load_sample_data(self):
        """
        Load sample data from sample_data.sql
        Useful for testing and demonstration
        """
        try:
            # Read sample data file
            with open('database/sample_data.sql', 'r') as f:
                sample_data = f.read()
            
            # Execute sample data
            with self.get_connection() as conn:
                conn.executescript(sample_data)
            
            print(" Sample data loaded successfully!")
            
        except FileNotFoundError:
            print(" Error: database/sample_data.sql file not found!")
        except Exception as e:
            print(f" Error loading sample data: {e}")
    
    def get_table_counts(self):
        """
        Get record count for all tables
        Useful for verifying data
        """
        tables = ['AREA', 'CONSUMER', 'ASSET', 'METER', 'CONSUMPTION', 'BILL', 'FAULT']
        
        print("\n" + "="*50)
        print("DATABASE STATISTICS")
        print("="*50)
        
        for table in tables:
            query = f"SELECT COUNT(*) as count FROM {table}"
            result = self.execute_query(query)
            count = dict(result[0])['count']
            print(f"{table:<15}: {count:>5} records")
        
        print("="*50 + "\n")