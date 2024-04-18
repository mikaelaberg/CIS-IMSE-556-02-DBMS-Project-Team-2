import psycopg2
from db_config import db_config

class Applicant_info:
    def __init__(self):
        self.applicantId = ''
        self.gre_verbal = 0
        self.gre_analytical = 0
        self.gre_quantitative = 0
        self.transcript_received = 'N'
        self.work_experience = ''
        self.application = 0

    def submitted_application(self):
        if self.application:
            return True
        else:
            return False

    def buildApplicantInfo(self, admissiontuple):
        if self.applicantId == admissiontuple[0]:
            self.gre_verbal = admissiontuple[1]
            self.gre_analytical = admissiontuple[2]
            self.gre_quantitative = admissiontuple[3]
            self.transcript_received = admissiontuple[4]
            self.work_experience = admissiontuple[5]
            return True
        return False

    def get_applicant_info(self):
        try:
            conn = psycopg2.connect(**db_config)
            cur = conn.cursor()
            cur.execute("""
                   SELECT * FROM starrs."APPLICANT" WHERE "USER_ID" = %s;
                   """,
                        [self.applicantId])
            applicant_row = cur.fetchone()
            success = self.buildApplicantInfo(applicant_row)
            cur.close()
            conn.close()
            self.get_application()
            return success
        except Exception as e:
            return False

    def get_application(self):
        dbApplication = Application()
        dbApplication.applicantid = self.applicantId
        if dbApplication.get_application():
            self.application = dbApplication


class Application:
    def __init__(self):
        self.admissionid = 0
        self.applicantid = ''
        self.area_of_interest = ''
        self.expected_date = ''
        self.admission_date = ''
        self.committee_decision = ''
        self.admission_ranking = ''
        self.admission_comment = ''
        self.recommended_advisor = ''
        self.letters = []

    def isValid(self):
        return self.admissionid > 0

    def get_application(self):
        try:
            conn = psycopg2.connect(**db_config)
            cur = conn.cursor()
            cur.execute("""
                   SELECT * FROM starrs."ADMISSION" WHERE "STUDENT_ID" = %s;
                   """,
                        [self.applicantid])
            admission_row = cur.fetchone()
            if admission_row is not None:
                success = self.buildApplication(admission_row)
            else:
                success = False
            cur.close()
            conn.close()
            return success
        except Exception as e:
            return False

    def buildApplication(self, applicationTuple):
        if self.applicantid == applicationTuple[1]:
            self.admissionid = applicationTuple[0]
            self.area_of_interest = applicationTuple[2]
            self.expected_date = applicationTuple[3]
            self.admission_date = applicationTuple[4]
            self.committee_decision = applicationTuple[5]
            self.admission_ranking = applicationTuple[6]
            self.admission_comment = applicationTuple[7]
            self.recommended_advisor = applicationTuple[8]
            return True
        return False

class Recommendation_letter:
    def __init__(self):
        self.letter_id = 0
        self.admissionid = 0
        self.letter_qty = 0
        self.letter_score = 0
        self.writer = Recommendation_letter_writer()

class Recommendation_letter_writer:
    def __init__(self):
        self.fname = ''
        self.mname = ''
        self.lname = ''
        self.title = ''
        self.affiliation = ''
        self.homephone = ''
        self.cellphone = ''
        self.email = ''
        self.street = ''
        self.city = ''
        self.state = ''
        self.country = ''
        self.zip = ''