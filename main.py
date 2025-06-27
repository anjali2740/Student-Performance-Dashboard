import mysql.connector
import pandas as pd
from tabulate import tabulate   # nice console tables (pip install tabulate)

# ──────────────────────────────────────────────────────────────────────────
# DB HELPERS
# ──────────────────────────────────────────────────────────────────────────
def connect_db():
    """Return a live MySQL connection (edit credentials as needed)."""
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",       # ← change me
        database="student_db"
    )

# ──────────────────────────────────────────────────────────────────────────
# CRUD OPERATIONS
# ──────────────────────────────────────────────────────────────────────────
def add_student(student_id: int, name: str, class_name: str):
    conn = connect_db()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO students (student_id, name, class) VALUES (%s, %s, %s)",
            (student_id, name, class_name)
        )
        conn.commit()
        print(f"✅ Added student “{name}” ({class_name}).")
    except mysql.connector.IntegrityError:
        print("⚠️  Student ID already exists.")
    finally:
        cur.close()
        conn.close()

def add_marks(student_id: int, subject: str, marks: int):
    conn = connect_db(); cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO marks (student_id, subject, marks) VALUES (%s, %s, %s)",
            (student_id, subject, marks)
        )
        conn.commit()
        print("✅ Marks added.")
    except mysql.connector.IntegrityError as e:
        print("❌ Error:", e)
    finally:
        cur.close(); conn.close()

def add_attendance(student_id: int, subject: str, percent: float):
    conn = connect_db(); cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO attendance (student_id, subject, attendance_percent) "
            "VALUES (%s, %s, %s)",
            (student_id, subject, percent)
        )
        conn.commit()
        print("✅ Attendance added.")
    except mysql.connector.IntegrityError as e:
        print("❌ Error:", e)
    finally:
        cur.close(); conn.close()

# ──────────────────────────────────────────────────────────────────────────
# ANALYTICS / REPORTS
# ──────────────────────────────────────────────────────────────────────────
MAX_MARK = 100   # change if your exam is not out of 100

def topper_report():
    conn = connect_db()
    q = """
    SELECT s.student_id, s.name, SUM(m.marks) AS total
    FROM students s
    JOIN marks m ON s.student_id = m.student_id
    GROUP BY s.student_id, s.name
    ORDER BY total DESC
    LIMIT 1;
    """
    df = pd.read_sql(q, conn); conn.close()
    if df.empty:
        print("⚠️  No marks recorded yet.")
    else:
        print("\n🏆 CLASS TOPPER")
        print(tabulate(df, headers="keys", tablefmt="psql", showindex=False))

def most_regular_report():
    conn = connect_db()
    q = """
    SELECT s.student_id, s.name,
           ROUND(AVG(a.attendance_percent),2) AS avg_attendance
    FROM students s
    JOIN attendance a ON s.student_id = a.student_id
    GROUP BY s.student_id, s.name
    ORDER BY avg_attendance DESC
    LIMIT 1;
    """
    df = pd.read_sql(q, conn); conn.close()
    if df.empty:
        print("⚠️  No attendance data yet.")
    else:
        print("\n📈 MOST REGULAR STUDENT")
        print(tabulate(df, headers="keys", tablefmt="psql", showindex=False))

def percentage_report():
    conn = connect_db()
    q = """
    SELECT s.student_id, s.name, COUNT(DISTINCT m.subject) AS subjects,
           SUM(m.marks) AS total_marks
    FROM students s
    LEFT JOIN marks m ON s.student_id = m.student_id
    GROUP BY s.student_id, s.name;
    """
    df = pd.read_sql(q, conn); conn.close()
    if df.empty:
        print("⚠️  No marks data yet.")
        return

    df["percentage"] = (df["total_marks"] / (df["subjects"]*MAX_MARK) * 100).round(2)
    print("\n🎯 MARKS PERCENTAGE (all students)")
    print(tabulate(df[["student_id", "name", "percentage"]],
                   headers=["ID", "Name", "% Marks"],
                   tablefmt="psql", showindex=False))

# ──────────────────────────────────────────────────────────────────────────
# CLI MENU
# ──────────────────────────────────────────────────────────────────────────
def main_menu():
    MENU = """
────────────────────────────────────────────────────
 STUDENT PERFORMANCE DASHBOARD  –  CLI
────────────────────────────────────────────────────
 1 › Add Student
 2 › Add Marks
 3 › Add Attendance
 4 › Show Class Topper
 5 › Show Most‑Regular Student
 6 › Show Marks Percentage (all)
 7 › Exit
────────────────────────────────────────────────────
"""
    while True:
        print(MENU)
        choice = input("Select option (1‑7): ").strip()
        if choice == "1":
            try:
                sid = int(input("Student ID: "))
                name = input("Name       : ")
                cls  = input("Class      : ")
                add_student(sid, name, cls)
            except ValueError:
                print("⚠️  Invalid input.")
        elif choice == "2":
            try:
                sid = int(input("Student ID: "))
                subject = input("Subject   : ")
                marks = int(input("Marks     : "))
                add_marks(sid, subject, marks)
            except ValueError:
                print("⚠️  Invalid input.")
        elif choice == "3":
            try:
                sid = int(input("Student ID     : "))
                subject = input("Subject        : ")
                percent = float(input("Attendance (%) : "))
                add_attendance(sid, subject, percent)
            except ValueError:
                print("⚠️  Invalid input.")
        elif choice == "4":
            topper_report()
        elif choice == "5":
            most_regular_report()
        elif choice == "6":
            percentage_report()
        elif choice == "7":
            print("Bye! 👋")
            break
        else:
            print("⚠️  Choose a valid option.")

if __name__ == "__main__":
    main_menu()
