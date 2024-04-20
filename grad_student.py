import psycopg2
from dbconfig import db_config

class Grad_Student:
    def __init__(self):
        self.student_id = ''
        self.status = ''
        self.degree_program = ''
        self.admitted_semester = ''

    def enroll(self):
        try:
            conn = psycopg2.connect(**db_config)
            cur = conn.cursor()
            cur.execute("""
                                INSERT INTO starrs."GRADUATE_STUDENT"(
                                "USER_ID", "STATUS", "DEGREE_PROGRAM", "ADMITTED_SEMESTER")
                                VALUES (%s, %s, %s, %s);""",
                        [self.student_id, self.status, self.degree_program, self.admitted_semester])

            cur.execute("""
                                DELETE FROM starrs."APPLICANT" WHERE "USER_ID" = %s;         
                            """,
                        [self.student_id])

            conn.commit()
            cur.close()
            conn.close()
            return True
        except Exception as e:
            conn.rollback()
            cur.close()
            conn.close()
            return False