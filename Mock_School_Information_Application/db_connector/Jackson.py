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

	#If a POST request was the method by which the page was requested, then the user arrives to this view after having used the forms involved in adding a new School.
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

	#Create a string object representation of a SELECT query retrieving user-relevant information from the Student table joined with the School table (to also display the School in which each Student attends).
	query = 'SELECT Student_ID, Last_Name, First_Name, Grade_Year, School_Name FROM Student LEFT JOIN School ON Student.School_ID = School.School_ID;'

	#Execute the above query with the database object and store the resulting data returned in var result.
	result = execute_query(db_connection, query).fetchall();
	
	#Populate the table in students.html template with the values stored in var result. The values correspond to the variable SELECT_Student_Rows in the Jinja template.	
	return render_template('students.html', SELECT_Student_Rows = result)

#This view handles the result of a user pressing the 'Remove' button in the View Students page in the row for a particular student. This UPDATEs that student's School_ID attribute to NULL. The int Student_ID variable corresponds to the primary key in table Student.
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

		#Populate the the drop-down selector/menu with the School names returned from the above SELECT query, for the user to choose which School the new Student they are adding will attend. The values correspond to the variable 'Schools' in the Jinja template.
		return render_template('studentsadd.html', Schools = result)

	#If a POST request was the method by which the page was requested, then the user arrives to this view after having used the forms involved in adding a new Student.
	elif request.method == 'POST':

		#Obtain the user supplied strings from the forms in the Add Students Page and assign them to the correspondingly named variables below.
		Student_LastName = request.form['StudentLastNameInput']

		Student_FirstName = request.form['StudentFirstNameInput']

		Student_GradeYear = request.form['StudentGradeYearInput']

		Student_SchoolID = request.form['StudentSchoolIDInput']

		#Create a string representation of an INSERT query into the School Table
		query = 'INSERT INTO Student(Last_Name, First_Name, Grade_Year, School_ID) VALUES (%s, %s, %s, %s);'

		#Use the variables containing user input from the forms and store them together as a tuple assigned to var data.
		data = (Student_LastName, Student_FirstName, Student_GradeYear, Student_SchoolID)

		#Execute the query using the query's string representation, tuple of user supplied data, and the database object. 
		execute_query(db_connection, query, data)

		#Redirect the user back to the '/students' view to show the newly added Student.
		return redirect('/students')

#This view handles the View Staff Page
@app.route('/staff', methods=['GET'])
def staff():

	#Connect to your database and create a new database object
	db_connection = connect_to_database()

	#Create a string object representation of a SELECT query retrieving user-relevant information from the Staff table joined with the School table (to also display the School in which each Staff member is involved in teaching at).
	query = 'SELECT Last_Name, First_Name, Role_Name, Certification_1, Certification_2, School_Name FROM Teaching_Staff JOIN School ON Teaching_Staff.School_ID = School.School_ID;'

	#Execute the above query with the database object and store the resulting data returned in var result.
	result = execute_query(db_connection, query).fetchall();
	
	#Populate the table in staff.html template with the values stored in var result. The values correspond to the variable SELECT_Staff_Rows in the Jinja template.
	return render_template('staff.html', SELECT_Staff_Rows = result)

#This view handles the Add Staff Page and form
@app.route('/staffadd', methods=['POST', 'GET'])
def staffadd():

	#Connect to your database and create a new database object
	db_connection = connect_to_database()

	#If a GET request was the method by which the page was requested, then we will display the page containing empty forms for adding a new Staff member.
	if request.method == 'GET':

		#Create a string object representation of a SELECT query retrieving the names of all schools currently existing in the School Table.
		query ='SELECT School_ID, School_Name FROM School'

		#Execute the above query with the database object.
		result = execute_query(db_connection, query).fetchall();

		#Populate the the drop-down selector/menu with the School names returned from the above SELECT query, for the user to choose which School the new Staff member will be assigned to teach. The values correspond to the variable 'Schools' in the Jinja template.
		return render_template('staffadd.html', Schools = result)

	#If a POST request was the method by which the page was requested, then the user arrives to this view after having used the forms involved in adding a new Staff member.
	elif request.method == 'POST':
		
		#Obtain the user supplied strings from the forms in the Add Staff Page and assign them to the correspondingly named variables below.
		Staff_LastName = request.form['StaffLastNameInput']

		Staff_FirstName = request.form['StaffFirstNameInput']

		Staff_Role = request.form['StaffRoleInput']

		Staff_SchoolID = request.form['StaffSchoolIDInput']

		Staff_Certification_1 = request.form['StaffCertification1Input']

		Staff_Certification_2 = request.form['StaffCertification2Input']

		#Create a string representation of an INSERT query into the Staff Table
		query = 'INSERT INTO Teaching_Staff(Last_Name, First_Name, Role_Name, School_ID, Certification_1, Certification_2) VALUES (%s, %s, %s, %s, %s, %s);'

		#Use the variables containing user input from the forms and store them together as a tuple assigned to var data.
		data = (Staff_LastName, Staff_FirstName, Staff_Role, Staff_SchoolID, Staff_Certification_1, Staff_Certification_2)

		#Execute the query using the query's string representation, tuple of user supplied data, and the database object. 
		execute_query(db_connection, query, data)

		#Redirect the user back to the '/students' view to show the newly added Staff member.
		return redirect('/staff')

