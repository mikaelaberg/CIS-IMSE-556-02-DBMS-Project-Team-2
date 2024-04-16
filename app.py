import psycopg2

from flask import Flask, render_template, jsonify,request, redirect, url_for

app = Flask(__name__)

# Database connection parameters
db_config = {
    'dbname': 'postgres',
    'user': 'postgres',
    'password': 'Harshitha@16',
    'host': 'localhost'
}
<<<<<<< HEAD



=======
>>>>>>> 1ce84e71c6e3e316e64fd847a58c114cb0035169
def get_pending_applications():
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
<<<<<<< HEAD
        cursor.execute('''
            SELECT "ADMISSION_ID" 
            FROM starrs."ADMISSION" 
            WHERE "ADMISSION_ID" NOT IN (
                SELECT "ADMISSION_ID" 
                FROM starrs."ADMISSION_REVIEW"
            )
        ''')
=======
        cursor.execute('SELECT "USER_ID" FROM starrs."APPLICANT"')
>>>>>>> 1ce84e71c6e3e316e64fd847a58c114cb0035169
        pending_applications = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return pending_applications
    except psycopg2.Error as e:
        print("Error retrieving pending applications:", e)
        return []
<<<<<<< HEAD


@app.route('/submit_review', methods=['POST'])
def submit_review():
    data = request.get_json()
    print("Received data:", data)
    # Extract data from the request

    reviewer_id = data['reviewer_id']
    admission_id = data['admission_id']
    ranking = data['ranking']
    comments = data['comments']
    decision = data['decision']
    committee_id = data['committee_id']
    advisor: object = data['advisor']
    print("Extracted data:", reviewer_id, admission_id, ranking, comments, decision, committee_id,advisor)

    # Insert the data into the database
    try:
        # Insert the data into the database
        conn = psycopg2.connect(**db_config)
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO starrs.\"ADMISSION_REVIEW\" (\"REVIEWER_ID\", \"ADMISSION_ID\", \"ADMISSION_COMMENT\", \"ADMISSION_RANKING\", \"ADMISSION_DECISION\", \"COMMITTEE_ID\", \"ADVISOR\") VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (reviewer_id, admission_id, comments, ranking, decision, committee_id, advisor))
        cur.execute(
            "UPDATE starrs.\"ADMISSION\" SET \"ADMISSION_COMMENT\" = %s, \"ADMISSION_RANKING\" = %s, \"COMMITTEE_DECISION\" = %s, \"RECOMMENDED_ADVISOR\" = %s WHERE \"ADMISSION_ID\" = %s",
            (comments, ranking, decision, advisor, admission_id))
        conn.commit()
        cur.close()
        conn.close()
        print("Review submitted successfully")
        return jsonify({'success': True, 'message': 'Review submitted successfully'})
    except Exception as e:
        print("Error submitting review:", e)
        return jsonify({'success': False, 'message': f'Error submitting review: {str(e)}'})

=======
>>>>>>> 1ce84e71c6e3e316e64fd847a58c114cb0035169
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