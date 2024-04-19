import psycopg2

import applicant_info
import graduate_secretary
import user
import sys
from datetime import datetime
from dbconfig import db_config
from flask import Flask, render_template, jsonify, redirect, request, flash, url_for

app = Flask(__name__)
active_user = user.User()
app.secret_key = 'your_secret_key'  # Needed for flashing messages


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

@app.route('/graduate')
def graduate_page():
    try:
        conn = psycopg2.connect(**db_config)
        cur = conn.cursor()
        cur.execute("SET search_path TO starrs, public;")
        cur.execute('SELECT * FROM "starrs"."GRADUATE_STUDENT_V";')
        data = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)})


# 20240415-MB addition
@app.route('/search_student', methods=['POST'])
def search_student():
    user_id = request.form['user_id']  # from grad app student entry
    degree_program = request.form['degree_program']  # from grad app html drop down
    try:
        conn = psycopg2.connect(**db_config)
        cur = conn.cursor()

        # First, verify the USER_ID and DEGREE_PROGRAM combination
        cur.execute('SELECT * FROM "starrs"."GRADUATE_STUDENT_V" WHERE "USER_ID" = %s AND "DEGREE_PROGRAM" = %s',
                    (user_id, degree_program))
        data = cur.fetchall()

        if not data:
            # No data found for the combination of USER_ID and DEGREE_PROGRAM
            flash("Not a valid Student ID or you are not enrolled in this degree. Try again.", "error")
            return render_template('graduation_application.html', data=None)

        # Data found, pass it to the template
        return render_template('graduation_application.html', data=data)
    except Exception as e:
        print("Database error:", e, file=sys.stderr)  # Print any database errors to stderr
        flash("An error occurred while fetching your data: " + str(e), "error")
        return render_template('graduation_application.html', data=None)
    finally:
        cur.close()
        conn.close()

@app.route('/audit_student', methods=['POST'])
def audit_student():
    user_id = request.form['user_id']
    print("Received USER_ID:", user_id)  # Initial reception of USER_ID

    try:
        conn = psycopg2.connect(**db_config)
        cur = conn.cursor()
        errors = []

        # First, check if the USER_ID exists at all
        cur.execute('SELECT "USER_ID" FROM "starrs"."GRADUATE_STUDENT_V" WHERE "USER_ID" = %s', (user_id,))
        result = cur.fetchone()
        print("User ID check:", result)  # Debug print
        if not result:
            flash("Not a valid USER_ID.", "error")
            return render_template('graduation_application.html', data=[])

        # Check for total credit hours and GPA
        cur.execute('SELECT total_credit_hrs, gpa FROM "starrs"."GRADUATE_STUDENT_V" WHERE "USER_ID" = %s', (user_id,))
        result = cur.fetchone()
        if result and all(r is not None for r in result):
            credit_total, gpa = result
            print("Credit and GPA fetch result:", credit_total, gpa)
            if credit_total < 30:
                errors.append("Total credit hours less than 30.")
            if gpa < 3.0:
                errors.append("GPA below 3.0.")
        else:
            errors.append("Credit hours and GPA data not available.")

        # Check for grades below 3.0
        cur.execute('SELECT COUNT(*) FROM "starrs"."ATTENDS_SECTION" WHERE "USER_ID" = %s AND "GRADE" < 3.0',
                    (user_id,))
        result = cur.fetchone()
        print("Low grades check:", result)
        if result and result[0] > 2:
            errors.append("More than two grades below 3.0.")

        # Check if student is currently enrolled in classes for 2024 or later
        cur.execute('SELECT COUNT(*) FROM "starrs"."ATTENDS_SECTION" WHERE "USER_ID" = %s AND "YEAR" >= 2024',
                    (user_id,))
        future_classes = cur.fetchone()[0]
        if future_classes > 0:
            errors.append("Student is currently enrolled in a class for 2024 or later.")

        # Update status based on audit result
        if not errors:
            status = "WAITING"  # Shortened from "WAITING FOR GS"
            flash("Passed initial audit waiting on GS approval", "success")
        else:
            status = "FAILED"
            status_message = "Failed initial audit for the following reasons: " + "; ".join(errors)
            flash(status_message, "error")

        # Ensure database update is outside the else condition
        try:
            cur.execute('UPDATE "starrs"."GRAD_APPLICATION" SET "STATUS" = %s WHERE "USER_ID" = %s', (status, user_id,))
            conn.commit()
        except Exception as e:
            flash(f"An error occurred during database update: {e}", "error")
            conn.rollback()

        return render_template('graduation_application.html', data=[])

    except Exception as e:
        flash(f"An error occurred: {e}", "error")
        return render_template('graduation_application.html', data=[])
    finally:
        cur.close()
        conn.close()


# 20240417 - MB

# Ensure this is the only place where '/faculty' route is defined
@app.route('/faculty')
def faculty_page():
    try:
        conn = psycopg2.connect(**db_config)
        cur = conn.cursor()
        cur.execute(
            'SELECT "USER_ID", "STATUS", "DEGREE_PROGRAM", "ADMITTED_SEMESTER", "gpa", "total_credit_hrs" FROM '
            '"starrs"."GRADUATE_STUDENT_V" WHERE "STATUS" = %s',
            ('WAITING',))
        students = cur.fetchall()  # Fetches all students in WAITING status
        cur.close()
        conn.close()
        return render_template('faculty_page.html', students=students)
    except Exception as e:
        print(f"An error occurred: {e}")
        return render_template('faculty_page.html', students=[])


