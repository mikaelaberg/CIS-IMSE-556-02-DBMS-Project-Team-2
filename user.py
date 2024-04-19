import psycopg2
import applicant_info
from db_config import db_config
import graduate_secretary
from flask import Flask, render_template, jsonify

class User:
    def __init__(self):
        self.id = ''
        self.role = ''
        self.fname = ''
        self.mname = ''
        self.lname = ''
        self.sex = ''
        self.homephone = ''
        self.cellphone = ''
        self.workphone = ''
        self.email = ''
        self.street = ''
        self.city = ''
        self.state = ''
        self.country = ''
        self.zip = ''
        self.applicantinfo = applicant_info.Applicant_info()



    def login(self, id):
        self.id = id

        self.gradsec = graduate_secretary.GraduateSecretary()


    def login(self, login_id):
        return self.get_user_data_for_id(login_id)

    def get_user_data_for_id(self, user_id):
        self.id = user_id

        try:
            conn = psycopg2.connect(**db_config)
            cur = conn.cursor()
            cur.execute("""
                SELECT * FROM starrs."USER_V" WHERE "USER_ID" = %s;
                """,
                [self.id])
            user_row = cur.fetchone()
            success = self.build_user(user_row)
            cur.close()
            conn.close()
            return success
        except Exception as e:
            return False

    def is_valid(self):
        valid = False
        if self.role:
            valid = True
        return valid

    def invalidate(self):
        self.id = ''
        self.role = ''
        self.fname = ''
        self.mname = ''
        self.lname = ''
        self.sex = ''
        self.homephone = ''
        self.cellphone = ''
        self.workphone = ''
        self.email = ''
        self.street = ''
        self.city = ''
        self.state = ''
        self.country = ''
        self.zip = ''

    def get_home(self):
        if(self.role == 'Applicant'):
            return '/applicant/home'
        if (self.role == 'Grad_Student'):
            return '/course_registration'
        if (self.role == 'Alumni'):
            return '/alumni_page'
        if (self.role == 'Faculty'):
            return '/faculty_page'
        return '/login'

    #Applicant methods
    def isApplicant(self):
        return self.role == 'Applicant'

    def submittedApplication(self):
        if self.isApplicant():
            return self.applicantinfo.submitted_application()
        return False

=
    def processApplicantApplication(self, form):
        self.buildApplicantUser(form)

    def buildApplicantUser(self, form):
        self.fname = form['fname']
        self.mname = form['mname']
        self.lname = form['lname']
        self.sex = ''#form['']
        self.homephone = form['homephone']
        self.cellphone = form['mobilephone']
        self.workphone = form['workphone']
        self.email = form['email']
        self.street = form['street']
        self.city = form['city']
        self.state = form['state']
        self.country = 'US'
        self.zip = form['zip']
        self.applicantinfo = applicant_info.Applicant_info()
        self.applicantinfo.applicantId = self.id
        self.applicantinfo.buildApplicantInfoFromForm(form)


    def applicantInfoExists(self):
        return (self.applicantinfo.applicantId != '')
    def get_applicant_info(self):
        if self.isApplicant():
            self.applicantinfo.applicantId = self.id
            return self.applicantinfo.get_applicant_info()
        return False

    #Grad Student Methods
    def isGradStudent(self):
        return self.role == 'Grad_Student'


    def isAlumni(self):
        return self.role == 'Alumni'

    def isFaculty(self):
        return self.role == 'Faculty'


    #Alumni Methods
    def isAlumni(self):
        return self.role == 'Alumni'

    #Faculty Methods
    def isFaculty(self):
        return self.role == 'Faculty'

    def get_graduate_secretary_status(self):
        if self.isFaculty():
            self.gradsec.faculty_id = self.id
            self.gradsec.check_for_gs_records()
            return self.gradsec.isGS
        return False

    def build_user(self, user_tuple):
        if self.id == user_tuple[0]:
            self.role = user_tuple[1]
            self.fname = user_tuple[2]
            self.mname = user_tuple[3]
            self.lname = user_tuple[4]
            self.sex = user_tuple[5]
            self.homephone = user_tuple[6]
            self.cellphone = user_tuple[7]
            self.workphone = user_tuple[8]
            self.email = user_tuple[9]
            self.street = user_tuple[10]
            self.city = user_tuple[11]
            self.state = user_tuple[12]
            self.country = user_tuple[13]
            self.zip = user_tuple[14]

            return True

        return False

    def save(self):
        self.saveuserfields()

        if self.isApplicant():
            if self.applicantInfoExists():
                self.applicantinfo.save()

    def saveuserfields(self):
        try:
            conn = psycopg2.connect(**db_config)
            cur = conn.cursor()
            cur.execute("""
                                UPDATE starrs."USER"
	                            SET "FIRST_NAME"=%s, "MIDDLE_NAME"=%s, "LAST_NAME"=%s, "SEX"=%s, 
	                            "HOME_PHONE"=%s, "CELL_PHONE"=%s, "WORK_PHONE"=%s, "EMAIL"=%s, 
	                            "STREET_ADDRESS"=%s, "CITY"=%s, "STATE"=%s, "COUNTRY"=%s, "ZIP_CODE"=%s
	                            WHERE "USER_ID"=%s;
                              """,
                        [self.fname, self.mname, self.lname, self.sex,
                         self.homephone, self.cellphone, self.workphone, self.email,
                         self.street, self.city, self.state, self.country, self.zip, self.id])
            conn.commit()
            cur.close()
            conn.close()
            return True
        except Exception as e:
            return False

