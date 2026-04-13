import os
import datetime
import json
from flask import Flask, jsonify, request, render_template_string
import psycopg2

app = Flask(__name__)

DB_HOST = os.environ.get('DB_HOST', 'db-server')
DB_USER = os.environ.get('DB_USER', 'postgres')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'mycloudroot')
DB_NAME = os.environ.get('DB_NAME', 'cloud_db')

def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            dbname=DB_NAME
        )
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

        return None

@app.route('/api/status', methods=['GET'])
def get_status():
    return jsonify({
        "status": "healthy",
        "system": "MyMiniCloud v1.0",
        "timestamp": datetime.datetime.now().isoformat()
    })

@app.get("/api/student")
def student():
    try:
        with open("students.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        
        # If the user requests from a browser, show the HTML table
        if "text/html" in request.headers.get("Accept", ""):
            html_content = """
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <title>Student List</title>
                <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;600&display=swap" rel="stylesheet">
                <style>
                    body { font-family: 'Outfit', sans-serif; background: #0f172a; color: white; padding: 40px; }
                    .container { max-width: 800px; margin: 0 auto; background: rgba(30, 41, 59, 0.7); padding: 30px; border-radius: 20px; border: 1px solid rgba(255,255,255,0.1); backdrop-filter: blur(10px); }
                    h1 { text-align: center; background: linear-gradient(to right, #6366f1, #22d3ee); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
                    table { width: 100%; border-collapse: collapse; margin-top: 20px; }
                    th { text-align: left; padding: 12px; border-bottom: 2px solid rgba(255,255,255,0.1); color: #94a3b8; font-size: 0.9rem; text-transform: uppercase; }
                    td { padding: 12px; border-bottom: 1px solid rgba(255,255,255,0.05); }
                    tr:hover { background: rgba(255,255,255,0.02); }
                    .gpa { font-weight: 600; color: #10b981; }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>🎓 Student Directory</h1>
                    <table>
                        <thead>
                            <tr><th>ID</th><th>Name</th><th>Major</th><th>GPA</th></tr>
                        </thead>
                        <tbody>
                            {% for s in students %}
                            <tr>
                                <td style="color:#94a3b8">#{{ s.id }}</td>
                                <td>{{ s.name }}</td>
                                <td>{{ s.major }}</td>
                                <td class="gpa">{{ s.gpa }}</td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                    <p style="text-align:center; margin-top:20px;"><a href="/" style="color:#22d3ee; text-decoration:none;">← Dashboard</a></p>
                </div>
            </body>
            </html>
            """
            return render_template_string(html_content, students=data)
            
        return jsonify(data)
    except FileNotFoundError:
        return jsonify({"error": "students.json not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.get("/api/students-db")
def student_db():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    
    try:
        cur = conn.cursor()
        cur.execute("SELECT id, student_id, fullname, dob, major FROM students ORDER BY id ASC")
        rows = cur.fetchall()
        
        students = []
        for row in rows:
            students.append({
                "id": row[0],
                "student_id": row[1],
                "fullname": row[2],
                "dob": row[3].strftime('%Y-%m-%d') if row[3] else None,
                "major": row[4]
            })
        cur.close()
        conn.close()

        # If accessed via browser, show nice table
        if "text/html" in request.headers.get("Accept", ""):
            html_content = """
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <title>Student Database</title>
                <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;600&display=swap" rel="stylesheet">
                <style>
                    body { font-family: 'Outfit', sans-serif; background: #0f172a; color: white; padding: 40px; }
                    .container { max-width: 900px; margin: 0 auto; background: rgba(30, 41, 59, 0.7); padding: 30px; border-radius: 20px; border: 1px solid rgba(255,255,255,0.1); backdrop-filter: blur(10px); }
                    h1 { text-align: center; background: linear-gradient(to right, #6366f1, #22d3ee); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
                    table { width: 100%; border-collapse: collapse; margin-top: 20px; }
                    th { text-align: left; padding: 12px; border-bottom: 2px solid rgba(255,255,255,0.1); color: #94a3b8; font-size: 0.85rem; text-transform: uppercase; }
                    td { padding: 12px; border-bottom: 1px solid rgba(255,255,255,0.05); }
                    .badge { padding: 4px 8px; border-radius: 5px; background: rgba(99,102,241,0.1); color: #6366f1; font-weight: 600; font-size: 0.8rem; }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>🎓 Student Database Records</h1>
                    <table>
                        <thead>
                            <tr><th>ID</th><th>Student ID</th><th>Full Name</th><th>DOB</th><th>Major</th></tr>
                        </thead>
                        <tbody>
                            {% for s in students %}
                            <tr>
                                <td style="color:#94a3b8">#{{ s.id }}</td>
                                <td><span class="badge">{{ s.student_id }}</span></td>
                                <td style="font-weight:600">{{ s.fullname }}</td>
                                <td>{{ s.dob }}</td>
                                <td>{{ s.major }}</td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                    <p style="text-align:center; margin-top:20px;"><a href="/" style="color:#22d3ee; text-decoration:none;">← Dashboard</a></p>
                </div>
            </body>
            </html>
            """
            return render_template_string(html_content, students=students)

        return jsonify(students)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.get("/hello")
@app.get("/api/hello")
def hello():
    return jsonify({"message": "Hello from App Server!"})

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "UP", "timestamp": datetime.datetime.now().isoformat()})

@app.route('/metrics', methods=['GET'])
def metrics():
    return "app_up 1", 200, {'Content-Type': 'text/plain; version=0.0.4; charset=utf-8'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)
