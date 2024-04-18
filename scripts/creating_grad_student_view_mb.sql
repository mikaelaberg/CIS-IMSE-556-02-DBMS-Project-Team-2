-- View: starrs.GRADUATE_STUDENT_V

-- DROP VIEW starrs."GRADUATE_STUDENT_V";

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