import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.models import DatabaseManager

def setup_database():
    """Initialize the database with some sample data"""
    print("Setting up database...")
    db = DatabaseManager()
    
    try:
        db.add_result(
            student_id="STU001",
            exam_id="EXAM001",
            score=85.5,
            total_questions=100,
            correct_answers=85,
            wrong_answers=15,
            status="completed"
        )
        db.add_metadata(
            result_id=1,
            metadata={
                "exam_name": "Sample Math Test",
                "subject": "Mathematics",
                "duration": "120 minutes",
                "difficulty": "Medium"
            }
        )
        
        print("✅ Database setup completed successfully!")
        print("📊 Sample data added for testing")
        
    except Exception as e:
        print(f"⚠️ Note: Sample data not added (probably already exists): {e}")
    
    stats = db.get_statistics()
    print(f"📈 Current statistics: {stats}")

if __name__ == "__main__":
    setup_database()