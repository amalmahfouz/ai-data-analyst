
# from openai import OpenAI
# from openai import OpenAI
# from config import BASE_URL, HF_API_KEY, MAX_TOKENS, MODEL_NAME, TEMPERATURE

# if not HF_API_KEY:
#   raise ValueError("problem with API_KEY in .env")
  

# client = OpenAI(base_url=BASE_URL, api_key=HF_API_KEY,)

# def ask_llm(system_prompt, user_prompt):
#     try:
#         completion = client.chat.completions.create(model=MODEL_NAME,
#             messages=[
#                 {
#                     "role": "system",
#                     "content": system_prompt
#                 },
#                 {
#                     "role": "user",
#                     "content": user_prompt
#                 }
#             ],
#             temperature=TEMPERATURE,
#             max_tokens=MAX_TOKENS,
#         )
#         return completion.choices[0].message.content
#     except Exception as e:
#        print(f"model connection failed {e}")
#        return f"ERROR: failed connection model - {str(e)}"



import time
from openai import OpenAI
from config import BASE_URL, HF_API_KEY, MAX_TOKENS, MODEL_NAME, TEMPERATURE

if not HF_API_KEY:
    raise ValueError("Problem with GROQ_API_KEY in .env")

client = OpenAI(
    base_url=BASE_URL,
    api_key=HF_API_KEY,
)

def ask_llm(system_prompt: str, user_prompt: str):
    start_time = time.time()
    try:
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
        )
        latency = round(time.time() - start_time, 2)
        # استخراج التوكينات بأمان من القاموس أو الكائن
        usage = getattr(completion, "usage", None)
        if usage:
            prompt_tokens = getattr(usage, "prompt_tokens", 0) or 0
            completion_tokens = getattr(usage, "completion_tokens", 0) or 0
            total_tokens = getattr(usage, "total_tokens", 0) or (prompt_tokens + completion_tokens)
        else:
            prompt_tokens, completion_tokens, total_tokens = 0, 0, 0
        
        response_text = completion.choices[0].message.content
        
        metadata = {
            "latency_sec": latency,
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": total_tokens
        }
        
        return response_text, metadata

    except Exception as e:
        latency = round(time.time() - start_time, 2)
        print(f"model connection failed {e}")
        return f"ERROR: failed connection model - {str(e)}", {
            "latency_sec": latency,
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0
        }