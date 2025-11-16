import sqlite3
import os
from typing import Dict, Any, List, Optional

DB_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'patient_records.db'))

# ---------------- Database Initialization ----------------
def init_db():
    """Create tables if they do not exist."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    # Patients table
    c.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            patient_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER,
            gender TEXT CHECK(gender IN ('Male', 'Female', 'Other'))
        )
    ''')
    
    # Records table
    c.execute('''
        CREATE TABLE IF NOT EXISTS records (
            record_id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id TEXT NOT NULL,
            filename TEXT,
            content TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE
        )
    ''')
    
    conn.commit()
    conn.close()

# ---------------- Add / Update Patient ----------------
def add_patient(patient_id: str, name: str, age: Optional[int] = None, gender: Optional[str] = None):
    """Insert a new patient or ignore if already exists."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        INSERT OR IGNORE INTO patients(patient_id, name, age, gender)
        VALUES (?, ?, ?, ?)
    """, (patient_id, name, age, gender))
    conn.commit()
    conn.close()

# ---------------- Add Patient Record ----------------
def add_record(patient_id: str, filename: str, content: str):
    """Add a new record for a patient."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    # Ensure patient exists
    c.execute("SELECT 1 FROM patients WHERE patient_id = ?", (patient_id,))
    if not c.fetchone():
        raise ValueError(f"Patient '{patient_id}' does not exist. Add patient first.")
    
    c.execute("""
        INSERT INTO records(patient_id, filename, content)
        VALUES (?, ?, ?)
    """, (patient_id, filename, content))
    
    conn.commit()
    conn.close()

# ---------------- Retrieve Patient Records ----------------
def get_patient_records(patient_id: str) -> List[Dict[str, Any]]:
    """Retrieve all records for a patient, ordered by timestamp descending."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        SELECT filename, content, timestamp
        FROM records
        WHERE patient_id = ?
        ORDER BY timestamp DESC
    """, (patient_id,))
    
    rows = c.fetchall()
    conn.close()
    
    return [{"filename": r[0], "content": r[1], "timestamp": r[2]} for r in rows]

# ---------------- Retrieve Patient Info ----------------
def get_patient_info(patient_id: str) -> Optional[Dict[str, Any]]:
    """Get basic patient info."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT patient_id, name, age, gender FROM patients WHERE patient_id = ?", (patient_id,))
    row = c.fetchone()
    conn.close()
    
    if row:
        return {"patient_id": row[0], "name": row[1], "age": row[2], "gender": row[3]}
    return None

# ---------------- Initialize DB on Import ----------------
init_db()
