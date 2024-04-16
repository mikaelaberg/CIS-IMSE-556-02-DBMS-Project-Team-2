INSERT INTO starrs."USER"(
	"USER_ID", "FIRST_NAME", "MIDDLE_NAME", "LAST_NAME", "SEX", "HOME_PHONE", "CELL_PHONE", "WORK_PHONE", "EMAIL", "STREET_ADDRESS", "CITY", "STATE", "COUNTRY", "ZIP_CODE")
	VALUES ('100000', 'Jane', 'T', 'Test01', 'F', '1115551111', '1115551112', '1115551113', 'Test@Testing.com', '999 Testing Street', 'Testville', 'MI', 'US', '11111');
INSERT INTO starrs."APPLICANT"(
	"USER_ID", "GRE_VERBAL", "GRE_ANALYTICAL", "GRE_QUANTITATIVE", "TRANSCRIPT_RECEIVED", "WORK_EXPERIENCE")
	VALUES ('100000', 170, .5, 130, 'N', 'I used to test stuff');
	
INSERT INTO starrs."USER"(
	"USER_ID", "FIRST_NAME", "MIDDLE_NAME", "LAST_NAME", "SEX", "HOME_PHONE", "CELL_PHONE", "WORK_PHONE", "EMAIL", "STREET_ADDRESS", "CITY", "STATE", "COUNTRY", "ZIP_CODE")
	VALUES ('111111', 'John', 'T', 'Test02', 'M', '1115551111', '1115551112', '1115551113', 'JohnT@Testing.com', '400 Testing Street', 'Testville', 'MI', 'US', '11111');
	INSERT INTO starrs."APPLICANT"(
	"USER_ID", "GRE_VERBAL", "GRE_ANALYTICAL", "GRE_QUANTITATIVE", "TRANSCRIPT_RECEIVED", "WORK_EXPERIENCE")
	VALUES ('111111', 130, 2, 160, 'N', 'I used to test stuff');
	
INSERT INTO starrs."USER"(
	"USER_ID", "FIRST_NAME", "MIDDLE_NAME", "LAST_NAME", "SEX", "HOME_PHONE", "CELL_PHONE", "WORK_PHONE", "EMAIL", "STREET_ADDRESS", "CITY", "STATE", "COUNTRY", "ZIP_CODE")
	VALUES ('200000', 'Jessica', 'T', 'Test03', 'F', '1115551111', '1115551112', '1115551113', 'JessT@Testing.com', '404 Testing Street', 'Testville', 'MI', 'US', '11111');
	INSERT INTO starrs."APPLICANT"(
	"USER_ID", "GRE_VERBAL", "GRE_ANALYTICAL", "GRE_QUANTITATIVE", "TRANSCRIPT_RECEIVED", "WORK_EXPERIENCE")
	VALUES ('200000', 140, 3, 150, 'N', 'I used to test stuff');
	
INSERT INTO starrs."USER"(
	"USER_ID", "FIRST_NAME", "MIDDLE_NAME", "LAST_NAME", "SEX", "HOME_PHONE", "CELL_PHONE", "WORK_PHONE", "EMAIL", "STREET_ADDRESS", "CITY", "STATE", "COUNTRY", "ZIP_CODE")
	VALUES ('222222', 'Timothy', 'T', 'Test04', 'M', '1115551111', '1115551112', '1115551113', 'TimT@Testing.com', '500 Testing Street', 'Testville', 'MI', 'US', '11111');
INSERT INTO starrs."APPLICANT"(
	"USER_ID", "GRE_VERBAL", "GRE_ANALYTICAL", "GRE_QUANTITATIVE", "TRANSCRIPT_RECEIVED", "WORK_EXPERIENCE")
	VALUES ('222222', 150, .5, 130, 'N', 'I used to test stuff');
	
INSERT INTO starrs."USER"(
	"USER_ID", "FIRST_NAME", "MIDDLE_NAME", "LAST_NAME", "SEX", "HOME_PHONE", "CELL_PHONE", "WORK_PHONE", "EMAIL", "STREET_ADDRESS", "CITY", "STATE", "COUNTRY", "ZIP_CODE")
	VALUES ('300000', 'StudentA', 'S', 'Test05', 'F', '1115551111', '1115551112', '1115551113', 'StudentA@Testing.com', '501 Testing Street', 'Testville', 'MI', 'US', '11111');
INSERT INTO starrs."GRADUATE_STUDENT"(
	"USER_ID", "STATUS", "DEGREE_PROGRAM", "ADMITTED_SEMESTER")
	VALUES ('300000', '', 'MS', 'FS2023');	
	
INSERT INTO starrs."USER"(
	"USER_ID", "FIRST_NAME", "MIDDLE_NAME", "LAST_NAME", "SEX", "HOME_PHONE", "CELL_PHONE", "WORK_PHONE", "EMAIL", "STREET_ADDRESS", "CITY", "STATE", "COUNTRY", "ZIP_CODE")
	VALUES ('333333', 'StudentB', 'S', 'Test06', 'M', '1115551111', '1115551112', '1115551113', 'StudentB@Testing.com', '502 Testing Street', 'Testville', 'MI', 'US', '11111');