#This view handles the View Classes Page
@app.route('/classes', methods=['GET'])
def classes():

	#Connect to your database and create a new database object
	db_connection = connect_to_database()

	#Create a string object representation of a SELECT query retrieving user-relevant information from the Class table joined with the School table (to also display the School in which each Class is held/taught at).
	query = 'SELECT Class_ID, Class_Name, Class_Term, School_Name FROM Class JOIN School ON Class.School_ID = School.School_ID;'

	#Execute the above query with the database object and store the resulting data returned in var result.
	result = execute_query(db_connection, query).fetchall();
	
	#Populate the table in classes.html template with the values stored in var result. The values correspond to the variable SELECT_Class_Rows in the Jinja template.	
	return render_template('classes.html', SELECT_Class_Rows = result)

#This view handles the result of a user pressing the 'Edit' button in the View Classes page in the row for a particular Class. Pressing the aforementioned button corresponding to a row in the Class table will take the user to a page
#containing a text form by which the user can UPDATE the Class_Name attribute of the chosen row to another value based on what string is supplied by the user through the form. The int Class_ID variable corresponds to the primary key in table Class.
@app.route('/classesedit/<int:Class_ID>', methods=['POST', 'GET'])
def classesedit(Class_ID):

	#If a GET request was the method by which the page was requested, then we will display the page containing an empty textform for inputting a new value for the Class_Name attribute for this particular row in the Class table
	if request.method == 'GET':

		return render_template('classesedit.html')

	#If a POST request was the method by which the page was requested, then the user arrives to this view after having used the forms involved in updating a class's name.
	elif request.method == 'POST':

		#Connect to your database and create a new database object
		db_connection = connect_to_database()

		#Obtain the user supplied strings from the forms in the Edit Class Page and assign them to the correspondingly named variable below.
		New_ClassName = request.form['EditClassNameInput']

		#Create a string representation of an UPDATE query into the Class Table
		query = 'UPDATE Class SET Class_Name = %s WHERE Class_ID = %s;'

		#Use the variable containing user input from the form and store it as a tuple assigned to var data.
		data = (New_ClassName, Class_ID,)

		#Execute the query using the query's string representation, tuple of user "selected" data, and the database object. 
		execute_query(db_connection, query, data)

		#Redirect the user back to the '/students' view to show the newly updated Class's name.
		return redirect('/classes')

#This view handles the Add Classes Page and form
@app.route('/classesadd', methods=['POST', 'GET'])
def classesadd():

	#Connect to your database and create a new database object
	db_connection = connect_to_database()

	#If a GET request was the method by which the page was requested, then we will display the page containing empty forms for adding a new Class.
	if request.method == 'GET':

		#Create a string object representation of a SELECT query retrieving the names of all schools currently existing in the School Table.
		query ='SELECT School_ID, School_Name FROM School'

		#Execute the above query with the database object.
		result = execute_query(db_connection, query).fetchall();

		#Populate the the drop-down selector/menu with the School names returned from the above SELECT query, for the user to choose which School the new Class will be assigned to. The values correspond to the variable 'Schools' in the Jinja template.
		return render_template('classesadd.html', Schools = result)

	#If a POST request was the method by which the page was requested, then the user arrives to this view after having used the forms involved in adding a new Class.
	elif request.method == 'POST':

		#Obtain the user supplied strings from the forms in the Add Staff Page and assign them to the correspondingly named variables below.
		Class_Name = request.form['AddClassNameInput']

		Class_Term = request.form['AddClassTermInput']

		Class_SchoolID = request.form['AddClassSchoolIDInput']

		#Create a string representation of an INSERT query into the Class Table
		query = 'INSERT INTO Class(Class_Name, Class_Term, School_ID) VALUES (%s, %s, %s);'

		#Use the variables containing user input from the forms and store them together as a tuple assigned to var data.
		data = (Class_Name, Class_Term, Class_SchoolID)

		#Execute the query using the query's string representation, tuple of user supplied data, and the database object. 
		execute_query(db_connection, query, data)

		#Redirect the user back to the '/students' view to show the newly added Class.
		return redirect('/classes')

