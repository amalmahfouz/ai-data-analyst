import json
import re
import pandas as pd
import plotly.express as px
import ast 


BLOCKED_KEYWORDS = [
    r"\bimport\b", r"\bfrom\b", r"\beval\b", r"\bexec\b",
    r"\bopen\b", r"\bos\b", r"\bsys\b", r"\bsubprocess\b",
    r"\b__import__\b", r"\bbuiltins\b", r"\bglobals\b", r"\blocals\b"
]

def validate_code_safety(code_str: str) -> tuple[bool, str]:
   
    if not code_str or not code_str.strip():
        return False, "Code string is empty."

    for pattern in BLOCKED_KEYWORDS:
        if re.search(pattern, code_str, re.IGNORECASE):
            match = re.search(pattern, code_str, re.IGNORECASE).group(0)
            return False, f"Security Violation: Forbidden keyword or operation detected ('{match}')."

    try:
        parsed_ast = ast.parse(code_str)
        for node in ast.walk(parsed_ast):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                return False, "Security Violation: Importing modules is strictly forbidden."
            
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name) and node.func.id in ["eval", "exec", "open", "__import__", "input"]:
                    return False, f"Security Violation: Function '{node.func.id}' is not allowed."
                    
    except SyntaxError as e:
        return False, f"Syntax Error in generated code: {str(e)}"

    return True, "Code is safe."



def clean_python_code(code_str: str) -> str:
  if not code_str:
    return ""

  cleaned = re.sub(r"```(?:python)?", "", code_str, flags=re.IGNORECASE)
  cleaned = cleaned.replace("```", "").strip()
  return cleaned



def parse_json_response(response_str: str) -> dict:
    try:
        # استخراج النص الموجود بين أول { وآخر }
        match = re.search(r'\{.*\}', response_str, re.DOTALL)
        if match:
            json_str = match.group(0)
            return json.loads(json_str)
        else:
            raise ValueError("No JSON object found in the response")
    except Exception as e:
        return { 
            "action": "out_of_scope",
            "reason": f" failed of analysis JSON   : {str(e)}",
            "clarification_question": None,
            "error_message": (
                " try again , error with json"
            ),
        }


def execute_pandas_code(code_str: str, df: pd.DataFrame):
  cleaned_code = clean_python_code(code_str)

    # فحص الأمان قبل التنفيذ
  is_safe, safety_msg = validate_code_safety(cleaned_code)
  if not is_safe:
        return False, f"Security Guardrail Triggered: {safety_msg}", cleaned_code


  local_vars = {"__builtins__": {},"df": df.copy(), "pd": pd,}

  try:
    exec(cleaned_code, {}, local_vars)
    result = local_vars.get("result", None)
    return True, result, cleaned_code
  except Exception as e:
    return False, str(e), cleaned_code


def generate_auto_chart(df: pd.DataFrame, result):
  try:
    # Bar chart or Scatter plot
    if isinstance(result, pd.DataFrame):
      cols = list(result.columns)
      if len(cols) >= 2:
        num_cols = result.select_dtypes(include=["number"]).columns.tolist()
        cat_cols = result.select_dtypes(include=["object", "category"]).columns.tolist()

        if num_cols and cat_cols: #str, number
          fig = px.bar(
              result,
              x=cat_cols[0],
              y=num_cols[0],
              title=f"{num_cols[0]} According to {cat_cols[0]}",
              text_auto=True,
          )
          return fig
        elif len(num_cols) >= 2: #Scatter Plot , numbers columns
          fig = px.scatter(
              result,
              x=num_cols[0],
              y=num_cols[1],
              title=f"compare {num_cols[0]} with {num_cols[1]}",
          )
          return fig

    elif isinstance(result, pd.Series):
      res_df = result.reset_index() #convert to dataframe
      cols = list(res_df.columns)
      fig = px.bar(
          res_df,
          x=cols[0],
          y=cols[1],
          title=f"{cols[1]} according to {cols[0]}",
          text_auto=True,
      )
      return fig

  except Exception as e:
    print(f"error with drawing charts: {e}")

  return None



def generate_markdown_report(chat_history: list, file_name: str = None) -> str:
    report = []
    report.append("# AI Data Analyst Report")
    if file_name:
        report.append(f"**Analyzed File:** `{file_name}`")
    report.append(f"**Total Questions Handled:** {len(chat_history)}")
    report.append("\n---\n")

    for i, chat in enumerate(chat_history, 1):
        q = chat.get("question", "")
        res = chat.get("response", {})
        status = res.get("status", "unknown")
        msg = res.get("message", "")
        code = res.get("code_executed", "")
        metrics = res.get("metrics", {})

        report.append(f"## Question {i}: {q}")
        report.append(f"- **Status:** `{status}`")
        if msg:
            report.append(f"- **Summary/Message:** {msg}")
        
        if code:
            report.append("\n### Executed Code:")
            report.append(f"```python\n{code}\n```")

        # إضافة نتيجة البيانات إن وجدت
        result_data = res.get("result")
        if result_data is not None:
            report.append("\n### Result Data:")
            try:
                # محاولة استخدام to_markdown في حال كانت مثبتة، وإلا استخدام تحويل بسيط
                if hasattr(result_data, "to_markdown"):
                    try:
                        report.append(result_data.to_markdown())
                    except ImportError:
                        report.append(f"```\n{result_data.to_string()}\n```")
                else:
                    report.append(f"**Value:** {result_data}")
            except Exception:
                report.append(f"**Value:** {str(result_data)}")

        if metrics:
            report.append(
                f"\n> ⏱️ **Latency:** {metrics.get('latency_sec', 0)}s | "
                f"🔢 **Total Tokens:** {metrics.get('total_tokens', 0)}"
            )

        report.append("\n---\n")

    return "\n".join(report)



def inspect_and_clean_data(df: pd.DataFrame):
    df_cleaned = df.copy()

    # 1. إزالة التكرارات
    duplicate_count = df_cleaned.duplicated().sum()
    if duplicate_count > 0:
        df_cleaned = df_cleaned.drop_duplicates()

    # 2. التحويل التلقائي للأعمدة النصية التي تحتوي على أرقام
    for col in df_cleaned.columns:
        if df_cleaned[col].dtype == "object":
            # تنظيف الرموز النصية الشائعة (مثل $ و , والمسافات)
            cleaned_series = (
                df_cleaned[col]
                .astype(str)
                .str.replace(r'[\$,]', '', regex=True)
                .str.strip()
            )

            # تحويل القيم إلى أرقام، والقيم النصية غير الرقمية تصبح NaN
            converted_numeric = pd.to_numeric(cleaned_series, errors="coerce")

            # إذا نجح تحويل أكثر من 50% من القيم إلى أرقام، يتم اعتماد العمود كعمود رقمي
            if converted_numeric.notnull().sum() > (0.5 * len(df_cleaned)):
                df_cleaned[col] = converted_numeric

    # 3. التحويل الذكي للتواريخ
    for col in df_cleaned.columns:
        if df_cleaned[col].dtype == "object":
            try:
                converted_dates = pd.to_datetime(
                    df_cleaned[col], errors="coerce", format="mixed"
                )
                if converted_dates.notnull().sum() > (0.8 * len(df_cleaned)):
                    df_cleaned[col] = converted_dates
            except Exception:
                pass

    missing_summary = df_cleaned.isnull().sum()[df_cleaned.isnull().sum() > 0].to_dict()

    return df_cleaned, duplicate_count, missing_summary