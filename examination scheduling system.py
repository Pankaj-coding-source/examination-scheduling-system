import pymysql

# Connect to MySQL
def connect():
    return pymysql.connect(host="localhost", user="root", password="your password", port=3306)

# Create Database
def createDB():
    mydb = connect()
    cursor = mydb.cursor()
    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS examsheduling")
        mydb.commit()
    except Exception as e:
        print(f"Database Error: {e}")
    finally:
        cursor.close()
        mydb.close()

# Create Tables
def createTables():
    mydb = connect()
    cursor = mydb.cursor()
    try:
        cursor.execute("USE examsheduling")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS course (
                courseid INT PRIMARY KEY,
                coursename VARCHAR(100)
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS exams (
                Examid INT PRIMARY KEY,
                courseid INT,
                examdate DATE,
                examtime TIME,
                FOREIGN KEY (courseid) REFERENCES course(courseid)
            )
        """)
        mydb.commit()
        print("Tables created successfully.")
    except Exception as e:
        print(f"Table Error: {e}")
    finally:
        cursor.close()
        mydb.close()

# Insert into Course
def insertCourse():
    mydb = connect()
    cursor = mydb.cursor()
    try:
        cursor.execute("USE examsheduling")
        course_id = int(input("Enter Course ID: "))
        course_name = input("Enter Course Name: ")
        cursor.execute("INSERT INTO course VALUES (%s, %s)", (course_id, course_name))
        mydb.commit()
        print("course added successfully")
    except Exception as e:
        print(f"Insertion Error (Course): {e}")
    finally:
        cursor.close()
        mydb.close()

# Insert into Exams
def insertExam():
    mydb = connect()
    cursor = mydb.cursor()
    try:
        cursor.execute("USE examsheduling")
        examId = int(input("Enter Exam ID: "))
        courseId = int(input("Enter Course ID: "))
        examDate = input("Enter Exam Date (YYYY-MM-DD): ")
        examTime = input("Enter Exam Time (HH:MM:SS): ")
        cursor.execute("INSERT INTO exams VALUES (%s, %s, %s, %s)", (examId, courseId, examDate, examTime))
        mydb.commit()
        print("exam added successfully")
    except Exception as e:
        print("course is unavailable")
       
    finally:
        cursor.close()
        mydb.close()

# Update Data
def updateExam():
    mydb = connect()
    cursor = mydb.cursor()
    try:
        cursor.execute("USE examsheduling")
        print("What would you like to update?")
        print("1. Course ID\n2. Exam ID\n3. Exam Date\n4. Exam Time")
        choice = int(input("Enter your choice (1-4): "))
        exam_id = input("Enter the Exam ID of the record to update: ")

        if choice == 1:
            new_course_id = input("Enter new Course ID: ")
            cursor.execute("UPDATE exams SET courseid = %s WHERE Examid = %s", (new_course_id, exam_id))
        elif choice == 2:
            new_exam_id = input("Enter new Exam ID: ")
            cursor.execute("UPDATE exams SET Examid = %s WHERE Examid = %s", (new_exam_id, exam_id))
        elif choice == 3:
            new_exam_date = input("Enter new Exam Date (YYYY-MM-DD): ")
            cursor.execute("UPDATE exams SET examdate = %s WHERE Examid = %s", (new_exam_date, exam_id))
        elif choice == 4:
            new_exam_time = input("Enter new Exam Time (HH:MM:SS): ")
            cursor.execute("UPDATE exams SET examtime = %s WHERE Examid = %s", (new_exam_time, exam_id))
        else:
            print("Invalid choice.")
            return

        mydb.commit()
        print(f"Rows updated: {cursor.rowcount}")
    except Exception as e:
        print(f"Update Error: {e}")
    finally:
        cursor.close()
        mydb.close()

# Display Data
def showExams():
    mydb = connect()
    cursor = mydb.cursor()
    try:
        cursor.execute("USE examsheduling")
        cursor.execute("SELECT Examid, courseid, examdate, TIME_FORMAT(examtime, '%H:%i:%s') FROM exams")
        rows = cursor.fetchall()
        for row in rows:
            print(row)
    except Exception as e:
        print(f"Display Error: {e}")
    finally:
        cursor.close()
        mydb.close()

# Delete/Search Functionality
def delete_data():
    mydb = connect()
    cursor = mydb.cursor()
    try:
        cursor.execute("USE examsheduling")
        t = input("Enter the table name (course/exams): ").lower()
        if t not in ["exams", "course"]:
            print("Invalid table name.")
            return

        print("Delete Options:\n1. Delete Row\n2. Delete Column\n3. Clear Table\n4. Drop Table")
        choice = int(input("Enter your choice: "))

        if choice == 1:
            if t == "exams":
                id_col = "Examid"
            else:
                id_col = "courseid"
            row_id = input(f"Enter the {id_col} to delete: ")
            cursor.execute(f"DELETE FROM {t} WHERE {id_col} = %s", (row_id,))
        elif choice == 2:
            column_name = input("Enter the column name to drop: ")
            cursor.execute(f"ALTER TABLE {t} DROP COLUMN {column_name}")
        elif choice == 3:
            cursor.execute(f"TRUNCATE TABLE {t}")
        elif choice == 4:
            cursor.execute(f"DROP TABLE {t}")
        else:
            print("Invalid choice.")
            return

        mydb.commit()
        print("Operation completed successfully.")
    except Exception as e:
        print(f"Delete Error: {e}")
    finally:
        cursor.close()
        mydb.close()

# Clear Exam Table
def clearExams():
    mydb = connect()
    cursor = mydb.cursor()
    try:
        cursor.execute("USE examsheduling")
        cursor.execute("TRUNCATE TABLE exams")
        print("Exams table cleared.")
        mydb.commit()
    except Exception as e:
        print(f"Clear Error: {e}")
    finally:
        cursor.close()
        mydb.close()

# Entry point
if __name__ == "__main__":
    createDB()
    createTables()

    while True:
        print("\nMenu:")
        print("1. Delete")
        print("2. Insert Exam")
        print("3. Update Exam")
        print("4. Display Exams")
        print("5. Clear Exams Table")
        print("6. Insert Course")
        print("7. Exit")
        choice = int(input("Enter your choice: "))

        if choice == 1:
            delete_data()
        elif choice == 2:
            n = int(input("Enter number of exams to insert: "))
            for _ in range(n):
                insertExam()
        elif choice == 3:
            updateExam()
        elif choice == 4:
            showExams()
        elif choice == 5:
            clearExams()
        elif choice == 6:
            insertCourse()
        elif choice == 7:
            print("Exiting... Thank you!")
            break
        else:
            print("Invalid choice. Please try again.")
