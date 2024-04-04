import psycopg2
from flask import Flask, render_template, jsonify

app = Flask(__name__)

# Database connection parameters
db_config = {
    'dbname': 'postgres',
    'user': 'postgres',
    'password': 'Harshitha@16',
    'host': 'localhost'
}
def get_pending_applications():
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute('SELECT "USER_ID" FROM starrs."APPLICANT"')
        pending_applications = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return pending_applications
    except psycopg2.Error as e:
        print("Error retrieving pending applications:", e)
        return []
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
@app.route('/pending_applications')
def pending_applications():
    pendingApplications = get_pending_applications()
    return jsonify(pendingApplications=pendingApplications)
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

