"""
Regenerate embeddings for all patient records in the database
This will index all existing patient records (001-003 and new 011-015)
Run from backend directory: python regenerate_embeddings.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import pickle
import logging
import sqlite3
from app.embedder import get_embedding
from app.db_handler import DB_FILE

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Setup directories
EMBEDDINGS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data', 'embeddings'))
os.makedirs(EMBEDDINGS_DIR, exist_ok=True)

DOCS_FILE = os.path.join(EMBEDDINGS_DIR, 'docs.pkl')
EMBEDDINGS_FILE = os.path.join(EMBEDDINGS_DIR, 'embeddings.pkl')

print("\n" + "="*70)
print("🔄 REGENERATING EMBEDDINGS FOR ALL PATIENT RECORDS")
print("="*70 + "\n")

try:
    # Get all records from database
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT record_id, patient_id, filename, content FROM records ORDER BY patient_id")
    all_records = [
        {
            'record_id': row[0],
            'patient_id': row[1],
            'filename': row[2],
            'content': row[3]
        }
        for row in c.fetchall()
    ]
    conn.close()
    
    if not all_records:
        print("❌ No records found in database!")
        sys.exit(1)
    
    print(f"📊 Found {len(all_records)} total records to embed")
    
    # Extract document texts and metadata
    docs = []
    embeddings = []
    
    print("\n📝 Embedding documents...")
    print("-" * 70)
    
    for idx, record in enumerate(all_records, 1):
        record_id = record.get('record_id')
        patient_id = record.get('patient_id')
        filename = record.get('filename')
        content = record.get('content', '')
        
        # Create embedding
        try:
            embedding = get_embedding(content)
            embeddings.append(embedding)
            
            # Store document metadata
            docs.append({
                'record_id': record_id,
                'patient_id': patient_id,
                'filename': filename,
                'content_preview': content[:200] + "..." if len(content) > 200 else content,
                'content_length': len(content)
            })
            
            print(f"✅ [{idx:2d}] Patient {patient_id} - {filename}")
            print(f"     └─ Content length: {len(content)} chars")
            
        except Exception as e:
            print(f"❌ [{idx:2d}] Error embedding patient {patient_id}: {e}")
    
    # Save embeddings and documents
    print("\n💾 Saving embeddings...")
    print("-" * 70)
    
    with open(DOCS_FILE, 'wb') as f:
        pickle.dump(docs, f)
    print(f"✅ Documents saved: {DOCS_FILE}")
    
    with open(EMBEDDINGS_FILE, 'wb') as f:
        pickle.dump(embeddings, f)
    print(f"✅ Embeddings saved: {EMBEDDINGS_FILE}")
    
    print("\n" + "="*70)
    print(f"✅ EMBEDDING COMPLETE!")
    print(f"   • Total documents indexed: {len(docs)}")
    print(f"   • Total embeddings created: {len(embeddings)}")
    print("="*70)
    
    # Show patients that were indexed
    print("\n📋 Patients indexed:")
    patients = {}
    for doc in docs:
        pid = doc['patient_id']
        if pid not in patients:
            patients[pid] = 0
        patients[pid] += 1
    
    for patient_id in sorted(patients.keys()):
        print(f"   • Patient {patient_id}: {patients[patient_id]} record(s)")
    
    print("\n✨ Ready to test! Run: python test_new_records.py")
    print("="*70 + "\n")
    
except Exception as e:
    print(f"\n❌ FATAL ERROR: {e}")
    logger.exception("Error regenerating embeddings")
    sys.exit(1)
