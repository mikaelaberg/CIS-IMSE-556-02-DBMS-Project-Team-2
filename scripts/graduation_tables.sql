DROP VIEW starrs."GRADUATE_STUDENT_V";
DROP VIEW starrs."USER_V";
DROP VIEW starrs."USER_ROLES_V";
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

GRANT ALL ON TABLE starrs."GRADUATE_STUDENT" TO PUBLIC;

GRANT ALL ON TABLE starrs."GRADUATE_STUDENT" TO postgres;


CREATE OR REPLACE VIEW starrs."GRADUATE_STUDENT_V"
 AS
 SELECT gst."USER_ID",
    gst."STATUS",
    gst."DEGREE_PROGRAM",
    gst."ADMITTED_SEMESTER",
    round(avg(atn."GRADE"), 1) AS gpa,
    sum(c."CREDITS") AS total_credit_hrs,
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
   FROM starrs."GRADUATE_STUDENT" gst
     JOIN starrs."USER" usr ON gst."USER_ID"::text = usr."USER_ID"::text
     JOIN starrs."ATTENDS_SECTION" atn ON gst."USER_ID"::text = atn."USER_ID"::text
     JOIN starrs."COURSE" c ON atn."COURSE_NO" = c."COURSE_NO"
  GROUP BY gst."USER_ID", gst."STATUS", gst."DEGREE_PROGRAM", gst."ADMITTED_SEMESTER", usr."FIRST_NAME", usr."MIDDLE_NAME", usr."LAST_NAME", usr."SEX", usr."HOME_PHONE", usr."CELL_PHONE", usr."WORK_PHONE", usr."EMAIL", usr."STREET_ADDRESS", usr."CITY", usr."STATE", usr."COUNTRY", usr."ZIP_CODE";

ALTER TABLE starrs."GRADUATE_STUDENT_V"
    OWNER TO postgres;


CREATE OR REPLACE VIEW starrs."USER_ROLES_V"
 AS
 SELECT u."USER_ID",
    'Applicant'::text AS "USER_ROLE"
   FROM starrs."USER" u,
    starrs."APPLICANT" app
  WHERE u."USER_ID"::text = app."USER_ID"::text
UNION
 SELECT u."USER_ID",
    'Grad_Student'::text AS "USER_ROLE"
   FROM starrs."USER" u,
    starrs."GRADUATE_STUDENT" gs
  WHERE u."USER_ID"::text = gs."USER_ID"::text
UNION
 SELECT u."USER_ID",
    'Alumni'::text AS "USER_ROLE"
   FROM starrs."USER" u,
    starrs."ALUMNI" al
  WHERE u."USER_ID"::text = al."USER_ID"::text
UNION
 SELECT u."USER_ID",
    'Faculty'::text AS "USER_ROLE"
   FROM starrs."USER" u,
    starrs."FACULTY" fac
  WHERE u."USER_ID"::text = fac."USER_ID"::text;

ALTER TABLE starrs."USER_ROLES_V"
    OWNER TO postgres;

-- View: starrs.USER_V

CREATE OR REPLACE VIEW starrs."USER_V"
 AS
 SELECT usr."USER_ID",
    urv."USER_ROLE",
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
   FROM starrs."USER_ROLES_V" urv,
    starrs."USER" usr
  WHERE urv."USER_ID"::text = usr."USER_ID"::text;

ALTER TABLE starrs."USER_V"
    OWNER TO postgres;
