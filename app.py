import os
import pandas as pd
import streamlit as st
import uuid
from full_system import process_user_query
from helper import inspect_and_clean_data, generate_markdown_report

st.set_page_config(
    page_title="AI Data Analyst",
    layout="wide",
)


st.markdown("""
            <style>
                .stButton button, div[data-testid="stFileUploader"] button {
                    border-color: #2563eb !important;
                    color: #2563eb !important;
                }
                .stButton button:hover, div[data-testid="stFileUploader"] button:hover {
                    background-color: #2563eb !important;
                    color: white !important;
                }

                div[data-testid="stToast"] {
                background-color: #f0fdf4 !important; /* خلفية خضراء فاتحة ناعمة */
                border: 1px solid #22c55e !important; /* إطار أخضر */
                color: #15803d !important; /* لون النص أخضر داكن */
                border-radius: 8px !important;
                }

                div[data-testid="stMetric"] {
                background-color: #e0f2fe; /* لون أزرق فاتح جداً */
                border: 1px solid #bae6fd; /* حدود زرقاء متناسقة */
                border-radius: 10px;       /* زوايا دائرية */
                padding: 15px;             /* مسافة داخلية */
                box-shadow: 0 2px 4px rgba(0,0,0,0.05); /* ظل خفيف */
                text-align: center;        /* توسيط النص */
            }

            div[data-testid="stChatInput"] {
                border-radius: 15px !important;
            }

            /* تغيير لون الحدود عند النقر (Focus) إلى الأزرق */
            div[data-testid="stChatInput"] > div:focus-within {
                border-color: #2563eb !important;
                box-shadow: 0 0 0 1px #2563eb !important;
            }

            /* تغيير لون أيقونة الإرسال إلى الأزرق */
            div[data-testid="stChatInput"] button {
                color: #ffffff !important;
            }

            /* تغيير لون الأيقونة عند تمرير الماوس (Hover) */
            div[data-testid="stChatInput"] button:hover {
                color: #1e40af !important; /* أزرق غامق */
                background-color: #eff6ff !important; /* خلفية زرقاء خفيفة جداً */
            }

                div[data-testid="stToast"] div {
                   color: #15803d !important;
                }
            </style>
        """, unsafe_allow_html=True)

st.title("AI Data Analyst System")
st.caption("Upload a CSV file and explore your data using natural language, no coding required ..." )

if "df" not in st.session_state:
    st.session_state.df = None



if "file_name" not in st.session_state:
    st.session_state.file_name = None

if "sessions" not in st.session_state:
    st.session_state.sessions = {}

if "current_session_id" not in st.session_state:
    st.session_state.current_session_id = None

def create_new_session():
    new_id = str(uuid.uuid4())[:8]
    st.session_state.sessions[new_id] = {
        "title": f"New Chat ({new_id})",
        "df": None,
        "file_name": None,
        "chat_history": [],
        "dup_count": 0,
        "missing_info": {}
    }
    st.session_state.current_session_id = new_id

if not st.session_state.sessions:
    create_new_session()

current_id = st.session_state.current_session_id
current_session = st.session_state.sessions[current_id]



with st.sidebar:
    st.header("Load Data File")
    uploaded_file = st.file_uploader("choose file .CSV", type=["csv"], key=f"uploader_{current_id}")
    
    if uploaded_file is not None:
            if current_session["file_name"] != uploaded_file.name:
                try:
                    df = pd.read_csv(uploaded_file)
                    if df.empty:
                        st.error("Warning: file is empty ..")
                    else:
                        df_cleaned, dup_count, missing_info = inspect_and_clean_data(df)
                        current_session["df"] = df_cleaned
                        current_session["file_name"] = uploaded_file.name
                        current_session["dup_count"] = dup_count
                        current_session["missing_info"] = missing_info
                        current_session["title"] = f" {uploaded_file.name[:15]}"
                        current_session["chat_history"] = []
                        # st.success(f"Loaded File {uploaded_file.name} Successfully!")
                        # st.rerun()
                        st.toast(f"Loaded File {uploaded_file.name} Successfully!", icon="✅")
                        st.rerun()  
                except Exception as e:
                    st.error(f"Error While Reading File : {e}")


    st.divider()
    st.header(" All Conversations")
    if st.button("+  New Chat", use_container_width=True):
        create_new_session()
        st.rerun()

   
    st.subheader("History Chats")
    for sess_id, sess_data in list(st.session_state.sessions.items()):
        col1, col2 = st.columns([0.8, 0.2])
        is_active = (sess_id == current_id)
        btn_label = sess_data['title']
        active_icon = ":material/chevron_right:" if is_active else None
        
        with col1:
            if st.button(btn_label, icon=active_icon, key=f"select_{sess_id}", use_container_width=True):
                st.session_state.current_session_id = sess_id
                st.rerun()
        with col2:
            if st.button("", icon=":material/delete:", key=f"del_{sess_id}", help="Delete chat"):
                del st.session_state.sessions[sess_id]
                if st.session_state.current_session_id == sess_id:
                    remaining_ids = list(st.session_state.sessions.keys())
                    st.session_state.current_session_id = remaining_ids[0] if remaining_ids else None
                st.rerun()

    
   

    if current_session["df"] is not None:
        if st.button("Clear Data and history", use_container_width=True):
            current_session["df"] = None
            current_session["chat_history"] = []
            current_session["file_name"] = None
            current_session["title"] = f"New Chat ({current_id})"
            st.rerun()

    
    if current_session["chat_history"]:
        st.divider()
        st.header("Export Report")
        markdown_content = generate_markdown_report(
            current_session["chat_history"], 
            current_session["file_name"]
        )
        st.download_button(
            label=" Download Report (.md)",
            data=markdown_content,
            file_name=f"analysis_report_{current_session['file_name'] or 'data'}.md",
            mime="text/markdown",
            use_container_width=True
        )

    st.divider()
    st.header("Last Questions: ")
    if current_session["chat_history"]:
        for i, chat in enumerate(reversed(current_session["chat_history"])):
            status = chat['response']['status']
            if status == "success":
                status_badge = " **Status:** Success"
            else:
                status_badge = " **Status:** " + status.capitalize()

            with st.expander(f"Question {len(current_session['chat_history']) - i}: {chat['question'][:25]}..."):
                st.write(f"**Q:** {chat['question']}")
                st.markdown(status_badge)
                if chat['response']['message']:
                    st.write(f"**Result:** {chat['response']['message']}")
    else:
        st.info("No Questions Yet ....")


