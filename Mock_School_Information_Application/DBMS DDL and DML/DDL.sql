
DROP TABLE IF EXISTS School;

CREATE TABLE School (
  School_ID INT NOT NULL AUTO_INCREMENT,
  School_Name VARCHAR(50) NOT NULL,
  Street_Address VARCHAR(100) DEFAULT NULL,
  City VARCHAR(50) DEFAULT NULL,
  Zip_Code VARCHAR(10) DEFAULT NULL,
  PRIMARY KEY (School_ID),
  UNIQUE KEY School_Name (School_Name)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;

INSERT INTO School VALUES (1,'Spruce High School', '1 Avenue Way','Rolling Hills','96789'),
(2,'Forrest High School', '2 Parkway Avenue','Forrest','96822'), 
(3,'Washington Elementary School', '3 Vista Loop','Grove','96788');

DROP TABLE IF EXISTS Student;

CREATE TABLE Student (
  Student_ID INT NOT NULL AUTO_INCREMENT,
  First_Name VARCHAR(40) NOT NULL,
  Last_Name VARCHAR(40) NOT NULL,
  Grade_Year TINYINT NOT NULL,
  School_ID INT DEFAULT NULL,
  PRIMARY KEY (Student_ID),
  FOREIGN KEY (School_ID) REFERENCES School (School_ID) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;

INSERT INTO Student VALUES (1,'Bob', 'Cat', 4, 3), (2,'John', 'Sy', 12, 1), (3,'Adam', 'Clayman', 11, 2);
--

DROP TABLE IF EXISTS Teaching_Staff;

CREATE TABLE Teaching_Staff (
  Staff_ID INT NOT NULL AUTO_INCREMENT,
  Role_Name VARCHAR(30) NOT NULL,
  First_Name VARCHAR(40) NOT NULL,
  Last_Name VARCHAR(40) NOT NULL,
  Certification_1 VARCHAR(50) DEFAULT NULL,
  Certification_2 VARCHAR(50) DEFAULT NULL,
  School_ID INT,
  PRIMARY KEY (Staff_ID),
  FOREIGN KEY (School_ID) REFERENCES School (School_ID) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;

INSERT INTO Teaching_Staff VALUES (1,'Instructor','Bat', 'Man', 'Hero', '', 3), (2,'Teaching Assistant','Cat','Man', 'Comp Sci', '', 2),(3,'Instructor','Deborah', 'Ries', 'Chemistry', '', 1);


DROP TABLE IF EXISTS Class;

CREATE TABLE Class (
  Class_ID INT NOT NULL AUTO_INCREMENT,
  Class_Name VARCHAR(100) NOT NULL,
  Class_Term VARCHAR(30) NOT NULL,
  School_ID INT,
  PRIMARY KEY (Class_ID),
  FOREIGN KEY (School_ID) REFERENCES School (School_ID) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT = 1 DEFAULT CHARSET=latin1;

INSERT INTO Class VALUES (1,'Chemistry', 'Fall 2019', 1),(2, 'Computer Science', 'Fall 2019',  2),(3, 'English', 'Fall 2019', 3);


DROP TABLE IF EXISTS Staff_Class;

CREATE TABLE Staff_Class (
  Staff_Class_ID INT AUTO_INCREMENT,
  Class_ID INT,
  Staff_ID INT,
  PRIMARY KEY (Staff_Class_ID),
  FOREIGN KEY (Class_ID) REFERENCES Class (Class_ID) ON DELETE CASCADE,
  FOREIGN KEY (Staff_ID) REFERENCES Teaching_Staff (Staff_ID) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT = 1 DEFAULT  CHARSET=latin1;


INSERT INTO `Staff_Class` VALUES (1,1,3),(2, 2, 2),(3, 3, 1);


