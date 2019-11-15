from flask import Flask, render_template
from flask import request
from db_connector.db_connector import connect_to_database, execute_query

app = Flask(__name__, static_url_path='/static')

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/schools', methods=['POST', 'GET'])
def schools():
	db_connection = connect_to_database()

	if request.method == 'GET':
		
		query = "SELECT School_Name, Street_Address, City, Zip_Code FROM School;"

		result = execute_query(db_connection, query).fetchall();
		
		return render_template('schools.html', SELECT_School_Rows = result)

	elif request.method == 'POST':

		Search_String = request.form['FindSchoolName']

		pattern = "%" + Search_String + "%"

		result = execute_query(db_connection, "SELECT School_Name, Street_Address, City, Zip_Code FROM School WHERE School_Name LIKE %s;", (pattern,)).fetchall();

		return render_template('schools.html', SELECT_School_Rows = result)

@app.route('/schoolsadd', methods=['POST', 'GET'])
def schoolsadd():

	if request.method == 'GET':

		return render_template('schoolsadd.html')

	elif request.method == 'POST':

		db_connection = connect_to_database()

		School_Name = request.form['SchoolNameInput']

		School_Address = request.form['SchoolAddressInput']

		School_City = request.form['SchoolCityInput']

		School_Zipcode = request.form['SchoolZipcodeInput']

		query = "INSERT INTO School(School_Name, Street_Address, City, Zip_Code) VALUES (%s, %s, %s, %s);"

		data = (School_Name, School_Address, School_City, School_Zipcode)

		execute_query(db_connection, query, data)

		return render_template('schools.html')

@app.route('/students', methods=['GET'])
def students():

	db_connection = connect_to_database()

	query = "SELECT Student_ID, Last_Name, First_Name, Grade_Year, School_Name FROM Student LEFT JOIN School ON Student.School_ID = School.School_ID;"

	result = execute_query(db_connection, query).fetchall();
		
	return render_template('students.html', SELECT_Student_Rows = result)

@app.route('/studentnull/<int:Student_ID>')
def studentnull(Student_ID):
	db_connection = connect_to_database()

	query = "UPDATE Student SET School_ID = NULL WHERE Student_ID = %s;"

	data = (Student_ID,)

	result = execute_query(db_connection, query, data)

	query = "SELECT Student_ID, Last_Name, First_Name, Grade_Year, School_Name FROM Student LEFT JOIN School ON Student.School_ID = School.School_ID;"

	result = execute_query(db_connection, query).fetchall();
		
	return render_template('students.html', SELECT_Student_Rows = result)

@app.route('/studentsadd', methods=['POST', 'GET'])
def studentsadd():

	db_connection = connect_to_database()

	if request.method == 'GET':

		query = "SELECT School_ID, School_Name FROM School"

		result = execute_query(db_connection, query).fetchall();

		return render_template('studentsadd.html', Schools = result)

	elif request.method == 'POST':

		Student_LastName = request.form['StudentLastNameInput']

		Student_FirstName = request.form['StudentFirstNameInput']

		Student_GradeYear = request.form['StudentGradeYearInput']

		Student_SchoolID = request.form['StudentSchoolIDInput']

		query = "INSERT INTO Student(Last_Name, First_Name, Grade_Year, School_ID) VALUES (%s, %s, %s, %s);"

		data = (Student_LastName, Student_FirstName, Student_GradeYear, Student_SchoolID)

		execute_query(db_connection, query, data)

		query = "SELECT Student_ID, Last_Name, First_Name, Grade_Year, School_Name FROM Student LEFT JOIN School ON Student.School_ID = School.School_ID;"

		result = execute_query(db_connection, query).fetchall();
			
		return render_template('students.html', SELECT_Student_Rows = result)

@app.route('/staff', methods=['GET'])
def staff():

	db_connection = connect_to_database()

	query = "SELECT Last_Name, First_Name, Role_Name, Certification_1, Certification_2, School_Name FROM Teaching_Staff JOIN School ON Teaching_Staff.School_ID = School.School_ID;"

	result = execute_query(db_connection, query).fetchall();
		
	return render_template('staff.html', SELECT_Staff_Rows = result)


@app.route('/staffadd', methods=['POST', 'GET'])
def staffadd():

	db_connection = connect_to_database()

	if request.method == 'GET':

		query ="SELECT School_ID, School_Name FROM School"

		result = execute_query(db_connection, query).fetchall();

		return render_template('staffadd.html', Schools = result)

	elif request.method == 'POST':
		
		Staff_LastName = request.form['StaffLastNameInput']

		Staff_FirstName = request.form['StaffFirstNameInput']

		Staff_Role = request.form['StaffRoleInput']

		Staff_SchoolID = request.form['StaffSchoolIDInput']

		Staff_Certification_1 = request.form['StaffCertification1Input']

		Staff_Certification_2 = request.form['StaffCertification2Input']

		query = "INSERT INTO Teaching_Staff(Last_Name, First_Name, Role_Name, School_ID, Certification_1, Certification_2) VALUES (%s, %s, %s, %s, %s, %s);"

		data = (Staff_LastName, Staff_FirstName, Staff_Role, Staff_SchoolID, Staff_Certification_1, Staff_Certification_2)

		execute_query(db_connection, query, data)

		query = "SELECT Last_Name, First_Name, Role_Name, Certification_1, Certification_2, School_Name FROM Teaching_Staff JOIN School ON Teaching_Staff.School_ID = School.School_ID ;"

		result = execute_query(db_connection, query).fetchall();
			
		return render_template('staff.html', SELECT_Staff_Rows = result)

