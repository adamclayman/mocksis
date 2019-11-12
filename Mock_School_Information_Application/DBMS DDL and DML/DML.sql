
-- Corresponds to View Schools Page l
SELECT School_Name, Street_Address, City, Zip_Code 
FROM School;

--User_Input taken directly from search/text form. This statement is used to display information from School filtered by the :USER_INPUT
SELECT School_Name, Street_Address, City, Zip_Code 
FROM School 
WHERE School_Name LIKE %:USER_INPUT%;

--Adds a new school into table School. Takes user input from forms in Add School Page which assigned to :Add_School_Name, :Add_School_Address, :Add_School_City, and :Add_School_Zip_Code respectively.
INSERT INTO School(School_Name, Street_Address, City, Zip_Code) 
VALUES (:Add_School_Name, :Add_School_Address, :Add_School_City, :Add_School_Zip_Code)

-- Corresponds to View Students Page 
SELECT Student_ID, Last_Name, First_Name, Grade_Year, School_Name 
FROM Student 
LEFT JOIN School ON Student.School_ID = School.School_ID;

--Corresponds to the "Remove" button which sets a particular student's associated School_ID to NULL from the View Students Page using value stored in :Student_ID_to_NULL
UPDATE Student SET School_ID = NULL 
WHERE Student_ID = :Student_ID_to_NULL;

--Adds a new student into table Student. Takes user input forms in Add Students page which assigned to :Add_Student_Last_Name, :Add_Student_First_Name, :Add_Student_Grade_Year, and :Add_Student_School_ID respectively.
INSERT INTO Student(Last_Name, First_Name, Grade_Year, School_ID) 
VALUES (:Add_Student_Last_Name, :Add_Student_First_Name, :Add_Student_Grade_Year, :Add_Student_School_ID);

-- Corresponds to View Staff Page 
SELECT Last_Name, First_Name, Role_Name, Certification_1, Certification_2, School_Name 
FROM 
Teaching_Staff JOIN School ON Teaching_Staff.School_ID = School.School_ID;

--Adds a new staff into table Teaching_Staff. Takes user input from forms in Add Staff which assigned to :Add_Staff_Last_Name, :Add_Staff_First_Name, :Add_Staff_Role_Name, :Add_Staff_School_ID, :Add_Staff_Certification_1, :Add_Staff_Certification_2
INSERT INTO Teaching_Staff(Last_Name, First_Name, Role_Name, School_ID, Certification_1, Certification_2) VALUES (:Add_Staff_Last_Name, :Add_Staff_First_Name, :Add_Staff_Role_Name, :Add_Staff_School_ID, :Add_Staff_Certification_1, :Add_Staff_Certification_2);

-- Corresponds to View Classes Page 
SELECT Class_ID, Class_Name, Class_Term, School_Name 
FROM 
Class JOIN School ON Class.School_ID = School.School_ID;

--Corresponds to the "Update Class" button which sets a particular Class's associated Class_Name to a new string value provided by the user in :New_Class_Name from the Edit Class Page. The specific class which is affected
--Is specified by the user from the "Edit Class Name" Button found on the view Classes Page
UPDATE Class 
SET Class_Name = :New_Class_Name
WHERE Class_ID = :Class_ID_to_Edit;

--Adds a new class into table Class. Takes user input from forms in Class Add Page which assigned to :Add_Class_Name, :Add_Class_Term, :Add_Class_School_ID respectively.
INSERT INTO Class(Class_Name, Class_Term, School_ID) VALUES (:Add_Class_Name, :Add_Class_Term, :Add_Class_School_ID);

-- Corresponds to View Class/Staff Assignment 
SELECT d.Staff_ID, b.School_Name, a.Class_Name, d.Last_Name, d.First_Name, d.Role_Name 
FROM 
Class a JOIN School b ON b.School_ID = a.School_ID 
JOIN Staff_Class c ON a.Class_ID = c.Class_ID 
JOIN Teaching_Staff d ON c.Staff_ID = d.Staff_ID;

--Corresponds to Delete Button in the View Class/Staff Assignment page. :Class_ID_to_Delete and :Staff_ID_to_Delete are specified by the user when they click on the
--Delete button for a specific class.
DELETE FROM Staff_Class 
WHERE Class_ID = :Class_ID_to_Delete AND Staff_ID = :Staff_ID_to_Delete;

--Adds a new staff and class assignment into table Staff_Class. Takes user input from Add Class/Staff Page which is assigned to :Add_ClassStaff_Class_ID and :AddClass_Staff_Staff_ID respectively.
INSERT INTO Staff_Class(Class_ID, Staff_ID) VALUES (:Add_ClassStaff_Class_ID, :Add_ClassStaff_Staff_ID);