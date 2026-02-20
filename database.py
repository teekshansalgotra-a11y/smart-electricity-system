"""
Test script to initialize database and load sample data
Run this to set up your database for the first time
"""

from src.database import Database


def main():
    print("\n" + "="*60)
    print("SMART ELECTRICITY SYSTEM - DATABASE SETUP")
    print("="*60 + "\n")
    
    # Create database instance
    db = Database()
    
    # Step 1: Initialize database (create tables)
    print("Step 1: Creating database tables...")
    db.initialize_database()
    
    # Step 2: Load sample data
    print("\nStep 2: Loading sample data...")
    response = input("Do you want to load sample data? (yes/no): ").lower()
    
    if response in ['yes', 'y']:
        db.load_sample_data()
    else:
        print("Skipping sample data. Database tables are empty.")
    
    # Step 3: Show statistics
    print("\nStep 3: Database Statistics")
    db.get_table_counts()
    
    print("Database setup complete!")
    print("Database file created: electricity_system.db")
    print("\nYou can now run the main application: python main.py\n")


if __name__ == "__main__":
    main()