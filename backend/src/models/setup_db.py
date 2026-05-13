import sqlite3
import os

def init_db():
    # Get the directory of the current script (backend/src/models)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Go up two levels to get to the backend folder
    backend_dir = os.path.dirname(os.path.dirname(current_dir))
    
    # Path to tasks.db at the root of the backend folder
    db_path = os.path.join(backend_dir, 'tasks.db')
    
    print(f"Initializing database at {db_path}...")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create tasks table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title VARCHAR(255) NOT NULL,
            description TEXT,
            status VARCHAR(20) DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    
    print("Database initialization complete.")

if __name__ == "__main__":
    init_db()
