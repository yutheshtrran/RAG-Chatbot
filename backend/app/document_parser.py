"""
Patient information extractor from documents
"""
import re
from typing import Dict, Optional

def extract_patient_info(content: str) -> Dict[str, Optional[str]]:
    """
    Extract patient information from document content.
    
    Returns dict with keys: name, age, gender, patient_id, hospital
    """
    info = {
        "name": None,
        "age": None,
        "gender": None,
        "patient_id": None,
        "hospital": None,
        "diagnosis": None
    }
    
    # Normalize content
    content_lower = content.lower()
    lines = content.split("\n")
    
    # Extract Patient Name
    for pattern in [
        r"(?:Patient\s+)?[Nn]ame:\s*([A-Za-z\s]+?)(?:\s+(?:Age|Gender|ID|Date|,)|\n|$)",
        r"(?:Patient|[Pp]atient\s+[Nn]ame):\s*([A-Za-z\s]+?)(?:\s+(?:Age|Gender|ID)|,|\n|$)",
    ]:
        match = re.search(pattern, content)
        if match:
            name = match.group(1).strip()
            # Clean up - remove titles and extra words
            name = re.sub(r"\s*(Patient|ID|Age|Gender|Date).*", "", name)
            if len(name.split()) >= 2:  # At least first and last name
                info["name"] = name.strip()
                break
    
    # Extract Age
    for pattern in [
        r"(?:Age|AGE):\s*(\d+)\s*(?:[yY]|years?|[Yy]ears?)",
        r"(\d+)\s*(?:[yY]ears?|[yY]|yo|y\.o\.)",
    ]:
        match = re.search(pattern, content)
        if match:
            age = match.group(1).strip()
            if 0 < int(age) < 150:
                info["age"] = age
                break
    
    # Extract Gender
    for pattern in [
        r"(?:Gender|GENDER):\s*([MmFf](?:ale|emale)?)",
        r"(?:Sex):\s*([MmFf](?:ale|emale)?)",
    ]:
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            gender_text = match.group(1).strip().lower()
            if gender_text.startswith("m"):
                info["gender"] = "Male"
            elif gender_text.startswith("f"):
                info["gender"] = "Female"
            break
    
    # Extract Patient ID
    for pattern in [
        r"(?:Patient\s+)?ID:\s*([A-Za-z0-9\-]+)",
        r"P(?:atient)?:?\s*([0-9]{3,})",
    ]:
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            pid = match.group(1).strip()
            if len(pid) >= 2:
                info["patient_id"] = pid
                break
    
    # Extract Hospital
    for pattern in [
        r"(?:Hospital|HOSPITAL):\s*([A-Za-z\s]+?)(?:\n|$|,)",
        r"(?:Facility|FACILITY):\s*([A-Za-z\s]+?)(?:\n|$)",
    ]:
        match = re.search(pattern, content)
        if match:
            hospital = match.group(1).strip()
            if 3 < len(hospital) < 100:
                info["hospital"] = hospital
                break
    
    # Extract Chief Complaint / Diagnosis
    for pattern in [
        r"(?:DIAGNOSIS|Diagnosis):\s*([^:\n]+?)(?:\n|,|$)",
        r"(?:Chief\s+Complaint|CHIEF\s+COMPLAINT):\s*([^:\n]+?)(?:\n|$)",
    ]:
        match = re.search(pattern, content)
        if match:
            diag = match.group(1).strip()
            if 5 < len(diag) < 200:
                info["diagnosis"] = diag
                break
    
    return info

def generate_patient_display_name(extracted_info: Dict) -> str:
    """Generate a display name for the patient from extracted info."""
    name = extracted_info.get("name")
    age = extracted_info.get("age")
    gender = extracted_info.get("gender")
    
    parts = []
    if name:
        parts.append(name)
    if age and gender:
        parts.append(f"({age}{gender[0]})")
    elif age:
        parts.append(f"(Age {age})")
    
    return " ".join(parts) if parts else "Unnamed Patient"
