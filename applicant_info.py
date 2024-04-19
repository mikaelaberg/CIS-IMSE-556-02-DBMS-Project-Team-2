import psycopg2
from dbconfig import db_config

class Applicant_info:
    def __init__(self):
        self.applicantId = ''
        self.application = Application()
        self.application_ID = 0


    def submitted_application(self):
        if self.application.isValid():
            return True
        else:
            return False

    def buildApplicantInfo(self, admissiontuple):
        if self.applicantId == admissiontuple[0]:
            # self.gre_verbal = admissiontuple[1]
            # self.gre_analytical = admissiontuple[2]
            # self.gre_quantitative = admissiontuple[3]
            # self.transcript_received = admissiontuple[4]
            # self.work_experience = admissiontuple[5]
            self.application_ID = admissiontuple[6]
            return True
        return False

    def buildApplicantInfoFromForm(self, form):
        self.application = Application()
        self.application.applicantid = self.applicantId
        self.application.buildApplicationFromForm(form)

    def get_applicant_info(self):
        try:
            conn = psycopg2.connect(**db_config)
            cur = conn.cursor()
            cur.execute("""
                   SELECT * FROM starrs."APPLICANT" WHERE "USER_ID" = %s;
                   """,
                        [self.applicantId])
            applicant_row = cur.fetchone()
            if applicant_row is not None:
                success = self.buildApplicantInfo(applicant_row)
            else:
                success = False
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

    def save(self):
        self.application.save()
        self.application_ID = self.application.admissionid
        self.save_applicant_info_fields()
        self.assign_graduate_secretary()

    def save_applicant_info_fields(self):
        try:
            conn = psycopg2.connect(**db_config)
            cur = conn.cursor()
            cur.execute("""
                                UPDATE starrs."APPLICANT"
                                SET "ADMISSION_ID"=%s
                                WHERE "USER_ID"=%s;
                              """,
                        [self.application_ID, self.applicantId])
            conn.commit()
            cur.close()
            conn.close()
            return True
        except Exception as e:
            return False

    def assign_graduate_secretary(self):
        try:
            conn = psycopg2.connect(**db_config)
            cur = conn.cursor()
            cur.execute("""
                                INSERT INTO starrs."GRADUATE_SECRETARY"(
                                "ADMISSION_ID", "APPLICANT_ID", "GS_ID")
                                VALUES (%s, %s, '600000');
                               """,
                        [self.application_ID, self.applicantId])
            conn.commit()
            cur.close()
            conn.close()
            return True
        except Exception as e:
            return False

