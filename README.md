# 🎓 Student Performance Dashboard

A command-line **Student Performance Dashboard** built using **Python** and **MySQL**, designed to manage student records, marks, attendance, and generate insightful reports such as class topper, most regular student, and performance percentages.

---

## 🚀 Features

- ➕ Add Student Records  
- 📝 Add Subject-wise Marks  
- 📊 Add Attendance Percentages  
- 🥇 Show Class Topper (Based on Total Marks)  
- 🕒 Show Most Regular Student (Based on Average Attendance)  
- 📈 Show Marks Percentage for Every Student  

---

## 🛠️ Tech Stack

- **Language:** Python  
- **Database:** MySQL  
- **Software:** PyCharm, MySQL Server  

---

## 🧱 Database Setup

1. **Credentials**
   - Username: `root`
   - Password: `your password`
   - Database Name: `student_db`

2. **SQL Queries to Create Tables**
   ```sql
   CREATE DATABASE student_db;
   USE student_db;

   CREATE TABLE students (
       student_id INT PRIMARY KEY,
       name VARCHAR(100),
       class VARCHAR(50)
   );

   CREATE TABLE marks (
       student_id INT,
       subject VARCHAR(100),
       marks INT,
       FOREIGN KEY (student_id) REFERENCES students(student_id)
   );

   CREATE TABLE attendance (
       student_id INT,
       subject VARCHAR(100),
       attendance_percent DECIMAL(5,2),
       FOREIGN KEY (student_id) REFERENCES students(student_id)
   );

🧮 Report Queries
🥇 Class Topper Report:

![image](https://github.com/user-attachments/assets/89a8a0f9-6eea-4b4a-86f0-e1ab6bd6a52c)

🕒 Most Regular Student Report:

![image](https://github.com/user-attachments/assets/be3a2c86-c140-40c8-a746-db8b061a682d)

📈 Marks Percentage Report:

![image](https://github.com/user-attachments/assets/857adba0-9792-41f2-9d7d-5150cbd7d831)

⚙️ Running the Program:
1. Ensure MySQL server is running.
2. Install MySQL connector for Python:
   ```bash
   pip install mysql-connector-python
3. Update main.py connection config if needed:
    ```bash
   conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your password here",
    database="student_db")
4. Run the script:
   ```bash
   python main.py

🙌 Contributions
Contributions are welcome!
Fork the repo, make improvements, and submit a pull request.

📜 License
This project is licensed under the MIT License – see the LICENSE file for details.

   


