ALTER TABLE IF EXISTS starrs."ADMISSION_REVIEW"
    ADD COLUMN "ADVISOR" character varying(30);

ALTER TABLE starrs."ADMISSION"
    ALTER COLUMN "COMMITTEE_DECISION" TYPE character varying(20) COLLATE pg_catalog."default";

ALTER TABLE starrs."ADMISSION"
    ALTER COLUMN "ADMISSION_RANKING" TYPE character varying(20) COLLATE pg_catalog."default";

ALTER TABLE starrs."ADMISSION"
    ALTER COLUMN "ADMISSION_COMMENT" TYPE character varying(250) COLLATE pg_catalog."default";

ALTER TABLE starrs."ADMISSION"
    ALTER COLUMN "RECOMMENDED_ADVISOR" TYPE character varying(30) COLLATE pg_catalog."default";

CREATE OR REPLACE VIEW starrs."ADMISSION_REVIEW_V"
 AS
 SELECT ar."REVIEWER_ID",
    usr."FIRST_NAME",
    usr."LAST_NAME",
    ar."ADMISSION_ID",
    ar."ADMISSION_COMMENT",
    ar."ADMISSION_RANKING",
    ar."ADMISSION_DECISION",
    ar."COMMITTEE_ID"
   FROM starrs."ADMISSION_REVIEW" ar,
    starrs."USER" usr
  WHERE ar."REVIEWER_ID"::text = usr."USER_ID"::text;

ALTER TABLE starrs."ADMISSION_REVIEW_V"
    OWNER TO postgres;

CREATE OR REPLACE VIEW starrs."GRAD_SECRETARY_V"
 AS
 SELECT ad."ADMISSION_ID",
    au."USER_ID" AS "APPLICANT_ID",
    au."FIRST_NAME" AS "APPLICANT_FIRST_NAME",
    au."LAST_NAME" AS "APPLICANT_LAST_NAME",
    fu."USER_ID" AS "GS_ID",
    fu."FIRST_NAME" AS "GS_FIRST_NAME",
    fu."LAST_NAME" AS "GS_LAST_NAME",
    ad."ADMISSION_DATE",
    ad."DEGREE_SOUGHT",
    ad."TRANSCRIPT_RECEIVED",
    ad."ADMISSION_STATUS"
   FROM starrs."GRADUATE_SECRETARY" gs,
    starrs."USER" fu,
    starrs."USER" au,
    starrs."ADMISSION" ad,
    starrs."APPLICANT" app
  WHERE gs."GS_ID"::text = fu."USER_ID"::text AND gs."APPLICANT_ID"::text = au."USER_ID"::text AND ad."STUDENT_ID"::text = au."USER_ID"::text AND au."USER_ID"::text = app."USER_ID"::text;

ALTER TABLE starrs."GRAD_SECRETARY_V"
    OWNER TO postgres;