class Application:
    def __init__(self):
        self.admissionid = 0
        self.applicantid = ''
        self.area_of_interest = ''
        self.expected_date = ''
        self.admission_status = ''
        self.admission_date = ''
        self.committee_decision = ''
        self.admission_ranking = ''
        self.admission_comment = ''
        self.recommended_advisor = ''
        self.gre_total = 0
        self.gre_verbal = 0
        self.gre_analytical = 0
        self.gre_quantitative = 0
        self.transcript_received = 'N'
        self.work_experience = ''
        self.degree_sought = ''
        self.bachelor_degree = Applicant_Degree()
        self.masters_degree = Applicant_Degree()
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

    def get_application_for_gs_review(self, admission_id):
        self.admissionid = admission_id
        self.get_application_by_id()
        self.get_application_degrees()
        self.get_recommendation_letters()

    def get_application_by_id(self):
        try:
            conn = psycopg2.connect(**db_config)
            cur = conn.cursor()
            cur.execute("""
                   SELECT * FROM starrs."ADMISSION" WHERE "ADMISSION_ID" = %s;
                   """,
                        [self.admissionid])
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
        self.applicantid = applicationTuple[1]
        self.admissionid = applicationTuple[0]
        self.area_of_interest = applicationTuple[2]
        self.admission_status = applicationTuple[3]
        self.expected_date = applicationTuple[4]
        self.admission_date = applicationTuple[5]
        self.committee_decision = applicationTuple[6]
        self.admission_ranking = applicationTuple[7]
        self.admission_comment = applicationTuple[8]
        self.recommended_advisor = applicationTuple[9]
        self.gre_total = applicationTuple[10]
        self.gre_verbal = applicationTuple[11]
        self.gre_analytical = applicationTuple[12]
        self.gre_quantitative = applicationTuple[13]
        self.transcript_received = applicationTuple[14]
        self.work_experience = applicationTuple[15]
        self.degree_sought = applicationTuple[16]
        return True


    def buildApplicationFromForm(self, form):
        self.area_of_interest = form['aoi']
        self.expected_date = form['startsem'] + form['startyear']
        self.gre_total = form['gretotal']
        self.gre_verbal = form['greverbal']
        self.gre_analytical = form['greanalytical']
        self.gre_quantitative = form['grequant']
        self.transcript_received = 'N'
        self.work_experience = form['pwxp']
        self.degree_sought = form['degree']

        if form['bachyear'] != '':
            self.bachelor_degree = Applicant_Degree()
            self.bachelor_degree.buildUndergradDegreeFromForm(form)

        if form['msyear'] != '':
            self.masters_degree = Applicant_Degree()
            self.masters_degree.buildGradDegreeFromForm(form)

        if form['c1lname'] != '':
            recommendation = Recommendation_letter()
            recommendation.buildRecommendLetterFromForm(form)
            self.letters.append(recommendation)

        if form['c2lname'] != '':
            recommendation2 = Recommendation_letter()
            recommendation2.buildRecommendLetter2FromForm(form)
            self.letters.append(recommendation2)

        if form['c3lname'] != '':
            recommendation3 = Recommendation_letter()
            recommendation3.buildRecommendLetter3FromForm(form)
            self.letters.append(recommendation3)

    def get_application_degrees(self):
        try:
            conn = psycopg2.connect(**db_config)
            cur = conn.cursor()
            cur.execute("""
                   SELECT * FROM starrs."APPLICANT_DEGREE" WHERE "APPLICANT_ID" = %s;
                   """,
                        [self.applicantid])
            degrees = cur.fetchall()
            success = False
            if degrees is not None:
                success = self.build_degrees(degrees)
            cur.close()
            conn.close()
            return success
        except Exception as e:
            return False

    def get_recommendation_letters(self):
        try:
            conn = psycopg2.connect(**db_config)
            cur = conn.cursor()
            cur.execute("""
                   SELECT * FROM starrs."RECOMMENDATION_LETTER" WHERE "ADMISSION_ID" = %s;
                   """,
                        [self.admissionid])
            letters = cur.fetchall()
            success = False
            if letters is not None:
                success = self.build_letters(letters)
            cur.close()
            conn.close()
            return success
        except Exception as e:
            return False

    def build_degrees(self, db_rows):
        if len(db_rows) == 0:
            return False
        for row in db_rows:
            degree = Applicant_Degree()
            degree.build_degree_from_db(row)
            if degree.undergrad_grad == 'U':
                self.bachelor_degree = degree
            else:
                self.masters_degree = degree
        return True

    def build_letters(self, db_rows):
        if len(db_rows) == 0:
            return False
        for row in db_rows:
            letter = Recommendation_letter()
            letter.build_letter_from_db(row)
            if letter.isValid():
                self.letters.append(letter)
        return True

    def save(self):
        if not self.getadmissionid():
            self.save_admission_fields()
            self.getadmissionid()
            if self.bachelor_degree.isValid():
                self.bachelor_degree.save()
            if self.masters_degree.isValid():
                self.masters_degree.save()
            for letter in self.letters:
                if letter.isValid():
                    letter.admissionid = self.admissionid
                    letter.save()
        return True

    def save_admission_fields(self):
        try:
            conn = psycopg2.connect(**db_config)
            cur = conn.cursor()
            cur.execute("""
                                INSERT INTO starrs."ADMISSION"( "STUDENT_ID", "AREA_OF_INTEREST", "ADMISSION_STATUS", 
                                "EXPECTED_DATE", "ADMISSION_DATE", "COMMITTEE_DECISION", "ADMISSION_RANKING", 
                                "ADMISSION_COMMENT", "RECOMMENDED_ADVISOR", "GRE_TOTAL", "GRE_VERBAL", "GRE_ANALYTICAL", 
                                "GRE_QUANTITATIVE", "TRANSCRIPT_RECEIVED", "WORK_EXPERIENCE", "DEGREE_SOUGHT")
                                VALUES (%s, %s, 'Incomplete', %s, current_date, '', '', '', '', %s, %s, %s, %s, 'N', %s, %s);
                               """,
                        [self.applicantid, self.area_of_interest, self.expected_date, self.gre_total,
                         self.gre_verbal, self.gre_analytical, self.gre_quantitative, self.work_experience, self.degree_sought])
            conn.commit()
            cur.close()
            conn.close()
            return True
        except Exception as e:
            return False

    def gs_update(self):
        self.gs_update_admission_fields()
        for letter in self.letters:
            letter.gs_update()
        return True

    def gs_update_admission_fields(self):
        try:
            conn = psycopg2.connect(**db_config)
            cur = conn.cursor()
            cur.execute("""
                                UPDATE starrs."ADMISSION"
                                SET "TRANSCRIPT_RECEIVED"=%s, "ADMISSION_STATUS"=%s
                                WHERE "ADMISSION_ID"=%s;
                               """,
                        [self.transcript_received, self.admission_status, self.admissionid])
            conn.commit()
            cur.close()
            conn.close()
            return True
        except Exception as e:
            return False

    def getadmissionid(self):
        try:
            conn = psycopg2.connect(**db_config)
            cur = conn.cursor()
            cur.execute("""
                   SELECT "ADMISSION_ID" FROM starrs."ADMISSION" WHERE "STUDENT_ID" = %s;
                   """,
                        [self.applicantid])
            dbreturn = cur.fetchone()
            success = False
            if dbreturn is not None:
                self.admissionid = dbreturn[0]
                success = True
            cur.close()
            conn.close()
            return success
        except Exception as e:
            return False

