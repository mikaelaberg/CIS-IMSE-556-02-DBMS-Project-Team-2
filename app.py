import psycopg2
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# Database connection parameters
db_config = {
    'dbname': 'postgres',
    'user': 'postgres',
    'password': 'Cosmopeepaws123',
    'host': 'localhost'
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/university_applications')
def university_applications():
    return render_template('university_applications.html')

@app.route('/course_registration')
def course_registration():
    return render_template('course_registration.html')

@app.route('/graduation_application')
def graduation_application():
    return render_template('graduation_application.html')

@app.route('/alumni_page')
def alumni_page():
    return render_template('alumni_page.html')

@app.route('/faculty_page')
def faculty_page():
    return render_template('faculty_page.html')
@app.route('/test_db')
def test_db():
    try:
        conn = psycopg2.connect(**db_config)
        cur = conn.cursor()
        cur.execute('SELECT version();')
        db_version = cur.fetchone()
        cur.close()
        conn.close()
        return jsonify({"success": True, "PostgreSQL Version": db_version})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)


@app.route('/check-student-status', methods=['POST'])
def check_student_status():
    data = request.json
    student_id = data.get('STUDENT_ID')

    # Connect to your PostgreSQL database
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="Cosmopeepaws123",
        host="localhost"
    )
    cur = conn.cursor()

    # Query the database for the student status
    cur.execute("""SELECT "STATUS" FROM starrs."GRAD_APPLICATION" WHERE "STUDENT_ID" = %s""", (student_id,))
    status = cur.fetchone()

    # Don't forget to close the connection
    cur.close()
    conn.close()

    if status:
        return jsonify({"status": status[0]})
    else:
        return jsonify({"error": "Student not found"}), 404