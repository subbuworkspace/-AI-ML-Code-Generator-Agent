
import os
import gradio as gr

from dotenv import load_dotenv
from smolagents import CodeAgent, LiteLLMModel, DuckDuckGoSearchTool

load_dotenv()

# Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_ID = os.getenv(
    "GEMINI_MODEL",
    "gemini/gemini-2.5-flash"
)

if not GEMINI_API_KEY:
    raise ValueError(
        "Please configure GEMINI_API_KEY in your .env file."
    )

# Initialize Gemini
model = LiteLLMModel(
    model_id=MODEL_ID,
    api_key=GEMINI_API_KEY,
    temperature=0.2
)

# Search tool
search_tool = DuckDuckGoSearchTool(max_results=5)

# AI Agent
agent = CodeAgent(
    tools=[search_tool],
    model=model,
    additional_authorized_imports=[
        "pandas",
        "numpy",
        "sklearn",
        "matplotlib",
        "seaborn",
        "math",
        "json"
    ],
    max_steps=6
)

SYSTEM_PROMPT = """
You are an expert AI and Machine Learning Developer.

Your responsibilities:
1. Understand the user's ML requirements.
2. Explain the problem-solving approach.
3. Generate Python code.
4. Recommend suitable ML algorithms.
5. Explain data preprocessing.
6. Explain model training and evaluation.
7. Provide readable and reusable code.
8. Explain assumptions and limitations.

Always respond with a structured technical explanation.
"""

def generate_solution(prompt):

    if not prompt.strip():
        return "Please enter an AI or ML task."

    try:
        task = f"""
        {SYSTEM_PROMPT}

        User Request:
        {prompt}
        """

        response = agent.run(task)

        return str(response)

    except Exception as error:
        return f"Error: {str(error)}"


# Gradio Interface
with gr.Blocks(
    title="AI/ML Code Generator Agent",
    theme=gr.themes.Soft()
) as demo:

    gr.Markdown(
        """
        # 🤖 AI/ML Code Generator Agent

        ### Your Intelligent Machine Learning Development Assistant

        Generate Python ML solutions using Agentic AI and Google Gemini.
        """
    )

    user_input = gr.Textbox(
        label="Enter your AI/ML requirement",
        placeholder="Example: Build an SVM classification model using Iris dataset",
        lines=5
    )

    generate_button = gr.Button(
        "Generate ML Solution",
        variant="primary"
    )

    output = gr.Markdown(
        label="Generated Solution"
    )

    generate_button.click(
        fn=generate_solution,
        inputs=user_input,
        outputs=output
    )

demo.launch()
