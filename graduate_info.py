import psycopg2
from db_config import db_config

class Graduate_info:
    def __init__(self):
        self.graduateId = ''
        self.status = ''
        self.degree_program = ''
        self.admitted_semester = ''
        self.application = None

    def submitted_audit(self):
        return bool(self.application)

    def build_graduate_info(self, graduatetuple):
        if self.graduateId == graduatetuple[0]:
            self.status = graduatetuple[1]
            self.degree_program = graduatetuple[2]
            self.admitted_semester = graduatetuple[3]
            return True
        return False

    def get_graduate_info(self):
        try:
            with psycopg2.connect(**db_config) as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT * FROM starrs.\"GRADUATE_STUDENT\" WHERE \"USER_ID\" = %s;", [self.graduateId])
                    applicant_row = cur.fetchone()
            if applicant_row:
                success = self.build_graduate_info(applicant_row)
                self.get_application()
                return success
            return False
        except Exception as e:
            print(f"Database error: {e}")
            return False

    def get_application(self):
        dbApplication = Grad_application()
        dbApplication.graduateId = self.graduateId
        if dbApplication.get_grad_application():
            self.application = dbApplication

class Grad_application:
    def __init__(self):
        self.applicationid = ''
        self.studentID = ''
        self.status = ''
        self.decision_date = ''
        self.decision = ''

    def is_valid(self):
        return bool(self.applicationid)

    def get_grad_application(self):
        try:
            with psycopg2.connect(**db_config) as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT * FROM starrs.\"GRAD_APPLICATION\" WHERE \"USER_ID\" = %s;", [self.studentID])
                    audit_row = cur.fetchone()
            if audit_row:
                return self.build_grad_application(audit_row)
            return False
        except Exception as e:
            print(f"Database error: {e}")
            return False

    def build_grad_application(self, gradApplicationTuple):
        if self.studentID == gradApplicationTuple[1]:
            self.applicationid = gradApplicationTuple[0]
            self.status = gradApplicationTuple[2]
            self.decision_date = gradApplicationTuple[3]
            self.decision = gradApplicationTuple[4]
            return True
        return False
