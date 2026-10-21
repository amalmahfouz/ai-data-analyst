# import pandas as pd
# from helper import execute_pandas_code, generate_auto_chart, parse_json_response
# from llm import ask_llm
# from prompts import build_code_prompt, build_intent_prompt


# def process_user_query(question: str, df: pd.DataFrame) -> dict:
#   if df is None or df.empty:
#     return {
#         "status": "error",
#         "action": "out_of_scope",
#         "message": "error empty file cvs",
#         "result": None,
#         "chart": None,
#         "code_executed": None,
#     }


#   system_intent_prompt, user_intent_prompt = build_intent_prompt(question, df)
#   intent_response_raw = ask_llm(system_intent_prompt, user_intent_prompt)
#   intent_data = parse_json_response(intent_response_raw)

#   action = intent_data.get("action", "out_of_scope")

#   if action == "ask_clarification":
#     return {
#         "status": "clarification",
#         "action": "ask_clarification",
#         "message": intent_data.get(
#             "clarification_question",
#             "The question is unclear; please provide more details.",
#         ),
#         "result": None,
#         "chart": None,
#         "code_executed": None,
#     }

#   elif action == "out_of_scope":
#     return {
#         "status": "error",
#         "action": "out_of_scope",
#         "message": intent_data.get(
#             "error_message",
#             "Sorry, this question cannot be answered based on the available data.",
#         ),
#         "result": None,
#         "chart": None,
#         "code_executed": None,
#     }

#   elif action == "generate_code":
#     system_code_prompt, user_code_prompt = build_code_prompt(question, df)
#     generated_code_raw = ask_llm(system_code_prompt, user_code_prompt)
#     success, result, cleaned_code = execute_pandas_code(generated_code_raw, df)

#     if not success:
#       return {
#           "status": "error",
#           "action": "execution_error",
#           "message": f"error in executed query     : {result}",
#           "result": None,
#           "chart": None,
#           "code_executed": cleaned_code,
#       }

#     if result is None:
#       return {
#           "status": "error",
#           "action": "no_result",
#           "message": (
#               "We were unable to derive a result from this question based on the current data columns."
#           ),
#           "result": None,
#           "chart": None,
#           "code_executed": cleaned_code,
#       }

   
#     chart = generate_auto_chart(df, result)

#     return {
#         "status": "success",
#         "action": "generate_code",
#         "message": "تم تحليل البيانات بنجاح!",
#         "result": result,
#         "chart": chart,
#         "code_executed": cleaned_code,
#     }

#   return {
#       "status": "error",
#       "action": "unknown",
#       "message": "حدث خطأ غير متوقع أثناء معالجة السؤال.",
#       "result": None,
#       "chart": None,
#       "code_executed": None,
#   }

# import pandas as pd
# from helper import execute_pandas_code, generate_auto_chart, parse_json_response
# from llm import ask_llm
# from prompts import build_code_prompt, build_intent_prompt


# def process_user_query(question: str, df: pd.DataFrame, chat_history: list = None) -> dict:
#     if df is None or df.empty:
#         return {
#             "status": "error",
#             "action": "out_of_scope",
#             "message": "error empty file csv",
#             "result": None,
#             "chart": None,
#             "code_executed": None,
#         }

#     system_intent_prompt, user_intent_prompt = build_intent_prompt(question, df, chat_history)
#     intent_response_raw = ask_llm(system_intent_prompt, user_intent_prompt)

   
#     intent_data = parse_json_response(intent_response_raw)

   

#     action = intent_data.get("action", "out_of_scope")

#     if action == "ask_clarification":
#         return {
#             "status": "clarification",
#             "action": "ask_clarification",
#             "message": intent_data.get(
#                 "clarification_question",
#                 "The question is unclear; please provide more details.",
#             ),
#             "result": None,
#             "chart": None,
#             "code_executed": None,
#         }

#     elif action == "out_of_scope":
#         return {
#             "status": "error",
#             "action": "out_of_scope",
#             "message": intent_data.get(
#                 "error_message",
#                 "Sorry, this question cannot be answered based on the available data.",
#             ),
#             "result": None,
#             "chart": None,
#             "code_executed": None,
#         }

#     elif action == "generate_code":
#         system_code_prompt, user_code_prompt = build_code_prompt(question, df, chat_history)
#         generated_code_raw = ask_llm(system_code_prompt, user_code_prompt)
#         success, result, cleaned_code = execute_pandas_code(generated_code_raw, df)

