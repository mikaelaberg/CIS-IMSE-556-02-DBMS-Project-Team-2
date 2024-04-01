## Test cases for graduate app:
### 1. Student ID:
- [ ] 1.1 Verification of system prompts student ID on page load up

  - Got the database connected, just have to populate the data down. 

- [ ] 1.2 Verification of “not a student” status for people not through the application process
- [ ] 1.3 Verification of “currently enrolled” status for active students
- [ ] 1.4 Verification of “waiting for graduation” status for students not in courses and waiting for an audit 
- [ ] 1.5 Verification of “cleared for graduation” status for students who passed the audit and are waiting on the GS approval 
- [ ] 1.6 Verification of “graduated” status for students who passed the audit and have been approved by the GS. This should reroute them to the alumni page.

TODO   
### 2. Student ID+ Degree Verification:
- [ ] 2.1 Verification of student ID + degree type matching
- [ ] 2.2 Verification of degree selection via dropdown menu 
- [ ] 2.3 Verification of system confirming enrollment in the selected degree
- [ ] 2.4 Verification of graduation requirements queued up and displayed post selection

### 3. Degree Requirements Audit:
- [ ] 3.1 Verification of audit success giving “status cleared” for graduation approval 
- [ ] 3.2 Verification of audit failure giving “status not cleared” and displays reason of failure 
- [ ] 3.3 Verification of graduation status displaying correctly next to the student name

### 4. Graduation Status: 
- [ ] 4.1 Verification of “Cleared: Waiting for Graduation” status for students waiting for GS approval 
- [ ] 4.2 Verification of “Cleared: Graduated” status for students approved by GS and transitioned to alumni 
- [ ] 4.3 Verification of “Not Cleared: Cannot Graduate” status for students who failed the audit. 

### 5. Database Integrity: 
- [ ] 5.1 Verification of students who received “Cleared: Graduated” has been removed from current student enrolled table 
- [ ] 5.2 Verification of students who received “Cleared: Graduated” has been moved to the alumni table.

### 6. Alumni Page Access + Info. Display: 
- [ ] 6.1 Verification the graduated student has access to the alumni page
- [ ] 6.2 Verification that the student information displayed is accurate:
  - [ ] 6.2.1 Personal information: Address, email ect. 
  - [ ] 6.2.2 Graduation details: Degree, GPA, ect. 
  - [ ] 6.2.3 Academic Transcript: Previous courses, when they were taken, grade, ect. 


###### References: 
[Markdown cheatsheet](https://www.datacamp.com/cheat-sheet/markdown-cheat-sheet-23)