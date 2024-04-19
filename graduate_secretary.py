import psycopg2

import applicant_info
from dbconfig import db_config

class GraduateSecretary:
    def __init__(self):
        self.faculty_id = ''
        self.gs_records = []
        self.isGS = False

    def check_for_gs_records(self):
        self.isGS = self.get_gs_records()
        return self.isGS

    def get_gs_records(self):
        try:
            conn = psycopg2.connect(**db_config)
            cur = conn.cursor()
            cur.execute("""
                   SELECT * FROM starrs."GRAD_SECRETARY_V" WHERE "GS_ID" = %s;
                   """,
                        [self.faculty_id])
            gs_records = cur.fetchall()
            if gs_records is not None:
                success = self.build_gs_record_array(gs_records)
            else:
                success = False
            cur.close()
            conn.close()
            return success
        except Exception as e:
            return False

    def build_gs_record_array(self, dbarray):
        if len(dbarray) == 0:
            return False
        self.gs_records = []
        for db_record in dbarray:
            gs_record = Graduate_Secretary_Record(db_record)
            self.gs_records.append(gs_record)
        return True

class Graduate_Secretary_Record:
    def __init__(self, gsr_tuple):
        self.admission_id = gsr_tuple[0]
        self.applicant_id = gsr_tuple[1]
        self.applicant_fname = gsr_tuple[2]
        self.applicant_lname = gsr_tuple[3]
        self.gs_id = gsr_tuple[4]
        self.gs_fname = gsr_tuple[5]
        self.gs_lname = gsr_tuple[6]
        self.app_date = gsr_tuple[7]
        self.degree = gsr_tuple[8]
        self.transcript_received = gsr_tuple[9]
        self.admission_status = gsr_tuple[10]

def process_gs_update(form):
    admissionid = form.get('admissionidinput')
    applicationstatus = form.get('applicationstatus')
    transcript = 'N'
    if form.get('transcriptreceived') is not None:
        transcript = 'Y'
    app_to_update = applicant_info.Application()
    app_to_update.admissionid = admissionid
    app_to_update.admission_status = applicationstatus
    app_to_update.transcript_received = transcript

    lettercount = int(form.get('lettercount'))
    for i in range(1, lettercount+1):
        iletter = applicant_info.Recommendation_letter()

        letteridlabel = 'letterid' + str(i)
        letterid = form.get(letteridlabel)

        letterreceivedlabel = 'letterreceived' + str(i)
        letterreceived = form.get(letterreceivedlabel)

        letterstatuslabel = 'letterstatus' + str(i)
        letterstatus = 0
        if form.get(letterstatuslabel) is not None:
            letterstatus = form.get(letterstatuslabel)

        iletter.letter_id = letterid
        iletter.letter_received = letterreceived
        iletter.letter_score = letterstatus

        app_to_update.letters.append(iletter)

    app_to_update.gs_update()


