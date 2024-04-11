import psycopg2
import user
from dbconfig import db_config
from flask import Flask, render_template, jsonify, redirect

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

