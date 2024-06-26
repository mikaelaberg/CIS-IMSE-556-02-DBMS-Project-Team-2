ALTER TABLE starrs."ADMISSION"
    ALTER COLUMN "AREA_OF_INTEREST" TYPE character varying(250) COLLATE pg_catalog."default";

ALTER TABLE IF EXISTS starrs."ADMISSION"
    ADD COLUMN "GRE_TOTAL" numeric;

ALTER TABLE IF EXISTS starrs."ADMISSION"
    ADD COLUMN "GRE_VERBAL" numeric;

ALTER TABLE IF EXISTS starrs."ADMISSION"
    ADD COLUMN "GRE_ANALYTICAL" numeric;

ALTER TABLE IF EXISTS starrs."ADMISSION"
    ADD COLUMN "GRE_QUANTITATIVE" numeric;

ALTER TABLE IF EXISTS starrs."ADMISSION"
    ADD COLUMN "TRANSCRIPT_RECEIVED" character(1);

ALTER TABLE IF EXISTS starrs."ADMISSION"
    ADD COLUMN "WORK_EXPERIENCE" character varying(250);
	
ALTER TABLE IF EXISTS starrs."APPLICANT"
    ADD COLUMN "ADMISSION_ID" bigint;
	
CREATE TABLE starrs."GRADUATE_SECRETARY"
(
    "ADMISSION_ID" bigint,
    "APPLICANT_ID" character varying,
    "GS_ID" character varying,
    PRIMARY KEY ("ADMISSION_ID"),
    FOREIGN KEY ("ADMISSION_ID")
        REFERENCES starrs."ADMISSION" ("ADMISSION_ID") MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID,
    FOREIGN KEY ("APPLICANT_ID")
        REFERENCES starrs."USER" ("USER_ID") MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID,
    FOREIGN KEY ("GS_ID")
        REFERENCES starrs."FACULTY" ("USER_ID") MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
);

ALTER TABLE IF EXISTS starrs."GRADUATE_SECRETARY"
    OWNER to postgres;
	
ALTER TABLE IF EXISTS starrs."APPLICANT_DEGREE"
    ADD COLUMN "YEAR_ISSUED" integer;
	
ALTER TABLE IF EXISTS starrs."ADMISSION"
    ADD COLUMN "DEGREE_SOUGHT" character varying(3);
	
ALTER TABLE starrs."ADMISSION"
    ALTER COLUMN "EXPECTED_DATE" TYPE character(6) COLLATE pg_catalog."default";
	
ALTER TABLE starrs."RECOMMENDATION_LETTER"
    ALTER COLUMN "WRITER_EMAIL" TYPE character varying(30) COLLATE pg_catalog."default";
		
ALTER TABLE IF EXISTS starrs."RECOMMENDATION_LETTER"
    ADD COLUMN "LETTER_RECEIVED" character(1) DEFAULT 'N';
	

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
    starrs."ADMISSION" ad
  WHERE gs."GS_ID"::text = fu."USER_ID"::text AND gs."APPLICANT_ID"::text = au."USER_ID"::text AND ad."STUDENT_ID"::text = au."USER_ID"::text;

ALTER TABLE starrs."GRAD_SECRETARY_V"
    OWNER TO postgres;
	
CREATE OR REPLACE VIEW starrs."ADMISSION_STATUS_V"
 AS
 SELECT ad."ADMISSION_ID",
    ad."STUDENT_ID",
    ad."ADMISSION_STATUS",
    ad."TRANSCRIPT_RECEIVED",
    count(ml."LETTER_ID") AS "LETTERS_PENDING"
   FROM starrs."ADMISSION" ad
     LEFT JOIN ( SELECT "RECOMMENDATION_LETTER"."LETTER_ID",
            "RECOMMENDATION_LETTER"."ADMISSION_ID"
           FROM starrs."RECOMMENDATION_LETTER"
          WHERE "RECOMMENDATION_LETTER"."LETTER_RECEIVED" = 'N'::bpchar) ml ON ad."ADMISSION_ID" = ml."ADMISSION_ID"
  GROUP BY ad."ADMISSION_ID", ad."STUDENT_ID", ad."ADMISSION_STATUS", ad."TRANSCRIPT_RECEIVED";

ALTER TABLE starrs."ADMISSION_STATUS_V"
    OWNER TO postgres;