#         if not success:
#             return {
#                 "status": "error",
#                 "action": "execution_error",
#                 "message": f"error in executed query : {result}",
#                 "result": None,
#                 "chart": None,
#                 "code_executed": cleaned_code,
#             }

#         if result is None:
#             return {
#                 "status": "error",
#                 "action": "no_result",
#                 "message": (
#                     "We were unable to derive a result from this question based on the current data columns."
#                 ),
#                 "result": None,
#                 "chart": None,
#                 "code_executed": cleaned_code,
#             }

#         chart = generate_auto_chart(df, result)

#         return {
#             "status": "success",
#             "action": "generate_code",
#             "message": "تم تحليل البيانات بنجاح!",
#             "result": result,
#             "chart": chart,
#             "code_executed": cleaned_code,
#         }

#     return {
#         "status": "error",
#         "action": "unknown",
#         "message": "حدث خطأ غير متوقع أثناء معالجة السؤال.",
#         "result": None,
#         "chart": None,
#         "code_executed": None,
#     }\
import pandas as pd
from helper import execute_pandas_code, generate_auto_chart, parse_json_response
from llm import ask_llm
from prompts import build_code_prompt, build_intent_prompt

def process_user_query(question: str, df: pd.DataFrame, chat_history: list = None) -> dict:
    if df is None or df.empty:
        return {
            "status": "error",
            "action": "out_of_scope",
            "message": "error empty file csv",
            "result": None,
            "chart": None,
            "code_executed": None,
            "metrics": {"total_tokens": 0, "latency_sec": 0, "prompt_tokens": 0, "completion_tokens": 0}
        }

    system_intent_prompt, user_intent_prompt = build_intent_prompt(question, df, chat_history)
    intent_response_raw, intent_meta = ask_llm(system_intent_prompt, user_intent_prompt)
    intent_data = parse_json_response(intent_response_raw)

    total_prompt_tokens = intent_meta["prompt_tokens"]
    total_completion_tokens = intent_meta["completion_tokens"]
    total_latency = intent_meta["latency_sec"]

    action = intent_data.get("action", "out_of_scope")

    if action in ["ask_clarification", "out_of_scope"]:
        msg = (
            intent_data.get("clarification_question", "The question is unclear; please provide more details.")
            if action == "ask_clarification"
            else intent_data.get("error_message", "Sorry, this question cannot be answered based on the available data.")
        )
        return {
            "status": "clarification" if action == "ask_clarification" else "error",
            "action": action,
            "message": msg,
            "result": None,
            "chart": None,
            "code_executed": None,
            "metrics": {
                "total_tokens": total_prompt_tokens + total_completion_tokens,
                "prompt_tokens": total_prompt_tokens,
                "completion_tokens": total_completion_tokens,
                "latency_sec": round(total_latency, 2)
            }
        }

    elif action == "generate_code":
        # 2. طلب توليد الكود (Code Generation)
        system_code_prompt, user_code_prompt = build_code_prompt(question, df, chat_history)
        generated_code_raw, code_meta = ask_llm(system_code_prompt, user_code_prompt)
        
        total_prompt_tokens += code_meta["prompt_tokens"]
        total_completion_tokens += code_meta["completion_tokens"]
        total_latency += code_meta["latency_sec"]
        
        success, result, cleaned_code = execute_pandas_code(generated_code_raw, df)

        metrics = {
            "total_tokens": total_prompt_tokens + total_completion_tokens,
            "prompt_tokens": total_prompt_tokens,
            "completion_tokens": total_completion_tokens,
            "latency_sec": round(total_latency, 2)
        }

        if not success:
            return {
                "status": "error",
                "action": "execution_error",
                "message": f"error in executed query : {result}",
                "result": None,
                "chart": None,
                "code_executed": cleaned_code,
                "metrics": metrics
            }

        if result is None:
            return {
                "status": "error",
                "action": "no_result",
                "message": "We were unable to derive a result from this question based on the current data columns.",
                "result": None,
                "chart": None,
                "code_executed": cleaned_code,
                "metrics": metrics
            }

        chart = generate_auto_chart(df, result)

        return {
            "status": "success",
            "action": "generate_code",
            "message": "تم تحليل البيانات بنجاح!",
            "result": result,
            "chart": chart,
            "code_executed": cleaned_code,
            "metrics": metrics
        }

    return {
        "status": "error",
        "action": "unknown",
        "message": "حدث خطأ غير متوقع أثناء معالجة السؤال.",
        "result": None,
        "chart": None,
        "code_executed": None,
        "metrics": {"total_tokens": 0, "latency_sec": 0, "prompt_tokens": 0, "completion_tokens": 0}
    }