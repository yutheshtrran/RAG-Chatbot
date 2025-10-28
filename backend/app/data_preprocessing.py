import os
import sys
import pdfplumber

# --- 1. Robust Path Setup ---
# Get the directory of the current script (data_preprocessing.py)
try:
    script_dir = os.path.dirname(os.path.abspath(__file__))
except NameError:
    # Fallback for environments like Jupyter or console execution
    # Note: sys.argv[0] gives the script path when run from console
    script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

# --- CORRECTED PATH LOGIC ---
# The logic navigates from the script directory (app/) up to (..) backend/, 
# then down to data/raw and data/processed directories.
RAW_DIR_RELATIVE = os.path.join(script_dir, '..', 'data', 'raw')
PROCESSED_DIR_RELATIVE = os.path.join(script_dir, '..', 'data', 'processed')

# Resolve to clean, absolute paths
RAW_DIR = os.path.abspath(RAW_DIR_RELATIVE)
PROCESSED_DIR = os.path.abspath(PROCESSED_DIR_RELATIVE)

# Check the corrected path
if not os.path.exists(RAW_DIR):
    print(f"Error: The raw data directory was not found.")
    print(f"Path expected: {RAW_DIR}")
    print("Please ensure your folder structure is correct (RAG-Chatbot/backend/data/raw).")
    # Exit the script if the source directory is missing
    sys.exit(1)

# Ensure the processed directory exists
os.makedirs(PROCESSED_DIR, exist_ok=True)
print(f"Source Directory: {RAW_DIR}")
print(f"Output Directory: {PROCESSED_DIR}")

# --- 2. File Processing Loop ---
count = 0
for filename in os.listdir(RAW_DIR):
    raw_path = os.path.join(RAW_DIR, filename)
    text = ""
    processed_filename = ""
    
    # Skip directories or non-file entries
    if os.path.isdir(raw_path):
        continue

    # --- Text/CSV Processing ---
    if filename.endswith(".txt") or filename.endswith(".csv"):
        print(f"Processing text file: {filename}")
        try:
            # Simple text files can be read directly
            with open(raw_path, "r", encoding="utf-8") as f:
                text = f.read()
            # Retain original name for text/csv files
            processed_filename = filename
            
        except Exception as e:
            print(f"Skipping {filename} due to text read error: {e}")
            continue

    # --- PDF Processing ---
    elif filename.endswith(".pdf"):
        print(f"Processing PDF file: {filename}")
        try:
            # Use pdfplumber to extract text from the binary PDF format
            with pdfplumber.open(raw_path) as pdf:
                for page in pdf.pages:
                    # Extract text; concatenate pages
                    text += page.extract_text() or "" 
            # Processed PDFs are saved as .txt files
            processed_filename = filename.replace(".pdf", ".txt")

        except Exception as e:
            print(f"Skipping {filename} due to PDF processing error: {e}")
            continue
            
    else:
        # Skip any other file types (e.g., .docx, .jpg)
        print(f"Skipping unsupported file type: {filename}")
        continue

    # --- 3. Preprocessing and Saving ---
    if text and processed_filename:
        # Standard preprocessing: remove excessive spaces, tabs, and newlines
        # by splitting the text and re-joining with a single space.
        text = " ".join(text.split()) 
        
        # Write the processed text to the PROCESSED_DIR
        processed_path = os.path.join(PROCESSED_DIR, processed_filename)
        
        try:
            with open(processed_path, "w", encoding="utf-8") as f:
                f.write(text)
            
            count += 1
            print(f"   -> Saved cleaned text as: {processed_filename}")
        except Exception as e:
            print(f"Failed to write file {processed_filename}: {e}")
            
    else:
        print(f"Skipping {filename} because no text was extracted.")


print("\n--- Summary ---")
print(f"Successfully preprocessed {count} files and saved them to {PROCESSED_DIR}")
