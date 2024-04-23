import psycopg2
from dbconfig import db_config

class Admission_Review:
    def __init__(self, db_row):
        self.reviewer_id = db_row[0]
        self.reviewer_fname = db_row[1]
        self.reviewer_lname = db_row[2]
        self.admission_id = db_row[3]
        self.admission_comment = db_row[4]
        self.admission_ranking = db_row[5]
        self.admission_decision = db_row[6]
        self.committee_id = db_row[7]

    def get_ranking_string(self):
        rank = int(self.admission_ranking)
        if rank == 2:
            return 'Borderline'
        if rank == 3:
            return 'Admit without Aid'
        if rank == 4:
            return 'Admit with Aid'
        return 'Reject'

def get_review_for_admission(admissionid):
    try:
        conn = psycopg2.connect(**db_config)
        cur = conn.cursor()
        cur.execute("""
                            SELECT "REVIEWER_ID", "FIRST_NAME", "LAST_NAME", 
                            "ADMISSION_ID", "ADMISSION_COMMENT", "ADMISSION_RANKING", 
                            "ADMISSION_DECISION", "COMMITTEE_ID"
                            FROM starrs."ADMISSION_REVIEW_V"
                            WHERE "ADMISSION_ID" = %s;
               """,
                    [admissionid])
        dbreview = cur.fetchone()
        review = None
        if dbreview is not None:
            review = Admission_Review(dbreview)
        cur.close()
        conn.close()
        return review
    except Exception as e:
        return None
