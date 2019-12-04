from flask import Flask, render_template, request, redirect
from db_connector.db_connector import connect_to_database, execute_query

app = Flask(__name__, static_url_path='/static')

#This view returns the index.html Homepage
@app.route('/')
def index():
    return render_template('index.html')

#This view handles the View Schools Page
@app.route('/schools', methods=['POST', 'GET'])
def schools():
	#Connect to your database and create a new database object
	db_connection = connect_to_database()

	#If a GET request was the method by which the page was requested, then we will display all the user-relevant information from the School table
	if request.method == 'GET':
		
		query = 'SELECT School_Name, Street_Address, City, Zip_Code FROM School;'

		result = execute_query(db_connection, query).fetchall();
		
		return render_template('schools.html', SELECT_School_Rows = result)

	#If a POST request was the method by which the page was requested, then the user arrives to this page after having used the Search form/submit button
	elif request.method == 'POST':

		#Take the user supplied string they are interested in using for their search criteria
		Search_String = request.form['FindSchoolName']

		#Add MariaDB compliant wildcard SQL operators on either side of the user's search string and save the result as a string object assigned to var pattern.
		pattern = '%' + Search_String + '%'

		#Execute a SELECT query using the user's search term concatenated with the SQL wildcards to the database object. Store the result of the query in var result. The values correspond to the variable SELECT_School_Rows in the Jinja template.
		result = execute_query(db_connection, 'SELECT School_Name, Street_Address, City, Zip_Code FROM School WHERE School_Name LIKE %s;', (pattern,)).fetchall();

		#Populate the table in schools.html template with the values stored in var result.
		return render_template('schools.html', SELECT_School_Rows = result)

#This view handles the Add Schools Page and form
@app.route('/schoolsadd', methods=['POST', 'GET'])
def schoolsadd():

	#If a GET request was the method by which the page was requested, then we will display the page containing empty forms for adding a new School.
	if request.method == 'GET':

		return render_template('schoolsadd.html')

	#If a POST request was the method by which the page was requested, then the user arrives to this page after having used the forms involved in adding a new School.
	elif request.method == 'POST':
		#Connect to your database and create a new database object
		db_connection = connect_to_database()

		#Obtain the user supplied strings from the forms in the Add Schools Page and assign them to the correspondingly named variables below.
		School_Name = request.form['SchoolNameInput']

		School_Address = request.form['SchoolAddressInput']

		School_City = request.form['SchoolCityInput']

		School_Zipcode = request.form['SchoolZipcodeInput']

		#Create a string representation of an INSERT query into the School Table
		query = 'INSERT INTO School(School_Name, Street_Address, City, Zip_Code) VALUES (%s, %s, %s, %s);'
		#Use the variables containing user input from the forms and store them together as a tuple assigned to var data.
		data = (School_Name, School_Address, School_City, School_Zipcode)

		#Execute the query using the query's string representation, tuple of user supplied data, and the database object. 
		execute_query(db_connection, query, data)

		return redirect('/schools')

#This view handles the View Students Page
@app.route('/students', methods=['GET'])
def students():

	#Connect to your database and create a new database object
	db_connection = connect_to_database()

	#Create a string object representation of a SELECT query retrieving user-relevant information from the Student table
	query = 'SELECT Student_ID, Last_Name, First_Name, Grade_Year, School_Name FROM Student LEFT JOIN School ON Student.School_ID = School.School_ID;'

	#Execute the above query with the database object and store the resulting data returned in var result.
	result = execute_query(db_connection, query).fetchall();
	
	#Populate the table in students.html template with the values stored in var result. The values correspond to the variable SELECT_Student_Rows in the Jinja template.	
	return render_template('students.html', SELECT_Student_Rows = result)

#This view handles the result of a user pressing the 'Remove' button in the View Students page in the row for a particular student. This update's that student's School_ID attribute to NULL. The int Student_ID variable corresponds to a primary key in table Student.
@app.route('/studentnull/<int:Student_ID>')
def studentnull(Student_ID):

	#Connect to your database and create a new database object
	db_connection = connect_to_database()

	#Create a string object representation of an UPDATE query for updating the School_ID attribute of a particular student identified by the foreign key Student_ID referencing the Student_ID from the Student table to NULL. This effectively removes a Student's relationship with their referenced School.
	query = 'UPDATE Student SET School_ID = NULL WHERE Student_ID = %s;'

	#Store the data corresponding to the student's Student_ID in a tuple object assigned to var data.
	data = (Student_ID,)

	#Execute the above query with the database object and tuple object containing the Student_ID value.
	execute_query(db_connection, query, data)

	#Redirect the user back to the '/students' view to show the updated value of the student's school.
	return redirect('/students')

#This view handles the Add Students Page and form
@app.route('/studentsadd', methods=['POST', 'GET'])
def studentsadd():

	#Connect to your database and create a new database object
	db_connection = connect_to_database()

	#If a GET request was the method by which the page was requested, then we will display the page containing forms for adding a new Student.
	if request.method == 'GET':

		#Create a string object representation of a SELECT query retrieving the names of all schools currently existing in the School Table.
		query = 'SELECT School_ID, School_Name FROM School'

		#Execute the above query with the database object.
		result = execute_query(db_connection, query).fetchall();

		#Populate the the drop-down selector/menu with the School names returned from the above SELECT query, for the user to choose which School the new Student they are adding will attend.
		return render_template('studentsadd.html', Schools = result)

	elif request.method == 'POST':

		Student_LastName = request.form['StudentLastNameInput']

		Student_FirstName = request.form['StudentFirstNameInput']

		Student_GradeYear = request.form['StudentGradeYearInput']

		Student_SchoolID = request.form['StudentSchoolIDInput']

		query = 'INSERT INTO Student(Last_Name, First_Name, Grade_Year, School_ID) VALUES (%s, %s, %s, %s);'

		data = (Student_LastName, Student_FirstName, Student_GradeYear, Student_SchoolID)

		execute_query(db_connection, query, data)

		return redirect('/students')