@app.route('/submit_faculty_decision', methods=['POST'])
def submit_faculty_decision():
    faculty_id = request.form['faculty_id']
    student_id = request.form['student_id']
    decision = request.form['decision']
    decision_year = datetime.now().year  # Gets the current year
    # Create a date string representing January 1st of the decision year
    decision_date = f"{decision_year}-01-01"
    try:
        conn = psycopg2.connect(**db_config)
        cur = conn.cursor()
        # Validate faculty ID
        cur.execute('SELECT * FROM "starrs"."USER" WHERE "USER_ID" = %s', (faculty_id,))
        if not cur.fetchone():
            flash("Invalid faculty ID.", "error")
            return render_template('faculty_page.html', message="Invalid faculty ID.")

        # Validate student ID in GRAD_APPLICATION
        cur.execute('SELECT "APPLICATION_ID" FROM "starrs"."GRAD_APPLICATION" WHERE "USER_ID" = %s', (student_id,))
        app_data = cur.fetchone()
        cur.execute(
            'SELECT "APPLICATION_ID" FROM "starrs"."GRAD_APPLICATION" WHERE "USER_ID" = %s',
            (student_id,)
        )
        app_data = cur.fetchone()
        if not app_data:
            flash("No application found for the given student ID.", "error")
            return redirect(url_for('faculty_page'))

        application_id = app_data[0]  # Use the fetched application ID

        # Update GRAD_APPLICATION with the faculty's decision
        cur.execute(
            'UPDATE "starrs"."GRAD_APPLICATION" SET "STATUS" = %s, "DECISION" = %s, "DECISION_DATE" = %s WHERE "APPLICATION_ID" = %s',
            (decision, decision, decision_date, application_id)
        )

        # Update GRADUATION_REVIEW assuming it should also be updated similarly
        cur.execute(
            'UPDATE "starrs"."GRADUATION_REVIEW" SET "DECISION" = %s, "DECISION_DATE" = %s WHERE "APPLICATION_ID" = %s AND "REVIEWER_ID" = %s',
            (decision, decision_date, application_id, faculty_id)
        )
        # Optional: Update GRADUATE_STUDENT if applicable
        cur.execute(
            'UPDATE "starrs"."GRADUATE_STUDENT" SET "STATUS" = %s WHERE "USER_ID" = %s',
            (decision, student_id)
        )

        conn.commit()
        flash("Decision processed successfully.", "success")

    except Exception as e:
        conn.rollback()
        flash(f"An error occurred: {e}", "error")
        print(f"An error occurred: {e}")  # Logging the error
        return redirect(url_for('faculty_page'))  # Redirect back to the faculty page
    finally:
        cur.close()
        conn.close()

    return render_template('faculty_page.html', message="Decision processed successfully.")


# Added 20240418 - MB
@app.route('/student_page')
def student_page():
    user_id = request.args.get('user_id')  # Assuming you pass the user_id as a query parameter

    try:
        conn = psycopg2.connect(**db_config)
        cur = conn.cursor()
        # Fetch the latest status and other relevant details
        cur.execute(
            'SELECT "USER_ID", "STATUS", "DEGREE_PROGRAM", "ADMITTED_SEMESTER", "gpa", "total_credit_hrs" FROM '
            '"starrs"."GRADUATE_STUDENT_V" WHERE "USER_ID" = %s',
            (user_id,)
        )
        student_info = cur.fetchone()
        cur.close()
        conn.close()
        return render_template('graduation_application.html', student=student_info)
    except Exception as e:
        flash(f"An error occurred: {e}", "error")
        return render_template('graduation_application.html', student=None)


@app.route('/graduate_student', methods=['POST'])
def graduate_student():
    user_id = request.form['user_id']

    try:
        conn = psycopg2.connect(**db_config)
        cur = conn.cursor()

        # Fetch application_id first if not already passed directly
        cur.execute('SELECT "APPLICATION_ID" FROM "starrs"."GRAD_APPLICATION" WHERE "USER_ID" = %s', (user_id,))
        application_id = cur.fetchone()
        if not application_id:
            flash("No application found for this user.", "error")
            return redirect(url_for('graduation_application'))

        # Delete references in GRADUATION_REVIEW first
        cur.execute('DELETE FROM "starrs"."GRADUATION_REVIEW" WHERE "APPLICATION_ID" = %s', (application_id,))

        # Now delete the application record
        cur.execute('DELETE FROM "starrs"."GRAD_APPLICATION" WHERE "APPLICATION_ID" = %s', (application_id,))

        # Insert into ALUMNI
        cur.execute('''
            INSERT INTO "starrs"."ALUMNI" ("USER_ID", "DEGREE", "GPA", "GRADUATION_YEAR")
            SELECT "USER_ID", "DEGREE_PROGRAM", "gpa", EXTRACT(YEAR FROM CURRENT_DATE)
            FROM "starrs"."GRADUATE_STUDENT_V"
            WHERE "USER_ID" = %s
        ''', (user_id,))

        # Remove from GRADUATE_STUDENT
        cur.execute('DELETE FROM "starrs"."GRADUATE_STUDENT" WHERE "USER_ID" = %s', (user_id,))

        conn.commit()
        flash("Congratulations! You have graduated.", "success")
        return redirect(url_for('alumni_page'))
    except Exception as e:
        conn.rollback()
        flash(f"An error occurred: {e}", "error")
        return redirect(url_for('graduation_application'))
    finally:
        cur.close()
        conn.close()

@app.route('/test_db')
def test_db():
    try:
        conn = psycopg2.connect(**db_config)
        cur = conn.cursor()
        cur.execute('SELECT version();')
        db_version = cur.fetchone()
        cur.close()
        conn.close()
        return jsonify({"success": True, "PostgresSQL Version": db_version})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)