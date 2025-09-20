from .models import DatabaseManager

def initialize_database():
    """Initialize the database with sample data"""
    db = DatabaseManager()
    print("Database initialized successfully!")
    print("Tables created:")
    print("- results: Store OMR evaluation results")
    print("- metadata: Store additional metadata for results")
    print("- audit_logs: Store system audit logs")
    print("- answer_details: Store individual question answers")

    stats = db.get_statistics()
    print(f"\nCurrent statistics:")
    print(f"Total results: {stats['total_results']}")
    print(f"Average score: {stats['average_score']}")
    
    return db

if __name__ == "__main__":
    initialize_database()