-- Table: starrs.USER

DROP TABLE starrs."USER" CASCADE;

CREATE TABLE IF NOT EXISTS starrs."USER"
(
    "USER_ID" character varying(10) COLLATE pg_catalog."default" NOT NULL,
    "FIRST_NAME" character varying(30) COLLATE pg_catalog."default",
    "MIDDLE_NAME" character varying(30) COLLATE pg_catalog."default",
    "LAST_NAME" character varying(30) COLLATE pg_catalog."default",
    "SEX" character(1) COLLATE pg_catalog."default",
    "HOME_PHONE" character varying(10) COLLATE pg_catalog."default",
    "CELL_PHONE" character varying(10) COLLATE pg_catalog."default",
    "WORK_PHONE" character varying(10) COLLATE pg_catalog."default",
    "EMAIL" character varying(30) COLLATE pg_catalog."default",
    "STREET_ADDRESS" character varying(30) COLLATE pg_catalog."default",
    "CITY" character varying(20) COLLATE pg_catalog."default",
    "STATE" character(2) COLLATE pg_catalog."default",
    "COUNTRY" character varying(20) COLLATE pg_catalog."default",
    "ZIP_CODE" character varying(10) COLLATE pg_catalog."default",
    CONSTRAINT "USER_pkey" PRIMARY KEY ("USER_ID")
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS starrs."USER"
    OWNER to postgres;

-- Table: starrs.ALUMNI

DROP TABLE IF EXISTS starrs."ALUMNI";

CREATE TABLE IF NOT EXISTS starrs."ALUMNI"
(
    "USER_ID" character varying(10) COLLATE pg_catalog."default" NOT NULL,
    "DEGREE" character varying(10) COLLATE pg_catalog."default",
    "GPA" numeric,
    "GRADUATION_YEAR" numeric,
    CONSTRAINT "ALUMNI_pkey" PRIMARY KEY ("USER_ID"),
    CONSTRAINT "ALUMNI_ID" FOREIGN KEY ("USER_ID")
        REFERENCES starrs."USER" ("USER_ID") MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS starrs."ALUMNI"
    OWNER to postgres;

-- Table: starrs.APPLICANT

DROP TABLE IF EXISTS starrs."APPLICANT";

CREATE TABLE IF NOT EXISTS starrs."APPLICANT"
(
    "USER_ID" character varying(10) COLLATE pg_catalog."default" NOT NULL,
    "GRE_VERBAL" numeric,
    "GRE_ANALYTICAL" numeric,
    "GRE_QUANTITATIVE" numeric,
    "TRANSCRIPT_RECEIVED" character(1) COLLATE pg_catalog."default" NOT NULL DEFAULT 'N'::bpchar,
    "WORK_EXPERIENCE" character varying(250) COLLATE pg_catalog."default",
    CONSTRAINT "APPLICANT_pkey" PRIMARY KEY ("USER_ID"),
    CONSTRAINT "APPLICANT_ID" FOREIGN KEY ("USER_ID")
        REFERENCES starrs."USER" ("USER_ID") MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        --NOT VALID
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS starrs."APPLICANT"
    OWNER to postgres;

-- Table: starrs.FACULTY

DROP TABLE starrs."FACULTY" CASCADE;

CREATE TABLE IF NOT EXISTS starrs."FACULTY"
(
    "USER_ID" character varying(10) COLLATE pg_catalog."default" NOT NULL,
    "DEPARTMENT" character varying(10) COLLATE pg_catalog."default",
    CONSTRAINT "FACULTY_pkey" PRIMARY KEY ("USER_ID"),
    CONSTRAINT "FACULTY_USER_ID_fkey" FOREIGN KEY ("USER_ID")
        REFERENCES starrs."USER" ("USER_ID") MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS starrs."FACULTY"
    OWNER to postgres;

-- Table: starrs.GRADUATE_STUDENT

DROP TABLE IF EXISTS starrs."GRADUATE_STUDENT";

CREATE TABLE IF NOT EXISTS starrs."GRADUATE_STUDENT"
(
    "USER_ID" character varying(10) COLLATE pg_catalog."default" NOT NULL,
    "STATUS" character varying(10) COLLATE pg_catalog."default",
    "DEGREE_PROGRAM" character varying(3) COLLATE pg_catalog."default",
    "ADMITTED_SEMESTER" character varying(6) COLLATE pg_catalog."default",
    CONSTRAINT "GRADUATE_STUDENT_pkey" PRIMARY KEY ("USER_ID"),
    CONSTRAINT "STUDENT_ID" FOREIGN KEY ("USER_ID")
        REFERENCES starrs."USER" ("USER_ID") MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS starrs."GRADUATE_STUDENT"
    OWNER to postgres;

-- Table: starrs.ADMISSION

DROP TABLE starrs."ADMISSION" CASCADE;

CREATE TABLE IF NOT EXISTS starrs."ADMISSION"
(
    "ADMISSION_ID" bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    "STUDENT_ID" character varying(10) COLLATE pg_catalog."default",
    "AREA_OF_INTEREST" character varying(20) COLLATE pg_catalog."default",
    "ADMISSION_STATUS" character varying(20) COLLATE pg_catalog."default",
    "EXPECTED_DATE" date,
    "ADMISSION_DATE" date,
    "COMMITTEE_DECISION" character varying(10) COLLATE pg_catalog."default",
    "ADMISSION_RANKING" character varying(10) COLLATE pg_catalog."default",
    "ADMISSION_COMMENT" character varying(200) COLLATE pg_catalog."default",
    "RECOMMENDED_ADVISOR" character varying(10) COLLATE pg_catalog."default",
    CONSTRAINT "ADMISSION_pkey" PRIMARY KEY ("ADMISSION_ID"),
    CONSTRAINT "ADMISSION_STUDENT_ID_fkey" FOREIGN KEY ("STUDENT_ID")
        REFERENCES starrs."USER" ("USER_ID") MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS starrs."ADMISSION"
    OWNER to postgres;

-- Table: starrs.ADMISSION_REVIEW

DROP TABLE IF EXISTS starrs."ADMISSION_REVIEW";

CREATE TABLE IF NOT EXISTS starrs."ADMISSION_REVIEW"
(
    "REVIEWER_ID" character varying(10) COLLATE pg_catalog."default" NOT NULL,
    "ADMISSION_ID" bigint NOT NULL,
    "ADMISSION_COMMENT" character varying(250) COLLATE pg_catalog."default",
    "ADMISSION_RANKING" character varying(20) COLLATE pg_catalog."default",
    "ADMISSION_DECISION" character varying(20) COLLATE pg_catalog."default",
    "COMMITTEE_ID" bigint,
    CONSTRAINT "ADMISSION_REVIEW_pkey" PRIMARY KEY ("REVIEWER_ID", "ADMISSION_ID"),
    CONSTRAINT "ADMISSION_REVIEW_ADMISSION_ID_fkey" FOREIGN KEY ("ADMISSION_ID")
        REFERENCES starrs."ADMISSION" ("ADMISSION_ID") MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
        -- NOT VALID,
    CONSTRAINT "ADMISSION_REVIEW_REVIEWER_ID_fkey" FOREIGN KEY ("REVIEWER_ID")
        REFERENCES starrs."USER" ("USER_ID") MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        --NOT VALID
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS starrs."ADMISSION_REVIEW"
    OWNER to postgres;

-- Table: starrs.APPLICANT_DEGREE

DROP TABLE IF EXISTS starrs."APPLICANT_DEGREE";

CREATE TABLE IF NOT EXISTS starrs."APPLICANT_DEGREE"
(
    "APPLICANT_DEGREE_ID" smallint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9999 CACHE 1 ),
    "UNDERGRADUATE_GRADUATE" character(1) COLLATE pg_catalog."default" NOT NULL DEFAULT 'U'::bpchar,
    "DEGREE_TYPE" character varying(3) COLLATE pg_catalog."default",
    "UNIVERSITY" character varying(20) COLLATE pg_catalog."default",
    "GPA" numeric,
    "APPLICANT_ID" character varying(10) COLLATE pg_catalog."default",
    CONSTRAINT "APPLICANT_DEGREE_pkey" PRIMARY KEY ("APPLICANT_DEGREE_ID"),
    CONSTRAINT "APPLICANT_DEGREE_FK" FOREIGN KEY ("APPLICANT_ID")
        REFERENCES starrs."USER" ("USER_ID") MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS starrs."APPLICANT_DEGREE"
    OWNER to postgres;

-- Table: starrs.COURSE
DROP TABLE starrs."COURSE" CASCADE;

CREATE TABLE IF NOT EXISTS starrs."COURSE"
(
    "COURSE_NO" bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    "TITLE" character varying(30) COLLATE pg_catalog."default",
    "CREDITS" numeric,
    CONSTRAINT "COURSE_pkey" PRIMARY KEY ("COURSE_NO")
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS starrs."COURSE"
    OWNER to postgres;

-- Table: starrs.SECTION

DROP TABLE IF EXISTS starrs."SECTION";

CREATE TABLE IF NOT EXISTS starrs."SECTION"
(
    "SECTION_NO" integer NOT NULL,
    "COURSE_NO" bigint NOT NULL,
    "SEMESTER" character(2) COLLATE pg_catalog."default" NOT NULL,
    "YEAR" integer NOT NULL,
    "INSTRUCTOR_ID" character varying(10) COLLATE pg_catalog."default",
    CONSTRAINT "SECTION_pkey" PRIMARY KEY ("SECTION_NO", "COURSE_NO", "SEMESTER", "YEAR"),
    CONSTRAINT "COURSE_SECTION_FK" FOREIGN KEY ("COURSE_NO")
        REFERENCES starrs."COURSE" ("COURSE_NO") MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT "INSTRUCTOR_ID_FK" FOREIGN KEY ("INSTRUCTOR_ID")
        REFERENCES starrs."FACULTY" ("USER_ID") MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS starrs."SECTION"
    OWNER to postgres;

-- Table: starrs.ATTENDS_SECTION

DROP TABLE IF EXISTS starrs."ATTENDS_SECTION";

CREATE TABLE IF NOT EXISTS starrs."ATTENDS_SECTION"
(
    "STUDENT_ID" character varying(10) COLLATE pg_catalog."default" NOT NULL,
    "COURSE_NO" bigint NOT NULL,
    "SECTION_NO" integer NOT NULL,
    "SEMESTER" character(2) COLLATE pg_catalog."default" NOT NULL,
    "YEAR" integer NOT NULL,
    CONSTRAINT "ATTENDS_SECTION_pkey" PRIMARY KEY ("STUDENT_ID", "COURSE_NO", "SECTION_NO", "SEMESTER", "YEAR"),
    CONSTRAINT "ATTENDS_SECTION_COURSE_NO_fkey" FOREIGN KEY ("COURSE_NO")
        REFERENCES starrs."COURSE" ("COURSE_NO") MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT "ATTENDS_SECTION_STUDENT_ID_fkey" FOREIGN KEY ("STUDENT_ID")
        REFERENCES starrs."USER" ("USER_ID") MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS starrs."ATTENDS_SECTION"
    OWNER to postgres;

-- Table: starrs.RECOMMENDATION_LETTER

DROP TABLE IF EXISTS starrs."RECOMMENDATION_LETTER";

CREATE TABLE IF NOT EXISTS starrs."RECOMMENDATION_LETTER"
(
    "LETTER_ID" bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    "ADMISSION_ID" bigint,
    "LETTER_QTY" integer,
    "LETTER_SCORE" numeric,
    "WRITER_FIRST_NAME" character varying(20) COLLATE pg_catalog."default",
    "WRITER_MIDDLE_NAME" character varying(20) COLLATE pg_catalog."default",
    "WRITER_LAST_NAME" character varying(20) COLLATE pg_catalog."default",
    "WRITER_TITLE" character varying(20) COLLATE pg_catalog."default",
    "WRITER_AFFILIATION" character varying(20) COLLATE pg_catalog."default",
    "WRITER_HOME_PHONE" character varying(20) COLLATE pg_catalog."default",
    "WRITER_CELL_PHONE" character varying(20) COLLATE pg_catalog."default",
    "WRITER_EMAIL" character varying(30)[] COLLATE pg_catalog."default",
    "WRITER_STREET" character varying(30) COLLATE pg_catalog."default",
    "WRITER_CITY" character varying(20) COLLATE pg_catalog."default",
    "WRITER_STATE" character(2) COLLATE pg_catalog."default",
    "WRITER_COUNTRY" character varying(10) COLLATE pg_catalog."default",
    "WRITER_ZIP" character varying(10) COLLATE pg_catalog."default",
    CONSTRAINT "RECOMMENDATION_LETTER_pkey" PRIMARY KEY ("LETTER_ID"),
    CONSTRAINT "RECOMMENDATION_LETTER_ADMISSION_ID_fkey" FOREIGN KEY ("ADMISSION_ID")
        REFERENCES starrs."ADMISSION" ("ADMISSION_ID") MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        -- NOT VALID
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS starrs."RECOMMENDATION_LETTER"
    OWNER to postgres;

-- Table: starrs.GRAD_APPLICATION
DROP TABLE starrs."GRAD_APPLICATION" CASCADE;

CREATE TABLE IF NOT EXISTS starrs."GRAD_APPLICATION"
(
    "APPLICATION_ID" bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    "STUDENT_ID" character varying(10) COLLATE pg_catalog."default",
    "STATUS" character varying(10) COLLATE pg_catalog."default",
    "DECISION_DATE" date,
    "DECISION" character varying(10) COLLATE pg_catalog."default",
    CONSTRAINT "GRAD_APPLICATION_pkey" PRIMARY KEY ("APPLICATION_ID"),
    CONSTRAINT "GRAD_APPLICATION_STUDENT_ID_fkey" FOREIGN KEY ("STUDENT_ID")
        REFERENCES starrs."USER" ("USER_ID") MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS starrs."GRAD_APPLICATION"
    OWNER to postgres;

-- Table: starrs.GRADUATION_REVIEW

DROP TABLE IF EXISTS starrs."GRADUATION_REVIEW";

CREATE TABLE IF NOT EXISTS starrs."GRADUATION_REVIEW"
(
    "REVIEWER_ID" character varying(10) COLLATE pg_catalog."default" NOT NULL,
    "APPLICATION_ID" bigint NOT NULL,
    CONSTRAINT "GRADUATION_REVIEW_pkey" PRIMARY KEY ("REVIEWER_ID", "APPLICATION_ID"),
    CONSTRAINT "GRADUATION_REVIEW_APPLICATION_ID_fkey" FOREIGN KEY ("APPLICATION_ID")
        REFERENCES starrs."GRAD_APPLICATION" ("APPLICATION_ID") MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT "GRADUATION_REVIEW_REVIEWER_ID_fkey" FOREIGN KEY ("REVIEWER_ID")
        REFERENCES starrs."USER" ("USER_ID") MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS starrs."GRADUATION_REVIEW"
    OWNER to postgres;

-- View: starrs.ALUMNI_V

-- DROP VIEW starrs."ALUMNI_V";

CREATE OR REPLACE VIEW starrs."ALUMNI_V"
 AS
 SELECT alu."USER_ID",
    alu."DEGREE",
    alu."GPA",
    alu."GRADUATION_YEAR",
    usr."FIRST_NAME",
    usr."MIDDLE_NAME",
    usr."LAST_NAME",
    usr."SEX",
    usr."HOME_PHONE",
    usr."CELL_PHONE",
    usr."WORK_PHONE",
    usr."EMAIL",
    usr."STREET_ADDRESS",
    usr."CITY",
    usr."STATE",
    usr."COUNTRY",
    usr."ZIP_CODE"
   FROM starrs."ALUMNI" alu,
    starrs."USER" usr
  WHERE alu."USER_ID"::text = usr."USER_ID"::text;

ALTER TABLE starrs."ALUMNI_V"
    OWNER TO postgres;

-- View: starrs.APPLICANT_V

-- DROP VIEW starrs."APPLICANT_V";

CREATE OR REPLACE VIEW starrs."APPLICANT_V"
 AS
 SELECT app."USER_ID",
    app."GRE_VERBAL",
    app."GRE_ANALYTICAL",
    app."GRE_QUANTITATIVE",
    app."TRANSCRIPT_RECEIVED",
    app."WORK_EXPERIENCE",
    usr."FIRST_NAME",
    usr."MIDDLE_NAME",
    usr."LAST_NAME",
    usr."SEX",
    usr."HOME_PHONE",
    usr."CELL_PHONE",
    usr."WORK_PHONE",
    usr."EMAIL",
    usr."STREET_ADDRESS",
    usr."CITY",
    usr."STATE",
    usr."COUNTRY",
    usr."ZIP_CODE"
   FROM starrs."APPLICANT" app,
    starrs."USER" usr
  WHERE app."USER_ID"::text = usr."USER_ID"::text;

ALTER TABLE starrs."APPLICANT_V"
    OWNER TO postgres;

-- View: starrs.FACULTY_V

-- DROP VIEW starrs."FACULTY_V";

CREATE OR REPLACE VIEW starrs."FACULTY_V"
 AS
 SELECT fac."USER_ID",
    fac."DEPARTMENT",
    usr."FIRST_NAME",
    usr."MIDDLE_NAME",
    usr."LAST_NAME",
    usr."SEX",
    usr."HOME_PHONE",
    usr."CELL_PHONE",
    usr."WORK_PHONE",
    usr."EMAIL",
    usr."STREET_ADDRESS",
    usr."CITY",
    usr."STATE",
    usr."COUNTRY",
    usr."ZIP_CODE"
   FROM starrs."FACULTY" fac,
    starrs."USER" usr
  WHERE fac."USER_ID"::text = usr."USER_ID"::text;

ALTER TABLE starrs."FACULTY_V"
    OWNER TO postgres;

-- View: starrs.GRADUATE_STUDENT_V

-- DROP VIEW starrs."GRADUATE_STUDENT_V";

CREATE OR REPLACE VIEW starrs."GRADUATE_STUDENT_V"
 AS
 SELECT gst."USER_ID",
    gst."STATUS",
    gst."DEGREE_PROGRAM",
    gst."ADMITTED_SEMESTER",
    usr."FIRST_NAME",
    usr."MIDDLE_NAME",
    usr."LAST_NAME",
    usr."SEX",
    usr."HOME_PHONE",
    usr."CELL_PHONE",
    usr."WORK_PHONE",
    usr."EMAIL",
    usr."STREET_ADDRESS",
    usr."CITY",
    usr."STATE",
    usr."COUNTRY",
    usr."ZIP_CODE"
   FROM starrs."GRADUATE_STUDENT" gst,
    starrs."USER" usr
  WHERE gst."USER_ID"::text = usr."USER_ID"::text;

ALTER TABLE starrs."GRADUATE_STUDENT_V"
    OWNER TO postgres;

