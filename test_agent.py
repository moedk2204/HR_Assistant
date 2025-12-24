"""
Quick test script for HR Assistant agent
Run from project root: python test_agent.py
"""

import sys
from pathlib import Path

# Ensure project root is in path
sys.path.insert(0, str(Path(__file__).parent))

from agent.agent import HRAssistantChat


def main():
    print("HR Assistant Agent Test\n")
    
    # Initialize chat
    chat = HRAssistantChat(verbose=True)
    
    # Test queries
    queries = [
        "Hi! What can you help me with?",
        "Get me the details for employee 3980",
        "What's the leave balance for employee 10075 ?",
        "Generate interview questions for data science role"
    ]
    
    for i, query in enumerate(queries, 1):
        print(f"\n{'='*70}")
        print(f"TEST {i}: {query}")
        print('='*70)
        
        response = chat.chat(query)
        
        print(f"\n✓ Response:\n{response}\n")
        input("Press Enter for next test...")
    
    print("\n✅ All tests completed!")


if __name__ == "__main__":
    main()