if current_session["df"] is None:
    st.info("Please upload a CSV file from the sidebar to start the analysis.")
else:
   
    with st.expander("Preview the first 5 rows of the uploaded data", expanded=True):
        st.dataframe(current_session["df"].head(5), width="stretch")

    st.markdown("### Description File & Quality :")
    col_desc1, col_desc2, col_desc3 = st.columns(3)
    col_desc1.metric("Rows Count", f"{current_session['df'].shape[0]:,}")
    col_desc2.metric("Columns Count", f"{current_session['df'].shape[1]:,}")
    col_desc3.metric("Duplicates Removed", f"{current_session['dup_count']:,}")

    columns_with_types = [f"{col} ({df_col_dtype})" for col, df_col_dtype in current_session["df"].dtypes.items()]
    st.caption("**Columns & Types:** " + ", ".join(columns_with_types))

    if current_session["missing_info"]:
        with st.expander("⚠️ Data Quality - Missing Values Info", expanded=False):
            st.info("Missing values by column:")
            for col, count in current_session["missing_info"].items():
                st.write(f"- Column **{col}**: has **{count}** missing values")

    st.divider()

  
    for chat in current_session["chat_history"]:
        with st.chat_message("user", avatar="👤"):
            st.write(chat["question"])

        with st.chat_message("assistant", avatar=":material/psychology:"):
            res = chat["response"]
            metrics = res.get("metrics", {})

            if res["status"] == "success":
                st.success(res["message"])

                if res["code_executed"]:
                    with st.expander("Show executed Pandas code"):
                        st.code(res["code_executed"], language="python")

                if isinstance(res["result"], (pd.DataFrame, pd.Series)):
                    st.dataframe(res["result"], width="stretch")
                elif res["result"] is not None:
                    st.metric(label="Result", value=str(res["result"]))

                if res["chart"] is not None:
                    st.plotly_chart(res["chart"], width="stretch")

            elif res["status"] == "clarification":
                st.warning(f"Clarification of the requirement: {res['message']}")

            elif res["status"] == "error":
                st.error(f"{res['message']}")

            if metrics:
                st.caption(
                    f"⏱️ **Latency:** {metrics.get('latency_sec', 0)}s | "
                    f"🔢 **Tokens:** {metrics.get('total_tokens', 0)} "
                    f"(Prompt: {metrics.get('prompt_tokens', 0)}, Completion: {metrics.get('completion_tokens', 0)})"
                )

    user_question = st.chat_input("Ask a question about your data (e.g., What are the total sales by region?)...")

    if user_question:
        with st.chat_message("user", avatar="👤"):
            st.write(user_question)

        with st.chat_message("assistant", avatar=":material/psychology:"):
            with st.spinner("Data is being analyzed and a decision is being made..."):
                response = process_user_query(
                    user_question, 
                    current_session["df"], 
                    current_session["chat_history"]
                )
                current_session["chat_history"].append({
                    "question": user_question,
                    "response": response,
                })
                st.rerun()


# with st.sidebar:
#     st.header("Load Data File")
#     uploaded_file = st.file_uploader("choose file .CSV", type=["csv"])

#     if uploaded_file is not None:
#         if st.session_state.file_name != uploaded_file.name:
#             try:
#                 df = pd.read_csv(uploaded_file)
#                 if df.empty:
#                     st.error("Warning: file is empty ..")
#                 else:
#                     st.session_state.df = df
#                     st.session_state.file_name = uploaded_file.name
#                     st.session_state.chat_history = [] 
#                     st.success(f"Loaded File {uploaded_file.name} Successfully!")
#             except Exception as e:
#                 st.error(f"Error While Reading File : {e}")

