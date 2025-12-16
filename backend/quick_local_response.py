import sqlite3
import os
import textwrap
import sys

DB_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data', 'patient_records.db'))


def local_generate_from_db(patient_id: str):
    if not os.path.exists(DB_FILE):
        print("Database not found:", DB_FILE)
        return
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT filename, content, timestamp FROM records WHERE patient_id = ? ORDER BY timestamp DESC", (patient_id,))
    rows = c.fetchall()
    conn.close()

    if not rows:
        print(f"No records found for patient {patient_id}")
        return

    lines = ["### 🩺 Answer based on internal patient records:\n"]
    for i, (filename, content, timestamp) in enumerate(rows, start=1):
        excerpt = (content or "").strip().replace('\n', ' ')
        if len(excerpt) > 600:
            excerpt = excerpt[:600].rsplit(' ', 1)[0] + "..."
        wrapped = textwrap.fill(excerpt, width=100)
        lines.append(f"**Record {i} ({filename}):**\n* {wrapped}\n\n")

    print('\n'.join(lines))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python quick_local_response.py <PATIENT_ID>')
        sys.exit(1)
    pid = sys.argv[1]
    local_generate_from_db(pid)
