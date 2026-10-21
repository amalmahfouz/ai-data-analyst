Project Name
- Smart Business Data Analyst

Problem Statement
- Sales managers and non-technical teams struggle with the slow process of analyzing   daily sales data stored in CSV files because they lack proficiency in writing code-based queries—such as those using Pandas or SQL—thereby hindering rapid decision-making.

realistic example
- The sales manager wants to know the "best-selling products at the main branch last month," so he has to wait for the data team to prepare the report.


Target User
- Sales managers, business analysts, and operations teams, and non-technical analysts.


Goal
-Upload your data file and ask natural language questions to receive instant textual answers, supporting data tables, and interactive visualizations in a single interface visit.


Scope
-Will Do:
 1. Reading CSV files, and detecting column structures and data types.
 2. Answering natural language questions by converting them into safe Pandas operations
 3. Generating illustrative charts and natural language text responses, with the option to request clarification if the question is ambiguous.
 4. Detect ambiguous queries and request clarification instead of guessing.

- Will NOT Do:
 1. Modifying the original CSV file or writing new data to it.
 2. Machine Learning forecasting

-Example Out of scope: 
 Forecast the expected sales for the coming year based on this file.

Input Contract
- file .csv    e.g. sales_data.csv
   if missing or error:
    "Display an alert message prompting the user to upload a valid CSV file and rejecting other file types."
- question from user (text :string)  
    "What are the total sales per region?"
    if missing or  ambiguous:
    "Flagging empty fields or asking clarifying questions if the inquiry is ambiguous."


Output Contract
- A data preview summary (number of rows and columns + the first 5 rows).
- A natural language text response directly explaining the result.
- A small table containing the filtered or aggregated data used.
- An interactive chart illustrating the specific comparisons.


Sample Output
  Status: Success
  Result Table:
    Region: North | Total_Sales: $10,400
    Region: East | Total_Sales: $9,100
  Chart: Bar chart showing Region on X-axis and Total_Sales on Y-axis.



Workflow Structure
- File upload -> CSV validation -> Data and schema analysis -> Query (User Enters Question) -> Intelligent agent decision  -> Pandas operations execution -> Result and chart display.


Alternative Paths:
-Invalid/empty file: Display error message and halt the process.[ prevent in code]
-Ambiguous query (e.g., "What is the best product?"): The agent halts execution and requests clarification of the criterion (best in terms of revenue or sales volume?).
-Out-of-Scope/Missing Column: Displays explicit user error message.

Agent Specification

-1. Goal: Interpret data-related questions and translate them into precise Pandas operations without executing unsafe code.

-2. Available Actions:
-load_and_preview
-ask_clarification
-generate_code (Filter, GroupBy, Aggregate, Sort), & charts
-out_of_scope

-3. State Variables
df: csv data file.
schema: Column names and types.
chat_history: Record of questions and answers.


-4. Decision Rules:
These are the conditions and criteria followed by the intelligent agent to decide on the next action.
Example:

Rule 1: If the question contains the word "best" or "highest" without specifying the metric (e.g., revenue, quantity, number of orders)
-> Decision: Ask the user for clarification.

Rule 2: If the user requests information from a column not present in the schema 
-> Decision: Display an error message stating that the column does not exist.

Rule 3: If the question is clear and direct
-> Decision: Select the appropriate analysis tool and execute the operation.



Example permissions:
Allowed: Reading the uploaded CSV file only.
Allowed: Executing specific aggregation and data manipulation functions from the Pandas library, such as df.groupby(), df.sum(), df.mean(), and df.filter().
Prohibited: Modifying the original file, executing system commands, or running unverified dynamic Python code.

Sample Data 

Number of rows: 35 rows.

Available columns:
Order_ID: Order number
Order_Date: Order date
Customer_Type: Customer type (Corporate, Consumer, Home Office)
Region: Region (North, South, East, West)
Category: Category (Electronics, Furniture, Office Supplies)
Product: Product name (Laptop, Smartphone, Desk, Monitor...)
Quantity: Quantity sold
Price: Unit price
Total_Sales: Total sales (Quantity x Price)



Interface Sketch
-Main Screen (Streamlit Layout):
--Sidebar: 
---CSV file upload button + file information display (number of rows and columns).
--- history 
--Main Area:
---App title and brief description.
---Text input box for questions (Chat Input / Text Box).
---Area for displaying text answers, clarifications, or error messages.
---Area for displaying the helper table and charts.


Success Tests
T1: Uploading the file sales_data.csv was successful. 
   -- Successfully displayed a preview of the first 5 rows and the total row/column count.

T2: Clear question: "What are the total sales per region?" 
   -- Calculated the total using groupby and displayed the answer with a bar chart.

T3: Ambiguous question: "What is the best product?" 
   --Requested clarification: "Do you mean the product with the highest revenue or the highest sales volume?"

T4: Question about a non-existent column: "What is the customer name?" 
   -- Displayed an alert stating that the Customer Name column does not exist in the data.

T5: Uploading an invalid file (empty text file or non-CSV format). 
   -- Displayed a clear error message requesting the upload of a valid CSV file.


Technology Plan
-Prerequisites: 
Python fundamentals and intelligent agent State concepts (Session 16).
Pandas: For data handling and performing statistical operations.
Plotly Express: For generating interactive charts.

-Tools for self-learning:
--Streamlit: For building the interface, displaying tables, and utilizing st.session_state.


Build Order
-Minimum Viable Product (MVP):
-- Build a simple Streamlit interface with a CSV file upload button and a preview feature.
-- Implement a function to accept queries and perform basic Pandas operations.
-- Display text-based results for direct queries.

-Enhancements and Additions:
--Add logic to clarify ambiguous questions.
--Integrate interactive charts using Plotly.
--Manage st.session_state to maintain conversation history.