-- Initial schema for MyMiniCloud
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE nodes (
    id SERIAL PRIMARY KEY,
    nodename VARCHAR(50) UNIQUE NOT NULL,
    status VARCHAR(20) DEFAULT 'unhealthy',
    cpu_usage NUMERIC(5,2),
    ram_usage NUMERIC(5,2),
    last_check TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Seed data
INSERT INTO users (username, password_hash, email) 
VALUES ('admin', 'scrypt:32768:8:1$94Nf8p1Q7W6E4k9P$941e97...', 'admin@myminicloud.local');

INSERT INTO nodes (nodename, status) VALUES ('node-1', 'healthy'), ('node-2', 'healthy');
