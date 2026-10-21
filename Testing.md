

| Test ID | Input / Situation | Expected Behavior | Actual Behavior | Pass / Fail |


| T1 | 
-- Input: Valid sales_data.csv uploaded
--Expected Behavior:Dataset loads properly showing row count (35), column count (9), and a 5-row preview table. 
--Actual Behavior: Correctly displayed 35 rows, 9 columns, and preview table in UI expander. 
--PASS / Fail : Pass


| T2 | 
-- Input: Query: "What are the total sales per region?" 
--Expected Behavior: System identifies clear intent, executes df.groupby("Region")["Total_Sales"].sum(), and renders result table + Plotly bar chart.
--Actual Behavior: Displayed table with East ($9,100), North ($10,400), South ($7,795), West ($6,520) and a bar chart.
--PASS / Fail : Pass


| T3 | 
-- Input:Ambiguous Query: "What is the best product?"
--Expected Behavior: System flags ambiguity and asks a follow-up question regarding how "best" is defined (revenue vs. quantity).
--Actual Behavior:  System returned warning: "Ambiguous query. Do you mean best by total sales revenue or quantity sold?"
--PASS/Fail : Pass


| T4 | 
-- Input:Out-of-Scope Query: "Show customer feedback ratings."
--Expected Behavior: System detects that "feedback ratings" column does not exist in schema and displays an informative message. 
--Actual Behavior: System returned error:"Column 'customer feedback' is not present in the dataset schema."
--PASS/Fail : Pass

