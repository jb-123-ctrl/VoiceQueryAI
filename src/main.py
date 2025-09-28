# src/main.py
from voice_to_sql_query import create_demo_db, get_voice_input, nlp_to_sql, run_query, format_and_speak, speak

if __name__ == "__main__":
    # Create demo database with sample data
    create_demo_db()

    # Main loop for voice input
    while True:
        query = get_voice_input()
        if not query:
            continue
        if query.lower() == "exit":
            speak("Goodbye! Closing program now.")
            print("👋 Exiting program.")
            break

        sql = nlp_to_sql(query)
        if sql:
            print("✅ Generated SQL:", sql)
            result = run_query(sql)
            print("📊 Result:", result)
            format_and_speak(sql, result)
        else:
            msg = "❌ Could not map your speech to SQL. Try again with keywords."
            print(msg)
            speak("I could not understand your query. Please try again.")
