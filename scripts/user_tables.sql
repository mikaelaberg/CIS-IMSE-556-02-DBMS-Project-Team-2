-- Table: starss.USER

-- DROP TABLE IF EXISTS starss."USER";

CREATE TABLE IF NOT EXISTS starss."USER"
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

ALTER TABLE IF EXISTS starss."USER"
    OWNER to postgres;
	

-- Table: starss.GRADUATE_STUDENT

-- DROP TABLE IF EXISTS starss."GRADUATE_STUDENT";

CREATE TABLE IF NOT EXISTS starss."GRADUATE_STUDENT"
(
    "USER_ID" character varying(10) COLLATE pg_catalog."default" NOT NULL,
    "STATUS" character varying(10) COLLATE pg_catalog."default",
    "DEGREE_PROGRAM" character varying(3) COLLATE pg_catalog."default",
    "ADMITTED_SEMESTER" character varying(6) COLLATE pg_catalog."default",
    CONSTRAINT "GRADUATE_STUDENT_pkey" PRIMARY KEY ("USER_ID"),
    CONSTRAINT "STUDENT_ID" FOREIGN KEY ("USER_ID")
        REFERENCES starss."USER" ("USER_ID") MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS starss."GRADUATE_STUDENT"
    OWNER to postgres;
	
	
-- Table: starss.FACULTY

-- DROP TABLE IF EXISTS starss."FACULTY";

CREATE TABLE IF NOT EXISTS starss."FACULTY"
(
    "USER_ID" character varying(10) COLLATE pg_catalog."default" NOT NULL,
    "DEPARTMENT" character varying(10) COLLATE pg_catalog."default",
    CONSTRAINT "FACULTY_pkey" PRIMARY KEY ("USER_ID"),
    CONSTRAINT "FACULTY_USER_ID_fkey" FOREIGN KEY ("USER_ID")
        REFERENCES starss."USER" ("USER_ID") MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS starss."FACULTY"
    OWNER to postgres;
	
	
-- Table: starss.APPLICANT

-- DROP TABLE IF EXISTS starss."APPLICANT";

CREATE TABLE IF NOT EXISTS starss."APPLICANT"
(
    "USER_ID" character varying(10) COLLATE pg_catalog."default" NOT NULL,
    "GRE_VERBAL" numeric,
    "GRE_ANALYTICAL" numeric,
    "GRE_QUANTITATIVE" numeric,
    "TRANSCRIPT_RECIEVED" character(1) COLLATE pg_catalog."default" NOT NULL DEFAULT 'N'::bpchar,
    "WORK_EXPERIENCE" character varying(250) COLLATE pg_catalog."default",
    CONSTRAINT "APPLICANT_pkey" PRIMARY KEY ("USER_ID"),
    CONSTRAINT "APPLICANT_ID" FOREIGN KEY ("USER_ID")
        REFERENCES starss."USER" ("USER_ID") MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS starss."APPLICANT"
    OWNER to postgres;
	
	
-- Table: starss.ALUMNI

-- DROP TABLE IF EXISTS starss."ALUMNI";

CREATE TABLE IF NOT EXISTS starss."ALUMNI"
(
    "USER_ID" character varying(10) COLLATE pg_catalog."default" NOT NULL,
    "DEGREE" character varying(10) COLLATE pg_catalog."default",
    "GPA" numeric,
    "GRADUATION_YEAR" numeric,
    CONSTRAINT "ALUMNI_pkey" PRIMARY KEY ("USER_ID"),
    CONSTRAINT "ALUMNI_ID" FOREIGN KEY ("USER_ID")
        REFERENCES starss."USER" ("USER_ID") MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS starss."ALUMNI"
    OWNER to postgres;
	
	
-- Table: starss.APPLICANT_DEGREE

-- DROP TABLE IF EXISTS starss."APPLICANT_DEGREE";

CREATE TABLE IF NOT EXISTS starss."APPLICANT_DEGREE"
(
    "APPLICANT_DEGREE_ID" smallint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9999 CACHE 1 ),
    "UNDERGRADUATE_GRADUATE" character(1) COLLATE pg_catalog."default" NOT NULL DEFAULT 'U'::bpchar,
    "DEGREE_TYPE" character varying(3) COLLATE pg_catalog."default",
    "UNIVERSITY" character varying(20) COLLATE pg_catalog."default",
    "GPA" numeric,
    "APPLICANT_ID" character varying(10) COLLATE pg_catalog."default",
    CONSTRAINT "APPLICANT_DEGREE_pkey" PRIMARY KEY ("APPLICANT_DEGREE_ID"),
    CONSTRAINT "APPLICANT_DEGREE_FK" FOREIGN KEY ("APPLICANT_ID")
        REFERENCES starss."USER" ("USER_ID") MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS starss."APPLICANT_DEGREE"
    OWNER to postgres;
	
-- View: starss.ALUMNI_V

-- DROP VIEW starss."ALUMNI_V";

CREATE OR REPLACE VIEW starss."ALUMNI_V"
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
   FROM starss."ALUMNI" alu,
    starss."USER" usr
  WHERE alu."USER_ID"::text = usr."USER_ID"::text;

ALTER TABLE starss."ALUMNI_V"
    OWNER TO postgres;

