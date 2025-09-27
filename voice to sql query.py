import sqlite3
import speech_recognition as sr
import pyttsx3
from fuzzywuzzy import fuzz

# -------------------------------
# Create demo database
# -------------------------------
def create_demo_db():
    conn = sqlite3.connect("demo.db")
    cur = conn.cursor()

    # Employees table
    cur.execute("DROP TABLE IF EXISTS employees")
    cur.execute("""
        CREATE TABLE employees (
            id INTEGER PRIMARY KEY,
            name TEXT,
            department TEXT,
            salary INTEGER,
            join_date TEXT
        )
    """)
    employees = [
        (1, "Ravi K", "IT", 75000, "2021-02-15"),
        (2, "Meena S", "HR", 55000, "2019-03-28"),
        (3, "Arjun N", "IT", 105000, "2020-11-25"),
        (4, "Priya M", "R&D", 95000, "2022-03-11"),
        (5, "Lakshmi N", "Finance", 60000, "2023-08-30")
    ]
    cur.executemany("INSERT INTO employees VALUES (?, ?, ?, ?, ?)", employees)

    # Departments table
    cur.execute("DROP TABLE IF EXISTS departments")
    cur.execute("""
        CREATE TABLE departments (
            id INTEGER PRIMARY KEY,
            name TEXT
        )
    """)
    departments = [(1, "IT"), (2, "HR"), (3, "R&D"), (4, "Finance")]
    cur.executemany("INSERT INTO departments VALUES (?, ?)", departments)

    conn.commit()
    conn.close()
    print("✅ Demo database created with sample data.")

# -------------------------------
# Run SQL query
# -------------------------------
def run_query(sql):
    conn = sqlite3.connect("demo.db")
    cur = conn.cursor()
    try:
        cur.execute(sql)
        rows = cur.fetchall()
        conn.close()
        return rows
    except Exception as e:
        conn.close()
        return f"❌ Error: {e}"

# -------------------------------
# Helper: fuzzy check
# -------------------------------
def fuzzy_contains(query_text, keyword, threshold=80):
    """Check if keyword is fuzzily present in query_text"""
    return fuzz.partial_ratio(query_text, keyword) >= threshold

# -------------------------------
# NLP → SQL mapping with fuzzy match
# -------------------------------
def nlp_to_sql(query_text: str) -> str:
    query_text = query_text.lower()

    if fuzzy_contains(query_text, "all employees"):
        return "SELECT * FROM employees;"
    elif fuzzy_contains(query_text, "employees in it"):
        return "SELECT * FROM employees WHERE department='IT';"
    elif fuzzy_contains(query_text, "employees in hr"):
        return "SELECT * FROM employees WHERE department='HR';"
    elif fuzzy_contains(query_text, "salary greater"):
        number = [int(s) for s in query_text.split() if s.isdigit()]
        if number:
            return f"SELECT * FROM employees WHERE salary > {number[0]};"
    elif fuzzy_contains(query_text, "count employees"):
        return "SELECT COUNT(*) FROM employees;"
    elif fuzzy_contains(query_text, "departments"):
        return "SELECT * FROM departments;"
    elif fuzzy_contains(query_text, "average salary"):
        return "SELECT AVG(salary) FROM employees;"
    elif fuzzy_contains(query_text, "highest salary"):
        return "SELECT name, salary FROM employees ORDER BY salary DESC LIMIT 1;"
    elif fuzzy_contains(query_text, "joined after"):
        number = [int(s) for s in query_text.split() if s.isdigit()]
        if number:
            return f"SELECT * FROM employees WHERE join_date > '{number[0]}-01-01';"
    elif fuzzy_contains(query_text, "employees with departments") or fuzzy_contains(query_text, "join"):
        return """
            SELECT e.name, e.department, d.id
            FROM employees e
            JOIN departments d ON e.department = d.name;
        """
    elif fuzzy_contains(query_text, "projects"):
        return "SELECT 'No project table yet';"
    else:
        return None

# -------------------------------
# Voice input
# -------------------------------
def get_voice_input():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("\n🎤 Microphone is active. Speak your query (say 'exit' to quit)...")
        r.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = r.listen(source, timeout=15, phrase_time_limit=15)
            text_query = r.recognize_google(audio)
            print("🗣 Recognized text (raw):", text_query)
            return text_query
        except sr.WaitTimeoutError:
            print("⌛ Timeout: No speech detected.")
            return None
        except sr.UnknownValueError:
            print("❌ Could not understand audio.")
            return None
        except Exception as e:
            print("❌ Speech error:", e)
            return None

# -------------------------------
# TTS setup
# -------------------------------
engine = pyttsx3.init()
engine.setProperty("rate", 170)
engine.setProperty("volume", 1.0)

def speak(text):
    print("🔊 Speaking:", text)
    engine.say(text)
    engine.runAndWait()

def format_and_speak(sql, result):
    if not result or isinstance(result, str):
        speak("No results found.")
        return
    if "count" in sql.lower():
        speak(f"There are {result[0][0]} employees in the database.")
    elif "avg" in sql.lower():
        speak(f"The average salary is {int(result[0][0])} rupees.")
    elif "limit 1" in sql.lower():
        speak(f"{result[0][0]} has the highest salary of {result[0][1]} rupees.")
    elif "employees where department='IT'" in sql:
        speak(f"There are {len(result)} employees in the IT department.")
    else:
        speak("I have fetched the results. Please check your screen for details.")

# -------------------------------
# Main loop
# -------------------------------
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


