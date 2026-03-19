import os
import datetime
from flask import Flask, jsonify, request
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

@app.route('/api/status', methods=['GET'])
def get_status():
    conn = get_db_connection()
    if not conn:
        return jsonify({"status": "unhealthy", "error": "DB connection failed"}), 500
    
    try:
        cur = conn.cursor()
        cur.execute("SELECT nodename, status, cpu_usage, ram_usage, last_check FROM nodes")
        nodes = cur.fetchall()
        cur.close()
        conn.close()

        result = []
        for node in nodes:
            result.append({
                "nodename": node[0],
                "status": node[1],
                "cpu": float(node[2]) if node[2] else 0.0,
                "ram": float(node[3]) if node[3] else 0.0,
                "timestamp": node[4].isoformat() if node[4] else None
            })
        
        return jsonify({
            "status": "healthy",
            "system": "MyMiniCloud v1.0",
            "nodes": result
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "UP", "timestamp": datetime.datetime.now().isoformat()})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
