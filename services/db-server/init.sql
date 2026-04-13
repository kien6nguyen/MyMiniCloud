-- Initial schema for MyMiniCloud
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Seed data
INSERT INTO users (username, password_hash, email) 
VALUES ('admin', 'scrypt:32768:8:1$94Nf8p1Q7W6E4k9P$941e97...', 'admin@myminicloud.local');

-- Student Management Table
CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    student_id VARCHAR(10),
    fullname VARCHAR(100),
    dob DATE,
    major VARCHAR(50)
);

INSERT INTO students (student_id, fullname, dob, major) VALUES 
('S001', 'Nguyen Van A', '2002-05-15', 'Computer Science'),
('S002', 'Le Thi B', '2001-08-22', 'Cyber Security'),
('S003', 'Tran Van C', '2002-12-10', 'Data Science');

-- Notes Table
CREATE TABLE notes (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO notes (title) VALUES ('Hello');
