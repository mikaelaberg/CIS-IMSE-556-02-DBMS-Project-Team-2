import psycopg2

import applicant_info
import graduate_secretary
import user
from dbconfig import db_config
from flask import Flask, render_template, jsonify, redirect, request

app = Flask(__name__)
active_user = user.User()



@app.route('/')
def index():
    if active_user.is_valid():
        return redirect('/login_redirect')
    return redirect('/login')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/logout')
def logout():
    active_user.invalidate()
    return redirect('/')

@app.route('/login2/<loginid>')
def login2(loginid):
    if active_user.login(loginid):
        return redirect('/login_redirect')
    else:
        return redirect("/error")


@app.route('/login_redirect')
def login_redirect():
    return redirect(active_user.get_home())

@app.route('/error')
def error():
    return render_template('error.html')

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

@app.route('/faculty/graduatesecretary')
def faculty_gradsec():
    if(active_user.isFaculty()):
        if active_user.get_graduate_secretary_status():
            return render_template('faculty_gs.html', gsrecords=active_user.gradsec.gs_records)
    return redirect('/error')

@app.route('/faculty/update_admission/<admissionid>')
def update_admission(admissionid):
    if active_user.isFaculty():
        if active_user.gradsec.isGS:
            app_to_review = applicant_info.Application()
            app_to_review.get_application_for_gs_review(admissionid)
            user_to_review = user.User()
            user_to_review.get_user_data_for_id(app_to_review.applicantid)
            user_to_review.applicantinfo.application = app_to_review
            return render_template('faculty_gs_update_admission.html', admission_user=user_to_review)
    return redirect("/error")

@app.route('/faculty/update_admission_submit', methods=['POST'])
def update_admission_submit():
    if active_user.isFaculty():
        if active_user.gradsec.isGS:
            applicationform = request.form
            graduate_secretary.process_gs_update(applicationform)
            return redirect("/faculty/graduatesecretary")
    return redirect("/error")

@app.route('/applicant/home')
def applicant_home():
    if(active_user.isApplicant()):
        if not active_user.applicantInfoExists():
            active_user.get_applicant_info()
        if active_user.submittedApplication():
            return render_template('applicant_home.html', applicationSubmitted=1)
        else:
            return render_template('applicant_home.html', applicationSubmitted=0)
    else:
        return redirect('/error')

@app.route('/applicant/application')
def applicant_application():
    if(active_user.isApplicant()):
        if not active_user.submittedApplication():
            return render_template('applicant_application.html', applicantid=active_user.id)
    return redirect('/error')

@app.route('/applicant/submit', methods=['POST'])
def applicant_submit():
    if(active_user.isApplicant()):
        if not active_user.submittedApplication():
            applicationform = request.form
            active_user.buildApplicantUser(applicationform)
            active_user.save()
            active_user.login(active_user.id)
            return redirect('/applicant/success')
    return redirect('/error')

@app.route('/applicant/success')
def applicant_success():
    if(active_user.isApplicant()):
        return render_template('applicant_success.html')
    return redirect('/error')

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