INSERT INTO starrs."GRADUATE_STUDENT"(
	"USER_ID", "STATUS", "DEGREE_PROGRAM", "ADMITTED_SEMESTER")
	VALUES ('333333', '', 'MS', 'WS2023');		
	
INSERT INTO starrs."USER"(
	"USER_ID", "FIRST_NAME", "MIDDLE_NAME", "LAST_NAME", "SEX", "HOME_PHONE", "CELL_PHONE", "WORK_PHONE", "EMAIL", "STREET_ADDRESS", "CITY", "STATE", "COUNTRY", "ZIP_CODE")
	VALUES ('400000', 'StudentC', 'S', 'Test07', 'F', '1115551111', '1115551112', '1115551113', 'StudentC@Testing.com', '503 Testing Street', 'Testville', 'MI', 'US', '11111');
INSERT INTO starrs."GRADUATE_STUDENT"(
	"USER_ID", "STATUS", "DEGREE_PROGRAM", "ADMITTED_SEMESTER")
	VALUES ('400000', '', 'MS', 'FS2022');		
	
INSERT INTO starrs."USER"(
	"USER_ID", "FIRST_NAME", "MIDDLE_NAME", "LAST_NAME", "SEX", "HOME_PHONE", "CELL_PHONE", "WORK_PHONE", "EMAIL", "STREET_ADDRESS", "CITY", "STATE", "COUNTRY", "ZIP_CODE")
	VALUES ('444555', 'AlumniA', 'A', 'Test08', 'M', '1115551111', '1115551112', '1115551113', 'AlumniA@Testing.com', '600 Testing Street', 'Testville', 'MI', 'US', '11111');
INSERT INTO starrs."ALUMNI"(
	"USER_ID", "DEGREE", "GPA", "GRADUATION_YEAR")
	VALUES ('444555', 'MS', 3.141, 2019);	
	
INSERT INTO starrs."USER"(
	"USER_ID", "FIRST_NAME", "MIDDLE_NAME", "LAST_NAME", "SEX", "HOME_PHONE", "CELL_PHONE", "WORK_PHONE", "EMAIL", "STREET_ADDRESS", "CITY", "STATE", "COUNTRY", "ZIP_CODE")
	VALUES ('500000', 'AlumniB', 'A', 'Test09', 'F', '1115551111', '1115551112', '1115551113', 'AlumniB@Testing.com', '601 Testing Street', 'Testville', 'MI', 'US', '11111');
INSERT INTO starrs."ALUMNI"(
	"USER_ID", "DEGREE", "GPA", "GRADUATION_YEAR")
	VALUES ('500000', 'MS', 3.75, 2012);	
	
INSERT INTO starrs."USER"(
	"USER_ID", "FIRST_NAME", "MIDDLE_NAME", "LAST_NAME", "SEX", "HOME_PHONE", "CELL_PHONE", "WORK_PHONE", "EMAIL", "STREET_ADDRESS", "CITY", "STATE", "COUNTRY", "ZIP_CODE")
	VALUES ('500500', 'FacultyA', 'F', 'Test10', 'M', '1115551111', '1115551112', '1115551113', 'FacultyA@Testing.com', '700 Testing Street', 'Testville', 'MI', 'US', '11111');
INSERT INTO starrs."FACULTY"(
	"USER_ID", "DEPARTMENT")
	VALUES ('500500', 'CIS');
	
INSERT INTO starrs."USER"(
	"USER_ID", "FIRST_NAME", "MIDDLE_NAME", "LAST_NAME", "SEX", "HOME_PHONE", "CELL_PHONE", "WORK_PHONE", "EMAIL", "STREET_ADDRESS", "CITY", "STATE", "COUNTRY", "ZIP_CODE")
	VALUES ('555555', 'FacultyB', 'F', 'Test11', 'F', '1115551111', '1115551112', '1115551113', 'FacultyB@Testing.com', '701 Testing Street', 'Testville', 'MI', 'US', '11111');
INSERT INTO starrs."FACULTY"(
	"USER_ID", "DEPARTMENT")
	VALUES ('555555', 'ECE');
	
INSERT INTO starrs."USER"(
	"USER_ID", "FIRST_NAME", "MIDDLE_NAME", "LAST_NAME", "SEX", "HOME_PHONE", "CELL_PHONE", "WORK_PHONE", "EMAIL", "STREET_ADDRESS", "CITY", "STATE", "COUNTRY", "ZIP_CODE")
	VALUES ('600000', 'FacultyC', 'F', 'Test12', 'M', '1115551111', '1115551112', '1115551113', 'FacultyC@Testing.com', '702 Testing Street', 'Testville', 'MI', 'US', '11111');
INSERT INTO starrs."FACULTY"(
	"USER_ID", "DEPARTMENT")
	VALUES ('600000', 'ABC');
	
