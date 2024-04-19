-- Table: starrs.GRADUATION_REVIEW

-- DROP TABLE IF EXISTS starrs."GRADUATION_REVIEW";

CREATE TABLE IF NOT EXISTS starrs."GRADUATION_REVIEW"
(
    "REVIEWER_ID" character varying(10) COLLATE pg_catalog."default" NOT NULL,
    "APPLICATION_ID" bigint NOT NULL,
    "DECISION" character varying(25) COLLATE pg_catalog."default",
    "DECISION_DATE" date,
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