class Recommendation_letter:
    def __init__(self):
        self.letter_id = 0
        self.admissionid = 0
        self.letter_qty = 0
        self.letter_score = 0
        self.letter_received = 'N'
        self.writer = Recommendation_letter_writer()

    def isValid(self):
        return self.writer.lname != ''

    def build_letter_from_db(self, lettertuple):
        self.letter_id = lettertuple[0]
        self.admissionid = lettertuple[1]
        self.letter_qty = lettertuple[2]
        self.letter_score = lettertuple[3]
        self.writer.fname = lettertuple[4]
        self.writer.mname = lettertuple[5]
        self.writer.lname = lettertuple[6]
        self.writer.title = lettertuple[7]
        self.writer.affiliation = lettertuple[8]
        self.writer.homephone = lettertuple[9]
        self.writer.cellphone = lettertuple[10]
        self.writer.email = lettertuple[11]
        self.writer.street = lettertuple[12]
        self.writer.city = lettertuple[13]
        self.writer.state = lettertuple[14]
        self.writer.country = lettertuple[15]
        self.writer.zip = lettertuple[16]
        self.letter_received = lettertuple[17]


    def buildRecommendLetterFromForm(self, form):
        self.writer.fname = form['c1fname']
        self.writer.mname = form['c1mname']
        self.writer.lname = form['c1lname']
        self.writer.email = form['c1email']
        self.writer.title = form['c1title']
        self.writer.affiliation = form['c1affiliation']

    def buildRecommendLetter2FromForm(self, form):
        self.writer.fname = form['c2fname']
        self.writer.mname = form['c2mname']
        self.writer.lname = form['c2lname']
        self.writer.email = form['c2email']
        self.writer.title = form['c2title']
        self.writer.affiliation = form['c2affiliation']

    def buildRecommendLetter3FromForm(self, form):
        self.writer.fname = form['c3fname']
        self.writer.mname = form['c3mname']
        self.writer.lname = form['c3lname']
        self.writer.email = form['c3email']
        self.writer.title = form['c3title']
        self.writer.affiliation = form['c3affiliation']

    def save(self):
        try:
            conn = psycopg2.connect(**db_config)
            cur = conn.cursor()
            cur.execute("""
                       INSERT INTO starrs."RECOMMENDATION_LETTER"(
                       "ADMISSION_ID", "LETTER_QTY", "LETTER_SCORE", "WRITER_FIRST_NAME", "WRITER_MIDDLE_NAME", 
                       "WRITER_LAST_NAME", "WRITER_TITLE", "WRITER_AFFILIATION", "WRITER_HOME_PHONE", 
                       "WRITER_CELL_PHONE", "WRITER_EMAIL", "WRITER_STREET", "WRITER_CITY", "WRITER_STATE", 
                       "WRITER_COUNTRY", "WRITER_ZIP")
                        VALUES (%s, 1, 0, %s, %s, %s, %s, %s, '', '', %s, '', '', '', '', '');
                        """,
                        [self.admissionid, self.writer.fname, self.writer.mname, self.writer.lname,
                         self.writer.title, self.writer.affiliation, self.writer.email])
            conn.commit()
            cur.close()
            conn.close()
            return True
        except Exception as e:
            return False

    def gs_update(self):
        try:
            conn = psycopg2.connect(**db_config)
            cur = conn.cursor()
            cur.execute("""
                                UPDATE starrs."RECOMMENDATION_LETTER"
                                SET "LETTER_RECEIVED"=%s, "LETTER_SCORE"=%s
                                WHERE "LETTER_ID"=%s;
                               """,
                        [self.letter_received, self.letter_score, self.letter_id])
            conn.commit()
            cur.close()
            conn.close()
            return True
        except Exception as e:
            return False

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

