ALTER TABLE starrs."COURSE"
    ALTER COLUMN "COURSE_NO" TYPE integer;
ALTER TABLE IF EXISTS starrs."COURSE"
    ALTER COLUMN "COURSE_NO" DROP IDENTITY;

ALTER TABLE IF EXISTS starrs."COURSE"
    ADD COLUMN "DEPARTMENT" character varying(10);
