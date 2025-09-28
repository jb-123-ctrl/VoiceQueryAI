if __name__ == "__main__":
    create_demo_db()

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




