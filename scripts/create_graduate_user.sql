BEGIN;

--STEP 1: ADD TO USER TABLE FIRST
INSERT INTO starrs."USER"("USER_ID", "FIRST_NAME", "MIDDLE_NAME", "LAST_NAME", "SEX", "HOME_PHONE", "CELL_PHONE", "WORK_PHONE", "EMAIL", "STREET_ADDRESS", "CITY", "STATE", "COUNTRY", "ZIP_CODE")
VALUES (
        '432432', 'Liam', 'A', 'Test', 'M', '1234567890', '1112223333', '9998887777', 'latest@testing.com', '101 Testing Street', 'Testville', 'MI', 'US', '11111'
       );

--STEP 2: ADD TO GRADUATE_STUDENT
INSERT INTO starrs."GRADUATE_STUDENT"("USER_ID", "STATUS", "DEGREE_PROGRAM", "ADMITTED_SEMESTER")
VALUES(
       '432432', NULL, 'MS', 'FS2023'
      );

--STEP 3: ADD TO ATTENDS SECTION
INSERT INTO starrs."ATTENDS_SECTION"("USER_ID", "COURSE_NO", "SECTION_NO", "SEMESTER", "YEAR", "GRADE", "REGISTRATION STATUS")
VALUES
    ('432432', '511', '1', 'Fa', '2023', '4', 'Registered'),
    ('432432', '521', '1', 'Wi', '2023', '3', 'Registered'),
    ('432432', '513', '1', 'Fa', '2023', '4', 'Registered'),
    ('432432', '5212', '1', 'Wi', '2023', '4', 'Registered'),
    ('432432', '515', '1', 'Fa', '2023', '4', 'Registered'),
    ('432432', '514', '1', 'Wi', '2023', '4', 'Registered'),
    ('432432', '5213', '1', 'Wi', '2023', '3', 'Registered'),
    ('432432', '510', '1', 'Fa', '2023', '4', 'Registered'),
    ('432432', '512', '1', 'Wi', '2023', '4', 'Registered'),
    ('432432', '522', '1', 'Wi', '2023', '4', 'Registered');

--STEP 4: ADD TO GRAD APPLICATION
INSERT INTO starrs."GRAD_APPLICATION"("USER_ID", "STATUS", "DECISION_DATE", "DECISION")
VALUES (
        '432432', NULL, NULL, NULL
       );


COMMIT;
