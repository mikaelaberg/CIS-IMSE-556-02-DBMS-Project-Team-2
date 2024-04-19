-- Table: starrs.GRADUATE_STUDENT

-- DROP TABLE IF EXISTS starrs."GRADUATE_STUDENT";

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