class Applicant_Degree:
    def __init__(self):
        self.applicant_degree_id = 0
        self.undergrad_grad = ''
        self.degree_type = ''
        self.university = ''
        self.gpa = 0
        self.applicant_id = ''
        self.year_issued = ''

    def isValid(self):
        return self.year_issued != '0'

    def build_degree_from_db(self, degreetuple):
        self.applicant_degree_id = degreetuple[0]
        self.undergrad_grad = degreetuple[1]
        self.degree_type = degreetuple[2]
        self.university = degreetuple[3]
        self.gpa = degreetuple[4]
        self.applicant_id = degreetuple[5]
        self.year_issued = degreetuple[6]

    def buildUndergradDegreeFromForm(self, form):
        self.undergrad_grad = 'U'
        self.degree_type = ''
        self.year_issued = form['bachyear']
        self.university = form['bachschool']
        self.gpa = form['bachgpa']
        self.applicant_id = form['userid']

    def buildGradDegreeFromForm(self, form):
        self.undergrad_grad = 'G'
        self.degree_type = ''
        self.year_issued = form['msyear']
        self.university = form['msschool']
        self.gpa = form['msgpa']
        self.applicant_id = form['userid']

    def save(self):
        try:
            conn = psycopg2.connect(**db_config)
            cur = conn.cursor()
            cur.execute("""
                   INSERT INTO starrs."APPLICANT_DEGREE"(
                   "UNDERGRADUATE_GRADUATE", "DEGREE_TYPE", "UNIVERSITY", "GPA", "APPLICANT_ID", "YEAR_ISSUED")
	                VALUES (%s, %s, %s, %s, %s, %s);;
                   """,
                        [self.undergrad_grad, self.degree_type, self.university,
                         self.gpa, self.applicant_id, self.year_issued])
            conn.commit()
            cur.close()
            conn.close()
            return True
        except Exception as e:
            return False
