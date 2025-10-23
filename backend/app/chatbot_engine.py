# backend/app/chatbot_engine.py

def get_bot_response(user_message: str) -> str:
    """
    Placeholder for chatbot response.
    Later replace with real RAG engine logic using embeddings + vector search + LLM generation.
    """
    return f"Echo: {user_message} (AI response placeholder)"


def get_ai_response(message: str) -> str:
    """
    Another placeholder function for API responses.
    """
    return f"Echo: {message} (AI response placeholder)"


# Example usage (for testing in Python console)
if __name__ == "__main__":
    test_message = "Hello, AI!"
    print(get_bot_response(test_message))
    print(get_ai_response(test_message))