@app.route('/staff', methods=['GET'])
def staff():

	db_connection = connect_to_database()

	query = 'SELECT Last_Name, First_Name, Role_Name, Certification_1, Certification_2, School_Name FROM Teaching_Staff JOIN School ON Teaching_Staff.School_ID = School.School_ID;'

	result = execute_query(db_connection, query).fetchall();
		
	return render_template('staff.html', SELECT_Staff_Rows = result)

@app.route('/staffadd', methods=['POST', 'GET'])
def staffadd():

	db_connection = connect_to_database()

	if request.method == 'GET':

		query ='SELECT School_ID, School_Name FROM School'

		result = execute_query(db_connection, query).fetchall();

		return render_template('staffadd.html', Schools = result)

	elif request.method == 'POST':
		
		Staff_LastName = request.form['StaffLastNameInput']

		Staff_FirstName = request.form['StaffFirstNameInput']

		Staff_Role = request.form['StaffRoleInput']

		Staff_SchoolID = request.form['StaffSchoolIDInput']

		Staff_Certification_1 = request.form['StaffCertification1Input']

		Staff_Certification_2 = request.form['StaffCertification2Input']

		query = 'INSERT INTO Teaching_Staff(Last_Name, First_Name, Role_Name, School_ID, Certification_1, Certification_2) VALUES (%s, %s, %s, %s, %s, %s);'

		data = (Staff_LastName, Staff_FirstName, Staff_Role, Staff_SchoolID, Staff_Certification_1, Staff_Certification_2)

		execute_query(db_connection, query, data)

		return redirect('/staff')

@app.route('/classes', methods=['GET'])
def classes():

	db_connection = connect_to_database()

	query = 'SELECT Class_ID, Class_Name, Class_Term, School_Name FROM Class JOIN School ON Class.School_ID = School.School_ID;'

	result = execute_query(db_connection, query).fetchall();
		
	return render_template('classes.html', SELECT_Class_Rows = result)

@app.route('/classesedit/<int:Class_ID>', methods=['POST', 'GET'])
def classesedit(Class_ID):

	if request.method == 'GET':

		return render_template('classesedit.html')

	elif request.method == 'POST':

		db_connection = connect_to_database()

		New_ClassName = request.form['EditClassNameInput']

		query = 'UPDATE Class SET Class_Name = %s WHERE Class_ID = %s;'

		data = (New_ClassName, Class_ID,)

		execute_query(db_connection, query, data)

		return redirect('/classes')

@app.route('/classesadd', methods=['POST', 'GET'])
def classesadd():

	db_connection = connect_to_database()

	if request.method == 'GET':

		query ='SELECT School_ID, School_Name FROM School'

		result = execute_query(db_connection, query).fetchall();

		return render_template('classesadd.html', Schools = result)

	elif request.method == 'POST':

		Class_Name = request.form['AddClassNameInput']

		Class_Term = request.form['AddClassTermInput']

		Class_SchoolID = request.form['AddClassSchoolIDInput']

		query = 'INSERT INTO Class(Class_Name, Class_Term, School_ID) VALUES (%s, %s, %s);'

		data = (Class_Name, Class_Term, Class_SchoolID)

		execute_query(db_connection, query, data)

		return redirect('/classes')

@app.route('/classstaff', methods=['GET'])
def classstaff():

	db_connection = connect_to_database()

	query = 'SELECT c.Staff_Class_ID, b.School_Name, a.Class_Name, d.Last_Name, d.First_Name, d.Role_Name FROM Class a JOIN School b ON b.School_ID = a.School_ID JOIN Staff_Class c ON a.Class_ID = c.Class_ID JOIN Teaching_Staff d ON c.Staff_ID = d.Staff_ID;'

	result = execute_query(db_connection, query).fetchall();
		
	return render_template('classstaff.html', SELECT_Class_Staff_Rows = result)

@app.route('/staffclassdelete/<int:StaffClass_ID>')
def staffclassdelete(StaffClass_ID):

	db_connection = connect_to_database()

	query = 'DELETE FROM Staff_Class WHERE Staff_Class_ID = %s;'

	data = (StaffClass_ID,)

	execute_query(db_connection, query, data)

	return redirect('/classstaff')

@app.route('/classstaffadd', methods=['POST', 'GET'])
def classstaffadd():
	db_connection = connect_to_database()

	if request.method == 'GET':

		query ='SELECT Staff_ID, First_Name, Last_Name FROM Teaching_Staff;'

		result = execute_query(db_connection, query).fetchall();

		query ='SELECT Class_ID, Class_Name FROM Class;'

		result2 = execute_query(db_connection, query).fetchall();

		return render_template('classstaffadd.html', Staff = result, Classes = result2)

	elif request.method == 'POST':

		Class_ID = request.form['ClassIDInput']

		Staff_ID = request.form['StaffIDInput']

		query = 'INSERT INTO Staff_Class(Class_ID, Staff_ID) VALUES (%s, %s);'

		data = (Class_ID, Staff_ID)

		execute_query(db_connection, query, data)

		return redirect('/classstaff')

