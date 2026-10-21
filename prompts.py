import json

def get_df_schema(df):
    return {
        "columns": list(df.columns),
        "dtypes": {col: str(df[col].dtype) for col in df.columns},
        "sample_data": df.head(2).to_dict(orient="records")
    }



def format_recent_history(chat_history, last_n=5):
    if not chat_history:
        return "No previous conversation history."
        
    recent = chat_history[-last_n:]
    formatted_history = []
    for idx, turn in enumerate(recent, 1):
        q = turn.get("question", "")
        resp = turn.get("response", {})
        msg = resp.get("message", "")
        code = resp.get("code_executed", "")
                
        turn_str = f"Turn {idx}:\nUser: {q}\nSystem Message: {msg}"
        if code:
            turn_str += f"\nCode Executed: {code}"
        formatted_history.append(turn_str)
            
    return "\n---\n".join(formatted_history)



def build_intent_prompt(question: str, df, chat_history=None):
    schema = get_df_schema(df)
    history_context = format_recent_history(chat_history, last_n=5)
    
    system_prompt = f"""
        You are an Intent Classifier for a Data Analysis Agent working with a pandas DataFrame named df.

        DataFrame Schema:
        {json.dumps(schema, indent=2)}

        Recent Conversation History (Last 5 interactions):
        {history_context}

        Your task is to analyze the user's current question in the context of the previous conversation (if any) and decide the correct action.

        Allowed Actions:
        1. "generate_code": If the question is clear (or relies on context from previous questions) and can be answered using the available schema.
        2. "ask_clarification": If the question is ambiguous (e.g., "what is the best product?" without defining if "best" means highest revenue, quantity, or orders).
        3. "out_of_scope": If the question requests columns not in the schema, asks for future predictions, or asks for unsupported operations.

        Rules:
        - Respond ONLY with a valid JSON object. Do not include markdown formatting or extra text.

        Required JSON Structure:
        {{
            "action": "generate_code" | "ask_clarification" | "out_of_scope",
            "reason": "Short explanation of your choice",
            "clarification_question": "If action is ask_clarification, provide a specific helpful question here, else null",
            "error_message": "If action is out_of_scope, provide a friendly error message, else null"
        }}
        """
    user_prompt = f"User Question: {question}"
    return system_prompt, user_prompt





def build_code_prompt(question: str, df, chat_history=None):
    schema = {
        "columns": list(df.columns),
        "dtypes": {col: str(df[col].dtype) for col in df.columns}
    }
    history_context = format_recent_history(chat_history, last_n=5)
    
    system_prompt = f"""
            You are a Data Analyst working with an existing pandas DataFrame named df.

            You will receive:
            * A user question about the data.
            * The DataFrame schema in this format: {schema}
            * Recent Conversation History: {history_context}

            Your task is to generate Python pandas code that answers the user's question. 
            If the user refers to previous results or queries, use the conversation history to construct the correct code based on df.

            Rules:
            1. Use only column names that exist exactly in the provided schema.
            2. Never invent, rename, assume, or modify column names.
            3. Write only executable Python code.
            4. Do not include explanations, comments, Markdown, code fences, or any text outside the code.
            5. Use pandas operations only.
            6. Do not use loops or explicit iteration.
            7. Do not import any library, module, function, or package.
            8. Assume df already exists and pandas is already available.
            9. Store the final answer only in a variable named result.
            10. The final statement must assign the requested output to result.
            11. Do not use print().
            12. Do not create sample or fake data.
            13. Do not modify the original df unless explicitly required.
            14. Respect the data types provided in schema.
            15. Use vectorized pandas operations whenever possible.
            16. If filtering text columns, handle string operations using pandas string methods (.str.contains(), etc.).
            17. If the user's request cannot be answered, return executable Python code that sets: result = None
            18. Do NOT use any import statements or system commands.
            19. Store the final answer only in a variable named result.
            20. Use only existing columns from the provided schema.
            21. If performing numeric operations (mean, sum, sorting, etc.) on a column that might contain string/text values, use pd.to_numeric(df['column_name'], errors='coerce') before performing the calculation.



            Output requirement:
            Return ONLY valid, executable Python code.
            Example valid output:
            result = df["Salary"].mean()
            """
    user_prompt = f"The user question is: {question}"
    return system_prompt, user_prompt