#This view handles the View Class/Staff Assignment Page
@app.route('/classstaff', methods=['GET'])
def classstaff():

	#Connect to your database and create a new database object
	db_connection = connect_to_database()

	#Create a string object representation of a SELECT query retrieving user-relevant information from the Class table joined with the Staff_Class table joined with the School table (to also display Class Name, the Staff Name who teaches the Class, and which School the Class is taught at).
	query = 'SELECT c.Staff_Class_ID, b.School_Name, a.Class_Name, d.Last_Name, d.First_Name, d.Role_Name FROM Class a JOIN School b ON b.School_ID = a.School_ID JOIN Staff_Class c ON a.Class_ID = c.Class_ID JOIN Teaching_Staff d ON c.Staff_ID = d.Staff_ID;'

	#Execute the above query with the database object and store the returned information in var result.
	result = execute_query(db_connection, query).fetchall();
	
	#Populate the table in classstaff.html template with the values stored in var result. The values correspond to the variable SELECT_Class_Staff_Rows in the Jinja template.
	return render_template('classstaff.html', SELECT_Class_Staff_Rows = result)

#This view handles the result of a user pressing a 'Delete' button in the View Class/Staff Assignment page which corresponds to a row in the Staff_Class Table. Pressing the aforementioned button will trigger the creation of a DELETE query to the database
#in which the row's Staff_Class_ID will be used to specify which row in the Staff_Class Table should be deleted. The int StaffClass_ID variable corresponds to the primary key in table Staff_Class.
@app.route('/staffclassdelete/<int:StaffClass_ID>')
def staffclassdelete(StaffClass_ID):

	#Connect to your database and create a new database object
	db_connection = connect_to_database()

	#Create a string object representation of a DELETE query for deleting the row identified by the StaffClass_ID variable.
	query = 'DELETE FROM Staff_Class WHERE Staff_Class_ID = %s;'

	#Use the StaffClass_ID variable within a tuple object and store in var data.
	data = (StaffClass_ID,)

	#Execute the query using the query's string representation, tuple of user "selected" data, and the database object. 
	execute_query(db_connection, query, data)

	#Redirect the user back to the '/classstaff' view to show the table that now no longer contains the row that was chosen for deletion.
	return redirect('/classstaff')

#This view handles the Add Class/Staff Assignment Page and forms
@app.route('/classstaffadd', methods=['POST', 'GET'])
def classstaffadd():

	#Connect to your database and create a new database object
	db_connection = connect_to_database()

	#If a GET request was the method by which the page was requested, then we will display the page containing the dynamically populated drop-down menu/slector forms required to insert a new row in Staff_Class Table.
	if request.method == 'GET':

		#Create a string object representation of a SELECT query retrieving the Staff_ID, First_Name and Last_Name of all teaching staff members from the Teaching_Staff table.
		query ='SELECT Staff_ID, First_Name, Last_Name FROM Teaching_Staff;'

		#Execute the above query with the database object and store the returned information in var result.
		result = execute_query(db_connection, query).fetchall();

		#Create a string object representation of a SELECT query retrieving the Class_ID and Class_Name fof all Classes from the Class table.
		query ='SELECT Class_ID, Class_Name FROM Class;'

		#Execute the above query with the database object and store the returned information in var result2.
		result2 = execute_query(db_connection, query).fetchall();

		#Populate the table in classstaffadd.html template with the values stored in var result and var result2. The values correspond to the variables 'Staff' and 'Classes' respectively in the Jinja template.
		return render_template('classstaffadd.html', Staff = result, Classes = result2)

	#If a POST request was the method by which the page was requested, then the user arrives to this view after having used the forms involved in adding a new Class/Staff Assignment.
	elif request.method == 'POST':

		#Obtain the user supplied values/strings from the forms in the Add Class/Staff Assignment Page and assign them to the correspondingly named variables below.
		Class_ID = request.form['ClassIDInput']

		Staff_ID = request.form['StaffIDInput']

		#Create a string object representation of a INSERT query into the Staff_Class Table.
		query = 'INSERT INTO Staff_Class(Class_ID, Staff_ID) VALUES (%s, %s);'

		#Use the variables containing user input from the forms and store them together as a tuple assigned to var data.
		data = (Class_ID, Staff_ID)

		#Execute the query using the query's string representation, tuple of user supplied data, and the database object. 
		execute_query(db_connection, query, data)

		#Redirect the user back to the '/classstaff' view to show the table that now includes the newly added Class/Staff Assignment.
		return redirect('/classstaff')

