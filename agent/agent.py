"""
HR Assistant Agent
Implements the main agent logic with tool-calling capabilities
"""

import sys
from pathlib import Path
from typing import List
from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from langchain_core.messages import HumanMessage, AIMessage

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agent.llm import get_ollama_llm
from agent.tools import create_langchain_tools


# STRICT ReAct prompt to prevent mixed output
REACT_PROMPT_TEMPLATE = """
Answer the user's question by following this EXACT format. Do NOT deviate.

TOOLS:
{tools}

TOOL NAMES: {tool_names}

FORMAT - You MUST use this structure:

Question: [the user's question]
Thought: [your reasoning about what to do next]
Action: [ONLY the tool name from: {tool_names}]
Action Input: [the exact input for the tool]
Observation: [wait for tool result - you will see this]
... (you can repeat Thought/Action/Action Input/Observation if needed)
Thought: [once you have all info] I now know the final answer
Final Answer: [give the complete answer here]

CRITICAL RULES:
1. NEVER write "Final Answer" and "Action" in the same response
2. After "Action Input:", STOP and WAIT for Observation
3. Only write "Final Answer:" when you have all the information
4. Do NOT add extra text after "Final Answer:"

Question: {input}
{agent_scratchpad}"""


def create_hr_agent(verbose: bool = True):
    """
    Create and return the HR Assistant agent using ReAct pattern
    
    Args:
        verbose (bool): Enable verbose output for debugging
    
    Returns:
        AgentExecutor: Configured LangChain agent
    """
    # Initialize LLM
    llm = get_ollama_llm(temperature=0.1)  # Lower temp for more consistent output
    
    # Create tools
    tools = create_langchain_tools()
    
    # Create strict prompt template
    prompt = PromptTemplate.from_template(REACT_PROMPT_TEMPLATE)
    
    # Create agent using ReAct pattern
    agent = create_react_agent(llm, tools, prompt)
    
    # Create executor with stricter settings
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=verbose,
        handle_parsing_errors=True,
        max_iterations=3,  # Reduced to prevent loops
        max_execution_time=30,  # Timeout for long tasks
        early_stopping_method="force",
        handle_final_answer_only=True, # type: ignore 
        return_intermediate_steps=False  # Cleaner output
    )
    
    return agent_executor


class HRAssistantChat:
    """
    Stateful chat interface for the HR Assistant
    Maintains conversation history and handles multi-turn interactions
    """
    
    def __init__(self, verbose: bool = False):
        """
        Initialize HR Assistant chat interface
        
        Args:
            verbose (bool): Enable verbose agent output
        """
        self.agent = create_hr_agent(verbose=verbose)
        self.chat_history: List[tuple] = []
        self.verbose = verbose
    
    def chat(self, user_input: str) -> str:
        """
        Process user input and return agent response
        
        Args:
            user_input (str): User's message
        
        Returns:
            str: Agent's response
        """
        try:
            # Run agent
            response = self.agent.invoke({
                "input": user_input
            })
            
            # Extract final output
            output = response.get("output", "I apologize, but I couldn't process that request.")
            
            # Update chat history
            self.chat_history.append((user_input, output))
            
            return output
            
        except Exception as e:
            error_msg = f"I encountered an error: {str(e)}\n\nPlease try rephrasing your question."
            self.chat_history.append((user_input, error_msg))
            return error_msg
    
    def reset(self):
        """Clear conversation history"""
        self.chat_history = []
        if self.verbose:
            print("✓ Chat history cleared")
    
    def get_history(self) -> List[tuple]:
        """Get current chat history"""
        return self.chat_history.copy()


def run_simple_query(query: str, verbose: bool = True) -> str:
    """
    Run a single query without maintaining conversation state
    Useful for testing
    
    Args:
        query (str): User query
        verbose (bool): Enable verbose output
    
    Returns:
        str: Agent response
    """
    agent = create_hr_agent(verbose=verbose)
    result = agent.invoke({"input": query})
    return result.get("output", "No response generated")


if __name__ == "__main__":
    # Test the agent with sample queries
    print("=" * 60)
    print("HR ASSISTANT AGENT TEST")
    print("=" * 60)
    print()
    
    # Create chat interface
    chat = HRAssistantChat(verbose=True)
    
    # Test queries
    test_queries = [
        "Hello! What can you help me with?",
        "What are the details for employee 10026?",
        "Check the leave balance for employee 10026",
    ]
    
    for query in test_queries:
        print(f"\n{'='*60}")
        print(f"USER: {query}")
        print(f"{'='*60}")
        response = chat.chat(query)
        print(f"ASSISTANT: {response}")
        print()