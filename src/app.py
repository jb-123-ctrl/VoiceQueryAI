import streamlit as st
import speech_recognition as sr
import sqlite3

st.title("VoiceQuery AI")
st.write("Speak your query and get SQL output!")

# Function to listen to speech
def listen_query():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening...")
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            return text
        except:
            return "Could not recognize speech."

# Function to execute SQL query
def execute_query(query):
    try:
        conn = sqlite3.connect('demo.db')  # your database file
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        conn.close()
        return result
    except Exception as e:
        return f"Error: {e}"

# Streamlit button to start listening
if st.button("Start Listening"):
    query_text = listen_query()
    st.success(f"You said: {query_text}")

    # For demo, assuming user speaks SQL directly
    result = execute_query(query_text)
    st.write("Query Result:")
    st.write(result)