#     if st.session_state.df is not None:
#         st.divider()
#         st.subheader("Description File:" )
#         st.write(f"Rows:  {st.session_state.df.shape[0]}")
#         st.write(f"Columns:  {st.session_state.df.shape[1]}")
#         st.write("Columns Name:")
#         st.caption(", ".join(st.session_state.df.columns))
#         df_cleaned, dup_count, missing_info = inspect_and_clean_data(st.session_state.df)
#         st.session_state.df = df_cleaned
#         if dup_count > 0 or missing_info:
#          with st.sidebar.expander(" Data Quality"):
#             if dup_count > 0:
#              st.warning(f"Discovered and removed   {dup_count} Duplicate rows")
#             if missing_info:
#              st.info("Missing values by row number:")
#             for col, count in missing_info.items():
#               st.write(f"- column {col}: have {count} missing value")

#         if st.button("Clear Data and history"):
#             st.session_state.df = None
#             st.session_state.chat_history = []
#             st.session_state.file_name = None
#             st.rerun()

#     st.divider()
#     st.header("📊 Usage & Metrics")
#     if st.session_state.chat_history:
#         total_session_tokens = sum(
#             chat["response"].get("metrics", {}).get("total_tokens", 0) 
#             for chat in st.session_state.chat_history
#         )
#         total_session_latency = sum(
#             chat["response"].get("metrics", {}).get("latency_sec", 0) 
#             for chat in st.session_state.chat_history
#         )
        
#         st.metric("Total Session Tokens", f"{total_session_tokens:,}")
#         st.metric("Total Response Time", f"{total_session_latency:.2f} s")
#     else:
#         st.caption("No requests recorded yet.")


#     # إضافة زر تصدير التقرير في القائمة الجانبية
#     if st.session_state.chat_history:
#         st.divider()
#         st.header("📥 Export Report")
        
#         # توليد محتوى التقرير
#         markdown_content = generate_markdown_report(
#             st.session_state.chat_history, 
#             st.session_state.file_name
#         )
        
#         # زر التنزيل في Streamlit
#         st.download_button(
#             label="📄 Download Report (.md)",
#             data=markdown_content,
#             file_name=f"analysis_report_{st.session_state.file_name or 'data'}.md",
#             mime="text/markdown",
#             use_container_width=True
#         )

#     st.header("Last Questions: ")
#     if st.session_state.chat_history:
#         for i, chat in enumerate(reversed(st.session_state.chat_history)):
#             status = chat['response']['status']
            
#             if status == "success":
#                 status_badge = " **Status:** Success"
#             else:
#                 status_badge = " **Status:** " + status.capitalize()

#             with st.expander(f"Question {len(st.session_state.chat_history) - i}: {chat['question'][:25]}..."):
#                 st.write(f"**Q:** {chat['question']}")
#                 st.markdown(status_badge)
#                 if chat['response']['message']:
#                     st.write(f"**Result:** {chat['response']['message']}")
#     else:
#         st.info("No Questions Yet ....")

# # Main Area) 
# if st.session_state.df is None:
#     st.info("Please upload a CSV file from the sidebar to start the analysis.")
# else:
#     with st.expander("Preview the first 5 rows of the uploaded data", expanded=True):
#         st.dataframe(st.session_state.df.head(5), use_container_width=True)

#     st.divider()
#     for chat in st.session_state.chat_history:
#         with st.chat_message("user"):
#             st.write(chat["question"])

#         with st.chat_message("assistant"):
#             res = chat["response"]

#             metrics = res.get("metrics", {})

#             if res["status"] == "success":
#                 st.success(res["message"])

#                 if res["code_executed"]:
#                     with st.expander("Show executed Pandas code"):
#                         st.code(res["code_executed"], language="python")

#                 if isinstance(res["result"], (pd.DataFrame, pd.Series)):
#                     st.dataframe(res["result"], width="stretch")
#                 elif res["result"] is not None:
#                     st.metric(label="Result", value=str(res["result"]))

#                 if res["chart"] is not None:
#                     st.plotly_chart(res["chart"],  width="stretch")

#             elif res["status"] == "clarification":
#                 st.warning(f"Clarification of the requirement: {res['message']}")

#             elif res["status"] == "error":
#                 st.error(f"{res['message']}")

#             if metrics:
#                 st.caption(
#                     f"⏱️ **Latency:** {metrics.get('latency_sec', 0)}s | "
#                     f"🔢 **Tokens:** {metrics.get('total_tokens', 0)} "
#                     f"(Prompt: {metrics.get('prompt_tokens', 0)}, Completion: {metrics.get('completion_tokens', 0)})"
#                 )

#     user_question = st.chat_input("Ask a question about your data (e.g., What are the total sales by region?)...")

#     if user_question:
#         with st.chat_message("user"):
#             st.write(user_question)

#         with st.chat_message("assistant"):
#             with st.spinner("Data is being analyzed and a decision is being made..."):
#                 response = process_user_query(user_question, st.session_state.df,st.session_state.chat_history )
#                 st.session_state.chat_history.append({
#                     "question": user_question,
#                     "response": response,
#                 })

#                 st.rerun()