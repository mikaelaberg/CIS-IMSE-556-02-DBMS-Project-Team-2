import psycopg2

import alumni
import applicant_info
import graduate_secretary
import user
import sys
import traceback
import admission_review
from datetime import datetime
from dbconfig import db_config
from flask import Flask, render_template, jsonify, session, redirect, request, flash, url_for

app = Flask(__name__)
active_user = user.User()
app.secret_key = 'your_secret_key'  # Needed for flashing messages

def get_pending_applications():
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT "ADMISSION_ID" 
            FROM starrs."ADMISSION" 
            WHERE "ADMISSION_STATUS" = 'Complete' AND 
            "ADMISSION_ID" NOT IN (
                SELECT "ADMISSION_ID" 
                FROM starrs."ADMISSION_REVIEW"
            )
        ''')
        pending_applications = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return pending_applications
    except psycopg2.Error as e:
        print("Error retrieving pending applications:", e)
        return []


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
        session['user_id'] = active_user.id  # Assign the user ID to the session
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
    alumni_details = alumni.Alumni()
    alumni_details.get_alumni_for_id(active_user.id)
    return render_template('alumni_page.html', userdetails=alumni_details)


@app.route('/faculty/graduatesecretary')
def faculty_gradsec():
    if (active_user.isFaculty()):
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
            committee_review = admission_review.get_review_for_admission(admissionid)
            return render_template('faculty_gs_update_admission.html', admission_user=user_to_review, creview=committee_review)
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
    if (active_user.isApplicant()):
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
    if (active_user.isApplicant()):
        if not active_user.submittedApplication():
            return render_template('applicant_application.html', applicantid=active_user.id)
    return redirect('/error')


@app.route('/applicant/submit', methods=['POST'])
def applicant_submit():
    if (active_user.isApplicant()):
        if not active_user.submittedApplication():
            applicationform = request.form
            active_user.buildApplicantUser(applicationform)
            active_user.save()
            active_user.login(active_user.id)
            return redirect('/applicant/success')
    return redirect('/error')


@app.route('/applicant/success')
def applicant_success():
    if (active_user.isApplicant()):
        return render_template('applicant_success.html')
    return redirect('/error')


@app.route('/applicant/status')
def applicant_status():
    if(active_user.isApplicant()):
        active_user.applicantinfo.applicantId = active_user.id
        active_user.applicantinfo.get_application_status()
        return render_template('applicant_status.html', appstatus=active_user.applicantinfo.status)
    return redirect('/error')


@app.route('/applicant/enroll')
def applicant_enroll():
    if(active_user.isApplicant()):
        if not active_user.applicantInfoExists():
            active_user.get_applicant_info()
        if(active_user.enroll()):
            relogin = '/login2/' + active_user.id
            return redirect(relogin)
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


# 20240415-MB addition -- 20240421 notes: might not need this at all?? might be able to combine with audit below
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
    degree_program = request.form['degree_program']
    print("Received USER_ID:", user_id, degree_program)  # Initial reception of USER_ID

    try:
        conn = psycopg2.connect(**db_config)
        cur = conn.cursor()
        errors = []

        # First, verify the USER_ID and DEGREE_PROGRAM combination
        cur.execute('SELECT * FROM "starrs"."GRADUATE_STUDENT_V" WHERE "USER_ID" = %s AND "DEGREE_PROGRAM" = %s',
                    (user_id, degree_program))
        data = cur.fetchall()

        if not data:
            # No data found for the combination of USER_ID and DEGREE_PROGRAM
            flash("Not a valid Student ID or you are not enrolled in this degree. Try again.", "error")
            return render_template('graduation_application.html', data=None)

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
            cur.execute('UPDATE "starrs"."GRADUATE_STUDENT" SET "STATUS" = %s WHERE "USER_ID" = %s', (status, user_id,))
            conn.commit()
        except Exception as e:
            flash(f"An error occurred during database update: {e}", "error")
            conn.rollback()

        # Fetch data to display
        cur.execute('SELECT * FROM "starrs"."GRADUATE_STUDENT_V" WHERE "USER_ID" = %s AND "DEGREE_PROGRAM" = %s',
                    (user_id, degree_program))
        data = cur.fetchall()
        if data:
            flash("Audit completed successfully. Your details are below.", "success")
        else:
            flash("No data found or audit failed. Please check the Student ID and Degree Program.", "error")
            data = None

    except Exception as e:
        flash(f"An error occurred: {e}", "error")
        return render_template('graduation_application.html', data=[])
    finally:
        cur.close()
        conn.close()

    return render_template('graduation_application.html', data=data)


# 20240417 - MB

# Ensure this is the only place where '/faculty' route is defined

@app.route('/pending_applications')
def pending_applications():
    pendingApplications = get_pending_applications()
    return jsonify(pendingApplications=pendingApplications)

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
        return render_template('faculty_page.html', students=students, activeuserid=active_user.id)
    except Exception as e:
        print(f"An error occurred: {e}")
        return render_template('faculty_page.html', students=[], activeuserid=active_user.id)


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
@app.route('/check_audit_status', methods=['POST'])
def check_audit_status():
    user_id = request.form['user_id']
    try:
        conn = psycopg2.connect(**db_config)
        cur = conn.cursor()

        # Fetch user's current audit status and necessary details
        cur.execute('SELECT "USER_ID", "STATUS", "DEGREE_PROGRAM", "ADMITTED_SEMESTER", gpa, total_credit_hrs FROM "starrs"."GRADUATE_STUDENT_V" WHERE "USER_ID" = %s', (user_id,))
        data = cur.fetchall()  # fetchall to handle potentially multiple records

        if not data:
            flash("No record found for the given Student ID.", "error")
            return render_template('graduation_application.html', data=[], show_graduate_button=False)

        flash("Status fetched successfully.", "success")
        # Check if any record has the status 'APPROVED' to determine if we show the graduate button
        show_graduate_button = any(row[1] == 'APPROVED' for row in data)
        return render_template('graduation_application.html', data=data, show_graduate_button=show_graduate_button)
    except Exception as e:
        flash(f"An error occurred while fetching the data: {e}", "error")
        return render_template('graduation_application.html', data=[], show_graduate_button=False)
    finally:
        cur.close()
        conn.close()


@app.route('/submit_course_registration', methods=['POST'])
def submit_course_registration():
    try:
        # Access form data
        course_no = request.form['course_no']
        course_title = request.form['course_title']
        semester = request.form['semester']
        year = request.form['year']
        department = request.form['department']

        # Initialize the SQL query to fetch courses
        course_query = "SELECT * FROM starrs.\"COURSE\" WHERE 1=1"

        # Add conditions based on form inputs
        if course_no:
            course_query += f" AND \"COURSE_NO\" = '{course_no}'"
        if course_title:
            course_query += f" AND \"TITLE\" = '{course_title}'"
        if department != 'Any':
            course_query += f" AND \"DEPARTMENT\" = '{department}'"

        conn = psycopg2.connect(**db_config)
        cur = conn.cursor()

        # Execute the SQL query to fetch courses
        cur.execute(course_query)
        courses = cur.fetchall()

        course_info = []
        for course in courses:
            course_sections_query = f"""
                SELECT
                    s.*,
                    u."FIRST_NAME",
                    u."LAST_NAME",
                    EXISTS (
                        SELECT 1
                        FROM starrs."ATTENDS_SECTION" a
                        WHERE
                            a."USER_ID" = %s
                            AND a."SECTION_NO" = s."SECTION_NO"
                            AND a."SEMESTER" = s."SEMESTER"
                            AND a."YEAR" = s."YEAR"
                    ) AS "enrolled"
                FROM
                    starrs."SECTION" s
                INNER JOIN
                    starrs."USER" u ON s."INSTRUCTOR_ID" = u."USER_ID"
                WHERE
                    s."COURSE_NO" = '{course[0]}'"""

            # Add conditions for semester and year
            if semester != 'Any':
                course_sections_query += f" AND s.\"SEMESTER\" = '{semester}'"
                if year != 'Any':
                    course_sections_query += f" AND s.\"YEAR\" = '{year}'"
            else:
                if year != 'Any':
                    course_sections_query += f" AND s.\"YEAR\" = '{year}'"

            cur.execute(course_sections_query, (session.get('user_id'),))  # Pass user_id as parameter
            sections = cur.fetchall()
            course_info.append((course, sections))

        # Render the template with the course information
        return render_template('course_results.html', course_info=course_info)
    except psycopg2.Error as e:
        # Print the error message and traceback for debugging
        print("Error executing SQL query:", e)
        traceback.print_exc()
        # Optionally, render an error page with a user-friendly message
        return render_template('error.html', message="An error occurred while fetching course information.")

# Course Enrollment------------------------------------------------------------------------------------------

@app.route('/enroll_course', methods=['POST'])
def enroll_course():
    try:
        # Access form data from the request object
        student_id = active_user.id  # Get student ID from session
        course_no = request.form['course_no']
        section_no = request.form['section_no']
        semester = request.form['semester']
        year = request.form['year']
        instructor_id = request.form['instructor_id']  # Added instructor ID

        # Print the enrolled course information
        print("Enrolled Course Information:")
        print("Student ID:", student_id)
        print("Course Number:", course_no)
        print("Section Number:", section_no)
        print("Semester:", semester)
        print("Year:", year)

        # Establish connection to the database
        conn = psycopg2.connect(**db_config)
        cur = conn.cursor()

        # Insert enrollment data into the ATTENDS_SECTION table
        cur.execute("""
            INSERT INTO starrs."ATTENDS_SECTION" (
                "USER_ID", "COURSE_NO", "SECTION_NO", "SEMESTER", "YEAR", "GRADE", "REGISTRATION STATUS")
            VALUES (%s, %s, %s, %s, %s, NULL, 'Registered')
        """, (student_id, course_no, section_no, semester, year))

        # Commit the transaction
        conn.commit()

        # Close cursor and connection
        cur.close()
        conn.close()

        # Return a success response
        return jsonify({'message': 'Enrollment successful'})

    except Exception as e:
        # Handle exceptions
        print("Error:", e)
        # Rollback the transaction in case of an error
        conn.rollback()  # Added rollback
        # Optionally, return an error response
        return jsonify({'error': 'Enrollment failed'}), 500

@app.route('/drop_course', methods=['POST'])
def drop_course():
    try:
        # Access form data
        course_no = request.form['course_no']
        section_no = request.form['section_no']
        semester = request.form['semester']
        year = request.form['year']
        instructor_id = request.form['instructor_id']

        # Check if the section is enrolled for the user ID in the ATTENDS_SECTION table
        user_id = session.get('user_id')
        if not user_id:
            return render_template('error.html', message="User ID not found in session.")

        conn = psycopg2.connect(**db_config)
        cur = conn.cursor()

        cur.execute("""
            DELETE FROM starrs."ATTENDS_SECTION"
            WHERE "USER_ID" = %s AND "SECTION_NO" = %s AND "SEMESTER" = %s AND "YEAR" = %s
            RETURNING 1
            """,
                    (user_id, section_no, semester, year, instructor_id))
        deleted = cur.fetchone()

        # If the record is deleted successfully, return a success message
        if deleted:
            return jsonify({'message': 'Course dropped successfully'})

        # If the record does not exist, return an error message
        else:
            return jsonify({'error': 'Course not found or not enrolled'}), 404

    except Exception as e:
        # Handle exceptions
        print("Error:", e)
        # Optionally, return an error response
        return jsonify({'error': 'Failed to drop course'}), 500

    finally:
        # Close database connection
        cur.close()
        conn.close()

# Registration Record--------------------------------------------------------------------------------------------------------------
#

@app.route('/search_attendance_records', methods=['POST'])
def search_attendance_records():
    try:
        # Access user ID from session
        user_id = active_user.id
        if not user_id:
            return render_template('error.html', message="Unable to recognize ID.")

        conn = psycopg2.connect(**db_config)
        cur = conn.cursor()

        # Fetch user information from the database
        user_query = f"""
            SELECT "USER_ID", "FIRST_NAME", "MIDDLE_NAME", "LAST_NAME", "EMAIL", "STREET_ADDRESS", "CITY", "STATE", "COUNTRY", "ZIP_CODE", "CELL_PHONE","WORK_PHONE"     
            FROM starrs."USER"
            WHERE "USER_ID" = '{user_id}'
        """

        cur.execute(user_query)
        user_data = cur.fetchone()

        # Fetch records from AttendSection table for the user ID
        attend_section_query = f"""
            SELECT a.*, c."COURSE_NO", c."TITLE", c."CREDITS", c."DEPARTMENT", s."SECTION_NO", s."SEMESTER", s."YEAR"
            FROM starrs."ATTENDS_SECTION" a
            INNER JOIN starrs."SECTION" s ON a."SECTION_NO" = s."SECTION_NO"
            INNER JOIN starrs."COURSE" c ON s."COURSE_NO" = c."COURSE_NO"
            WHERE a."USER_ID" = '{user_id}'
        """

        cur.execute(attend_section_query)
        records = cur.fetchall()

        # Render the template with the fetched records and user information
        return render_template('registration_record.html', records=records, user=user_data)

    except psycopg2.Error as e:
        # Handle database errors
        print("Error executing SQL query:", e)
        traceback.print_exc()
        return render_template('error.html', message="An error occurred while fetching records.")

    finally:
        # Close database connection if applicable
        pass  # Adjust this according to your database handling

# GS/Faculty Grading--------------------------------------------------------------------------------------------------------------

@app.route('/student_academic_management')
def student_academic_management():
    return render_template('student_academic_management.html')

@app.route('/submit_student_academic', methods=['POST'])
def submit_student_academic():
    return render_template('student_academic_result.html')

# @app.route('/search_student_academic_records', methods=['POST'])
# def search_student_academic_records():
#     try:
#         # Access student ID and course number from the form data
#         student_id = request.form.get('student_id')
#         course_no = request.form.get('course_no')
#
#         if student_id and course_no:
#             conn = psycopg2.connect(**db_config)
#             cur = conn.cursor()
#
#             # Use parameterized query to prevent SQL injection
#             attend_section_query = """
#                 SELECT *
#                 FROM starrs."ATTENDS_SECTION"
#                 WHERE "STUDENT_ID" = %s AND "COURSE_NO" = %s
#             """
#
#             cur.execute(attend_section_query, (student_id, course_no))
#             records = cur.fetchall()
#
#             # Render the template with the fetched records
#             return render_template('student_academic_result.html', records=records)
#         else:
#             # If student ID or course number is not provided, display an error message
#             return render_template('student_academic_result.html', message="Please enter both student ID and course number.")
#
#     except psycopg2.Error as e:
#         # Handle database errors
#         print("Error executing SQL query:", e)
#         traceback.print_exc()
#         return render_template('error.html', message="An error occurred while fetching records.")
#     finally:
#         # Close cursor and connection
#         if cur:
#             cur.close()
#         if conn:
#             conn.close()
#

@app.route('/search_student_academic_records', methods=['POST'])
def search_student_academic_records():
    try:
        # Access student ID and course number from the form data
        student_id = request.form.get('student_id')
        course_no = request.form.get('course_no')

        if student_id and course_no:
            conn = psycopg2.connect(**db_config)
            cur = conn.cursor()

            # Use parameterized query to prevent SQL injection
            attend_section_query = """
                SELECT a.*, c."COURSE_NO", c."TITLE", c."CREDITS", c."DEPARTMENT", s."SECTION_NO", s."SEMESTER", s."YEAR",
                       u."FIRST_NAME" AS instructor_first_name, u."LAST_NAME" AS instructor_last_name
                FROM starrs."ATTENDS_SECTION" a
                INNER JOIN starrs."SECTION" s ON a."SECTION_NO" = s."SECTION_NO"
                INNER JOIN starrs."COURSE" c ON s."COURSE_NO" = c."COURSE_NO"
                INNER JOIN starrs."USER" u ON s."INSTRUCTOR_ID" = u."USER_ID"
                WHERE a."USER_ID" = %s AND a."COURSE_NO" = %s
            """

            cur.execute(attend_section_query, (student_id, course_no))
            records = cur.fetchall()

            # Render the template with the fetched records
            return render_template('student_academic_result.html', records=records)
        else:
            # If student ID or course number is not provided, display an error message
            return render_template('student_academic_result.html',
                                   message="Please enter both student ID and course number.")

    except psycopg2.Error as e:
        # Handle database errors
        print("Error executing SQL query:", e)
        traceback.print_exc()
        return render_template('error.html', message="An error occurred while fetching records.")
    finally:
        # Close cursor and connection
        if cur:
            cur.close()
        if conn:
            conn.close()

@app.route('/update_record', methods=['POST'])
def update_record():
    try:
        # Establish connection to the database
        conn = psycopg2.connect(**db_config)
        cur = conn.cursor()

        # Iterate over form data to update records
        for key, value in request.form.items():
            if key.startswith('grade_'):
                # Extract student_id, course_no, and section_no from the form field name
                prefix_length = len('grade_')
                identifiers = key[prefix_length:].split('_')
                if len(identifiers) == 3:
                    student_id, course_no, section_no = identifiers
                else:
                    continue

                # Get the registration status corresponding to the grade
                status_key = f"status_{student_id}_{course_no}_{section_no}"
                registration_status = request.form.get(status_key)

                # Ensure NULL values for grade if not "completed" or "dropped" status
                if registration_status not in ["Completed", "Dropped"]:
                    value = None

                print("Updating record with the following details:")
                print("Student ID:", student_id)
                print("Course Number:", course_no)
                print("Section Number:", section_no)
                print("Grade:", value)
                print("Registration Status:", registration_status)

                # Update the record in the database
                cur.execute("""
                    UPDATE starrs."ATTENDS_SECTION"
                    SET "GRADE" = %s, "REGISTRATION STATUS" = %s
                    WHERE "USER_ID" = %s AND "COURSE_NO" = %s AND "SECTION_NO" = %s
                """, (value, registration_status, student_id, course_no, section_no))

                print("Record updated successfully.")

        # Commit the transaction
        conn.commit()

        # Close cursor and connection
        cur.close()
        conn.close()

        # Return a success response
        return jsonify({'message': 'Records updated successfully'})
    except Exception as e:
        # Handle exceptions
        print("Error:", e)
        # Rollback the transaction in case of an error
        conn.rollback()
        # Optionally, return an error response
        return jsonify({'error': 'Failed to update records'}), 500

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


