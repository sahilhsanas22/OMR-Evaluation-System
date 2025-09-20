import sqlite3
from typing import Optional, List, Dict, Any
import json
import os

class DatabaseManager:
    def __init__(self, db_path: str = None):
        if db_path is None:
            current_file_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(current_file_dir)
            db_dir = os.path.join(project_root, "database")
            os.makedirs(db_dir, exist_ok=True)
            self.db_path = os.path.join(db_dir, "omr_system.db")
        else:
            self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the database with required tables"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id TEXT NOT NULL,
                    exam_id TEXT NOT NULL,
                    upload_filename TEXT NOT NULL,
                    processed_filename TEXT,
                    score REAL,
                    total_questions INTEGER,
                    correct_answers INTEGER,
                    incorrect_answers INTEGER,
                    unanswered INTEGER,
                    processing_status TEXT DEFAULT 'pending',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS metadata (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    result_id INTEGER,
                    key TEXT NOT NULL,
                    value TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (result_id) REFERENCES results (id)
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS audit_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    action TEXT NOT NULL,
                    table_name TEXT NOT NULL,
                    record_id INTEGER,
                    old_values TEXT,
                    new_values TEXT,
                    user_id TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS answer_details (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    result_id INTEGER,
                    question_number INTEGER,
                    student_answer TEXT,
                    correct_answer TEXT,
                    is_correct BOOLEAN,
                    confidence_score REAL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (result_id) REFERENCES results (id)
                )
            ''')
            
            conn.commit()
    
    def insert_result(self, student_id: str, exam_id: str, upload_filename: str, 
                     score: Optional[float] = None, total_questions: Optional[int] = None) -> int:
        """Insert a new result record"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO results (student_id, exam_id, upload_filename, score, total_questions)
                VALUES (?, ?, ?, ?, ?)
            ''', (student_id, exam_id, upload_filename, score, total_questions))
            conn.commit()
            return cursor.lastrowid
    
    def update_result(self, result_id: int, **kwargs):
        """Update a result record"""
        if not kwargs:
            return
        
        set_clause = ', '.join([f"{key} = ?" for key in kwargs.keys()])
        values = list(kwargs.values())
        values.append(result_id)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(f'''
                UPDATE results 
                SET {set_clause}, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', values)
            conn.commit()
    
    def get_result(self, result_id: int) -> Optional[Dict]:
        """Get a specific result by ID"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM results WHERE id = ?', (result_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def get_all_results(self) -> List[Dict]:
        """Get all results"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM results ORDER BY created_at DESC')
            return [dict(row) for row in cursor.fetchall()]
    
    def get_results_by_exam(self, exam_id: str) -> List[Dict]:
        """Get all results for a specific exam"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM results WHERE exam_id = ? ORDER BY created_at DESC', (exam_id,))
            return [dict(row) for row in cursor.fetchall()]
    
    def insert_answer_detail(self, result_id: int, question_number: int, 
                           student_answer: str, correct_answer: str, 
                           is_correct: bool, confidence_score: float = 0.0):
        """Insert answer detail for a specific question"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO answer_details 
                (result_id, question_number, student_answer, correct_answer, is_correct, confidence_score)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (result_id, question_number, student_answer, correct_answer, is_correct, confidence_score))
            conn.commit()
    
    def get_answer_details(self, result_id: int) -> List[Dict]:
        """Get all answer details for a result"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM answer_details 
                WHERE result_id = ? 
                ORDER BY question_number
            ''', (result_id,))
            return [dict(row) for row in cursor.fetchall()]
    
    def log_audit(self, action: str, table_name: str, record_id: int, 
                 old_values: Dict = None, new_values: Dict = None, user_id: str = None):
        """Log an audit entry"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO audit_logs (action, table_name, record_id, old_values, new_values, user_id)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (action, table_name, record_id, 
                  json.dumps(old_values) if old_values else None,
                  json.dumps(new_values) if new_values else None,
                  user_id))
            conn.commit()
    
    def get_audit_logs(self, limit: int = 100) -> List[Dict]:
        """Get recent audit logs"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM audit_logs 
                ORDER BY timestamp DESC 
                LIMIT ?
            ''', (limit,))
            return [dict(row) for row in cursor.fetchall()]
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get system statistics"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            cursor.execute('SELECT COUNT(*) FROM results')
            total_results = cursor.fetchone()[0]

            cursor.execute('SELECT processing_status, COUNT(*) FROM results GROUP BY processing_status')
            status_counts = dict(cursor.fetchall())

            cursor.execute('SELECT AVG(score) FROM results WHERE score IS NOT NULL')
            avg_score = cursor.fetchone()[0] or 0

            cursor.execute('''
                SELECT COUNT(*) FROM results 
                WHERE created_at >= datetime('now', '-7 days')
            ''')
            recent_activity = cursor.fetchone()[0]
            
            return {
                'total_results': total_results,
                'status_counts': status_counts,
                'average_score': round(avg_score, 2),
                'recent_activity': recent_activity
            }