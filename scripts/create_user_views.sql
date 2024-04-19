
-- View: starrs.USER_ROLES_V

-- DROP VIEW starrs."USER_ROLES_V";

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

-- DROP VIEW starrs."USER_V";

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

-- View: starrs.USER_ROLES_V

-- DROP VIEW starrs."USER_ROLES_V";

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

-- DROP VIEW starrs."USER_V";

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


