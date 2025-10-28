from typing import Dict, Any

def get_user_data(user_id: str) -> Dict[str, Any]:
    """
    Stub for retrieving user data.
    Returns example projects for demonstration.
    """
    return {
        "user": user_id,
        "projects": [
            "Clinical Trial A",
            "Diagnostic Model V2"
        ]
    }
