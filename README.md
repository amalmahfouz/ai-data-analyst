# AI Data Analyst System 

An intelligent, interactive web application built with Streamlit, Python Pandas, Plotly, and Qwen3-Coder LLM. The system enables business users to upload CSV data files and explore them using natural language queries without writing code.





Goal: Upload your data file and ask natural language questions to receive instant textual answers, supporting data tables, and interactive visualizations in a single interface visit.

Target User: Sales managers, business analysts, operations teams, and non-technical professionals who need rapid insights from daily data files without writing SQL or Pandas queries.


##  Key Features
- CSV Data Inspection: Automatic parsing, row/column metric calculations, and data preview.
- Natural Language Data Querying: Translates user questions into safe, executable Pandas operations.
- Ambiguity  Management: Detects unclear user queries and asks clarification questions before executing code.
- Interactive Visualizations: Automatically generates Plotly charts for tabular or aggregated outputs.
- Session History Dashboard: Retains session history, executable code logs, and past queries in a collapsible sidebar.



##  Architecture & Project Structure
AI Data Analyst System/

  .env # API keys and environment variables

  config.py # Configuration parameters and LLM settings

  prompts.py # Intent classification & code generation prompts

  llm.py # OpenAI API client wrapper for Qwen

  helper.py # Code cleaning, execution input, and Plotly chart generator

  full_system.py # Core Agent decision logic and orchestration

  app.py # Streamlit UI frontend

  sales_data.csv # Sample dataset for testing

  PROJECT_PLAN.md 

  TEST_RESULTS.md # Test cases and validation results




Setup & Execution Guide

1. Prerequisites
- Python 3.8 or higher.
- A valid Hugging Face / Novita API Key for LLM access.

2. Installation
Clone/download the repository and install the dependencies:
-pip install streamlit pandas plotly openai python-dotenv

3. Environment Configuration
Create a .env file in the root folder and add your API key:
HF_API_KEY=your_huggingface_api_key_here

4. Running the Application
Launch the Streamlit web server:
    streamlit run app.py


##Example Usage
1. Open the application and upload sales_data.csv via the sidebar.

2. Review the automatically generated Data Quality report.

3. Type a query in the chat box: "What are the total sales per region?"

4. The system will output the calculated total, display a data table, and render an interactive Plotly bar chart.

5. Try an ambiguous query like "What is the best product?" to see the Agent's clarification guardrails in action.


New Tools & Techniques Learned
- Streamlit Session State: Mastered state management across reruns to preserve chat history and uploaded data.

- LLM Intent Classification: Built a two-step agent architecture (Intent -> Execution) to prevent unsafe  code execution.

- Dynamic Chart Generation: Automated Plotly visualizations based on pandas object types 


Known Limitations
- The system currently only supports .csv files.

- It is constrained to Pandas analytical operations (filtering, grouping, aggregating) and cannot perform predictive machine learning forecasting.

- Highly unstructured text data within the CSV may require manual cleaning before upload.