@app.route('/classes', methods=['GET'])
def classes():

	db_connection = connect_to_database()

	query = "SELECT Class_ID, Class_Name, Class_Term, School_Name FROM Class JOIN School ON Class.School_ID = School.School_ID;"

	result = execute_query(db_connection, query).fetchall();
		
	return render_template('classes.html', SELECT_Class_Rows = result)


@app.route('/classesedit/<int:Class_ID>', methods=['POST', 'GET'])
def classesedit(Class_ID):

	if request.method == 'GET':

		return render_template('classesedit.html')

	elif request.method == 'POST':

		db_connection = connect_to_database()

		New_ClassName = request.form['EditClassNameInput']

		query = "UPDATE Class SET Class_Name = %s WHERE Class_ID = %s;"

		data = (New_ClassName, Class_ID,)

		execute_query(db_connection, query, data)

		query = "SELECT Class_ID, Class_Name, Class_Term, School_Name FROM Class JOIN School ON Class.School_ID = School.School_ID;"

		result = execute_query(db_connection, query).fetchall();
			
		return render_template('classes.html', SELECT_Class_Rows = result)


@app.route('/classesadd', methods=['POST', 'GET'])
def classesadd():

	db_connection = connect_to_database()


	if request.method == 'GET':

		query ="SELECT School_ID, School_Name FROM School"

		result = execute_query(db_connection, query).fetchall();

		return render_template('classesadd.html', Schools = result)

	elif request.method == 'POST':

		Class_Name = request.form['AddClassNameInput']

		Class_Term = request.form['AddClassTermInput']

		Class_SchoolID = request.form['AddClassSchoolIDInput']

		query = "INSERT INTO Class(Class_Name, Class_Term, School_ID) VALUES (%s, %s, %s);"

		data = (Class_Name, Class_Term, Class_SchoolID)

		execute_query(db_connection, query, data)

		query = "SELECT Class_ID, Class_Name, Class_Term, School_Name FROM Class JOIN School ON Class.School_ID = School.School_ID;"

		result = execute_query(db_connection, query).fetchall();
			
		return render_template('classes.html', SELECT_Class_Rows = result)


@app.route('/classstaff', methods=['GET'])
def classstaff():

	db_connection = connect_to_database()

	query = "SELECT d.Staff_ID, b.School_Name, a.Class_Name, d.Last_Name, d.First_Name, d.Role_Name FROM Class a JOIN School b ON b.School_ID = a.School_ID JOIN Staff_Class c ON a.Class_ID = c.Class_ID JOIN Teaching_Staff d ON c.Staff_ID = d.Staff_ID;"

	result = execute_query(db_connection, query).fetchall();
		
	return render_template('classstaff.html', SELECT_Class_Staff_Rows = result)


@app.route('/staffclassdelete/<int:StaffClass_ID>')
def staffclassdelete(StaffClass_ID):

	db_connection = connect_to_database()

	query = "DELETE FROM Staff_Class WHERE Staff_Class_ID = %s;"

	data = (StaffClass_ID,)

	result = execute_query(db_connection, query, data)

	query = "SELECT b.Staff_Class_ID, a.Class_Name, c.Last_Name, c.First_Name, c.Role_Name FROM Class a JOIN Staff_Class b ON a.Class_ID = b.Class_ID JOIN Teaching_Staff c ON b.Staff_ID = c.Staff_ID;"

	result = execute_query(db_connection, query).fetchall();
		
	return render_template('classstaff.html', SELECT_Class_Staff_Rows = result)


@app.route('/classstaffadd', methods=['POST', 'GET'])
def classstaffadd():

	if request.method == 'GET':

		query ="SELECT Staff_ID, First_Name, Last_Name FROM Teaching_Staff"

		result = execute_query(db_connection, query).fetchall();

		query ="SELECT Class_ID, Class_Name FROM Class"

		result2 = execute_query(db_connection, query).fetchall();

		return render_template('classstaffadd.html', Staff = result, Classes = result2)


	elif request.method == 'POST':

		db_connection = connect_to_database()

		Class_ID = request.form['ClassIDInput']

		Staff_ID = request.form['StaffIDInput']

		query = "INSERT INTO Staff_Class(Class_ID, Staff_ID) VALUES (%s, %s);"

		data = (Class_ID, Staff_ID)

		execute_query(db_connection, query, data)

		query = "SELECT d.Staff_ID, b.School_Name, a.Class_Name, d.Last_Name, d.First_Name, d.Role_Name FROM Class a JOIN School b ON b.School_ID = a.School_ID JOIN Staff_Class c ON a.Class_ID = c.Class_ID JOIN Teaching_Staff d ON c.Staff_ID = d.Staff_ID;"

		result = execute_query(db_connection, query).fetchall();
			
		return render_template('classstaff.html', SELECT_Class_Staff_Rows = result)