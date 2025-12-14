import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configure MySQL from environment variables
app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST', 'localhost')
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD', 'root')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB', 'flask_db')

# Initialize MySQL
mysql = MySQL(app)

def init_db():
    """Initialize database and create tables if they don't exist"""
    try:
        with app.app_context():
            cur = mysql.connection.cursor()
            cur.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INT AUTO_INCREMENT PRIMARY KEY,
                message TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            ''')
            mysql.connection.commit()
            cur.close()
            print("✅ Database initialized successfully")
    except Exception as e:
        print(f"❌ Database initialization error: {e}")

@app.route('/')
def index():
    """Main portfolio page"""
    try:
        cur = mysql.connection.cursor()
        cur.execute('SELECT message FROM messages ORDER BY created_at DESC LIMIT 50')
        messages = cur.fetchall()
        cur.close()
        return render_template('index.html', messages=messages)
    except Exception as e:
        print(f"Error fetching messages: {e}")
        return render_template('index.html', messages=[])

@app.route('/submit', methods=['POST'])
def submit():
    """Handle message submissions"""
    try:
        if request.is_json:
            new_message = request.json.get('new_message')
        else:
            new_message = request.form.get('new_message')
        
        if not new_message:
            return jsonify({'error': 'Message is required'}), 400
        
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO messages (message) VALUES (%s)', [new_message])
        mysql.connection.commit()
        cur.close()
        
        return jsonify({'message': new_message, 'status': 'success'}), 200
    except Exception as e:
        print(f"Error submitting message: {e}")
        return jsonify({'error': 'Failed to submit message'}), 500

@app.route('/health')
def health():
    """Health check endpoint for monitoring"""
    try:
        cur = mysql.connection.cursor()
        cur.execute('SELECT 1')
        cur.close()
        return jsonify({'status': 'healthy', 'database': 'connected'}), 200
    except:
        return jsonify({'status': 'unhealthy', 'database': 'disconnected'}), 500

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)