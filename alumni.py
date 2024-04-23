import psycopg2
from dbconfig import db_config

class Alumni:
    def __init__(self):
        self.alumni_id = ''
        self.degree = ''
        self.gpa = ''
        self.gradyear = ''
        self.fname = ''
        self.mname = ''
        self.lname = ''
        self.homephone = ''
        self.cell_phone = ''
        self.workphone = ''
        self.email = ''
        self.street = ''
        self.city = ''
        self.state = ''
        self.country = ''
        self.zip = ''
        self.class_records = []

    def build_from_db(self, db_row):
        self.alumni_id = db_row[0]
        self.degree = db_row[1]
        self.gpa = db_row[2]
        self.gradyear = db_row[3]
        self.fname = db_row[4]
        self.mname = db_row[5]
        self.lname = db_row[6]
        self.homephone = db_row[7]
        self.cell_phone = db_row[8]
        self.workphone = db_row[9]
        self.email = db_row[10]
        self.street = db_row[11]
        self.city = db_row[12]
        self.state = db_row[13]
        self.country = db_row[14]
        self.zip = db_row[15]

    def get_alumni_for_id(self, alumni_id):
        self.alumni_id = alumni_id
        try:
            conn = psycopg2.connect(**db_config)
            cur = conn.cursor()
            cur.execute("""
                        SELECT
                        "USER_ID", "DEGREE", "GPA", "GRADUATION_YEAR", "FIRST_NAME", "MIDDLE_NAME", "LAST_NAME",
                        "HOME_PHONE", "CELL_PHONE", "WORK_PHONE", "EMAIL", "STREET_ADDRESS", "CITY", "STATE",
                        "COUNTRY", "ZIP_CODE" FROM starrs."ALUMNI_V" WHERE "USER_ID" = %s;
                   """,
                        [alumni_id])
            dbalumni = cur.fetchone()
            if dbalumni is not None:
                self.build_from_db(dbalumni)
            cur.close()
            conn.close()
            self.get_class_records()
            return True
        except Exception as e:
            return False

    def get_class_records(self):
        records = []
        try:
            conn = psycopg2.connect(**db_config)
            cur = conn.cursor()
            cur.execute("""
                        SELECT a.*, c."TITLE", c."CREDITS", c."DEPARTMENT"
                        FROM starrs."ATTENDS_SECTION" a
                        INNER JOIN starrs."SECTION" s ON a."SECTION_NO" = s."SECTION_NO"
                        INNER JOIN starrs."COURSE" c ON s."COURSE_NO" = c."COURSE_NO"
                        WHERE a."USER_ID" = %s;
                   """,
                        [self.alumni_id])
            dbrecords = cur.fetchall()
            if dbrecords is not None:
                for record in dbrecords:
                    arecord = Alumni_Record(record)
                    records.append(arecord)
            self.class_records = records
            cur.close()
            conn.close()
            return True
        except Exception as e:
            return None

    def calculatedGPA(self):
        totalscore = 0
        classes_taken = len(self.class_records)
        if classes_taken > 0:
            for record in self.class_records:
                totalscore += float(record.grade)
            return totalscore / classes_taken
        else:
            return 0


class Alumni_Record:
    def __init__(self, db_row):
        self.alumni_id = db_row[0]
        self.course_no = db_row[1]
        self.section_no = db_row[2]
        self.semester = db_row[3]
        self.year = db_row[4]
        self.grade = db_row[5]
        self.rstatus = db_row[6]
        self.title = db_row[7]
        self.credits = db_row[8]
        self.department = db_row[9]

