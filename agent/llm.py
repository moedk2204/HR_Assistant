import os
from dotenv import load_dotenv
from langchain_community.chat_models import ChatOllama
# Load environment variables
load_dotenv()


def get_ollama_llm(
    model: str = "gpt-oss:120b",
    base_url: str = "https://ollama.com",
    temperature: float = 0.1,
    **kwargs
):
    """
    Initialize and return ChatOllama instance configured for Ollama Cloud
    
    Args:
        model (str): Model name (default: "gpt-oss:120b")
        base_url (str): Ollama Cloud API endpoint
        temperature (float): Sampling temperature (0.0 to 1.0)
        **kwargs: Additional ChatOllama parameters
    
    Returns:
        ChatOllama: Configured LLM instance
    
    Environment Variables:
        OLLAMA_API_KEY: Required API key for Ollama Cloud
        OLLAMA_MODEL: Optional override for model name
        OLLAMA_BASE_URL: Optional override for base URL
    """
    # Get API key from environment
    api_key = os.getenv("OLLAMA_API_KEY")
    if not api_key:
        raise ValueError(
            "OLLAMA_API_KEY not found in environment variables. "
            "Please set it in your .env file or environment."
        )
    
    # Allow environment variable overrides
    model = os.getenv("OLLAMA_MODEL", model)
    base_url = os.getenv("OLLAMA_BASE_URL", base_url)
    
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    
    llm = ChatOllama(
        model=model,
        base_url=base_url,
        temperature=temperature,
        headers=headers,
        **kwargs
    )
    
    print(f"✓ Ollama LLM initialized: {model} @ {base_url}")
    
    return llm


def test_llm_connection():
    """
    Test the Ollama Cloud connection with a simple query
    Returns True if successful, raises exception otherwise
    """
    try:
        llm = get_ollama_llm()
        response = llm.invoke("Say 'Hello, HR Assistant!' if you can hear me.")
        print(f"✓ LLM Connection Test Passed")
        print(f"  Response: {response.content[:100]}...")
        return True
    except Exception as e:
        print(f"✗ LLM Connection Test Failed: {str(e)}")
        raise


if __name__ == "__main__":
    # Quick test when run directly
    print("Testing Ollama Cloud connection...")
    test_llm_connection()