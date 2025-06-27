CREATE DATABASE student_db;

use student_db;

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



