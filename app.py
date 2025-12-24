"""
HR Assistant - Gradio Chat Interface
Main application entry point for the HR Assistant with web UI
"""

import gradio as gr
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from agent.agent import HRAssistantChat


# Initialize the agent
print("🚀 Initializing HR Assistant...")
chat_assistant = HRAssistantChat(verbose=False)
print("✅ HR Assistant ready!")


def chat_interface(message, history):
    """
    Process chat messages and return responses
    
    Args:
        message (str): User's message
        history (list): Chat history
    
    Returns:
        str: Assistant's response
    """
    if not message or message.strip() == "":
        return "Please enter a message."
    
    try:
        response = chat_assistant.chat(message)
        return response
    except Exception as e:
        return f"❌ Error: {str(e)}\n\nPlease try rephrasing your question."


def reset_conversation():
    """Reset the chat history"""
    chat_assistant.reset()
    return None

# Custom Premium Theme
modern_theme = gr.themes.Soft(
    primary_hue=gr.themes.colors.indigo,
    secondary_hue=gr.themes.colors.slate,
    font=[gr.themes.GoogleFont("Inter"), "ui-sans-serif", "system-ui", "sans-serif"],
).set(
    body_background_fill="*neutral_50",
    block_background_fill="white",
    block_border_width="1px",
    block_shadow="0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)",
    button_primary_background_fill="*primary_600",
    button_primary_background_fill_hover="*primary_700",
)

# Custom CSS for that "Premium" feel
custom_css = """
#chatbot {
    border-radius: 12px !important;
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    background-color: #0f172a !important; /* Slate 900 */
    border: 1px solid #1e293b !important;
}

/* Fix for message visibility and style in Dark Mode */
.message.user {
    background-color: #4f46e5 !important; /* Indigo 600 */
    color: white !important;
    border-radius: 18px 18px 2px 18px !important;
    border: none !important;
}

.message.bot, .message.assistant {
    background-color: #1e293b !important; /* Slate 800 */
    color: #f1f5f9 !important; /* Slate 100 */
    border-radius: 18px 18px 18px 2px !important;
    border: 1px solid #334155 !important;
}

/* Ensure markdown text inside bubbles is also visible */
.message p, .message li, .message span {
    color: inherit !important;
}

.footer {
    text-align: center;
    margin-top: 30px;
    color: #64748b;
    font-size: 0.875rem;
}

.header-container {
    text-align: center;
    margin-bottom: 2rem;
}

.header-container h1 {
    font-weight: 800;
    letter-spacing: -0.025em;
    color: #1e293b;
    margin-top: 1rem;
}
"""

# Build Gradio Interface
with gr.Blocks(css=custom_css, title="HR Assistant | Premium", theme=modern_theme) as demo:
    
    with gr.Column(elem_classes="header-container"):
        gr.Markdown(
            """
            # HR Assistant
            An intelligent agent for employee data, leave management, and recruitment support.
            """
        )
    
    with gr.Row():
        with gr.Column(scale=4):
            chatbot = gr.Chatbot(
                elem_id="chatbot",
                show_label=False,
                height=550,
                show_copy_button=True,
                avatar_images=(None, "https://api.dicebear.com/7.x/bottts/svg?seed=hr"),
                bubble_full_width=False
            )
            
            with gr.Row():
                msg = gr.Textbox(
                    show_label=False,
                    placeholder="Type your message here (e.g., 'What is the leave balance for 10026?')",
                    container=False,
                    scale=7
                )
                submit = gr.Button("Send", variant="primary", scale=1)
            
            with gr.Row():
                gr.ClearButton([msg, chatbot], value="Clear Chat", variant="secondary")
                reset = gr.Button("Reset Agent", variant="secondary")
        
        with gr.Column(scale=1):
            with gr.Group():
                gr.Markdown("### 🛡️ System Info")
                status_text = gr.Markdown("🟢 **Status:** Ready")
                gr.Markdown("**Model:** `gpt-oss:120b`")
                
                with gr.Accordion("💡 Quick Examples", open=True):
                    gr.Examples(
                        examples=[
                            ["What are the details for employee 3348?"],
                            ["Check leave balance for employee 10026"],
                            ["Generate 5 interview questions for a Data Scientist"],
                            ["What can you help me with?"]
                        ],
                        inputs=msg,
                        label=None
                    )
                
                with gr.Accordion("📂 Requirements", open=False):
                    gr.Markdown(
                        """
                        Ensure CSVs are in `data/`:
                        - `employee_data.csv`
                        - `leave_balances.csv`
                        - `recruitment_data.csv`
                        """
                    )

    # Footer
    gr.Markdown(
        """
        <div class="footer">
        Powered by LangChain & Ollama • Premium UI v2.0
        </div>
        """,
        elem_classes="footer"
    )
    
    # Event Handlers
    def user_message(message, history):
        if not message or message.strip() == "":
            return "", history
        if history is None:
            history = []
        return "", history + [[message, None]]
    
    def bot_response(history):
        if history and history[-1][1] is None:
            user_msg = history[-1][0]
            bot_msg = chat_interface(user_msg, history)
            history[-1][1] = bot_msg
        return history
    
    # Connect events
    msg.submit(user_message, [msg, chatbot], [msg, chatbot], queue=False).then(
        bot_response, chatbot, chatbot
    )
    
    submit.click(user_message, [msg, chatbot], [msg, chatbot], queue=False).then(
        bot_response, chatbot, chatbot
    )
    
    reset.click(
        reset_conversation,
        None,
        chatbot,
        queue=False
    ).then(
        lambda: "🟢 **Status:** Reset & Ready",
        None,
        status_text
    )


# Launch the app
if __name__ == "__main__":
    print("\n" + "="*60)
    print("🚀 Starting HR Assistant")
    print("="*60 + "\n")
    
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True,
        quiet=False
    )
