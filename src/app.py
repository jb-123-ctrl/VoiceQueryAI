import streamlit as st
import sqlite3
from voice_to_sql_query import nlp_to_sql, run_query, format_and_speak

st.title("VoiceQuery AI (Text Input Version)")
st.write("Type your query in plain English and get SQL output!")

# Text input replaces microphone
query_text = st.text_input("Enter your SQL query in plain English:")

if query_text:
    sql = nlp_to_sql(query_text)  # convert natural language to SQL
    if sql:
        st.write("✅ Generated SQL:", sql)
        result = run_query(sql)  # execute SQL
        st.write("📊 Query Result:")
        st.write(result)
        # Display results
        format_and_speak(sql, result, use_streamlit=True)
    else:
        st.write("❌ Could not map your query to SQL. Try again with keywords.")
