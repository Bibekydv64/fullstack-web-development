from flask import Flask, render_template,request,url_for,redirect
from flask_mysqldb import MySQL

app = Flask(__name__)

app.secret_key ='bibekkey'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_PASSWORD'] =''
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_DB'] = 'student_managment_system_database'

conn = MySQL(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/admin-login', methods=['GET','POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if email == 'bibek@12':
            if password == 'bibek':
                return redirect(url_for('admin_dashboard'))
            else:
                return 'Invalid Password! try again'
        else:
            return 'invalid name! try agin'
        
    return render_template('login_admin/login-admin.html')



@app.route('/admin-dashboard')
def admin_dashboard():

    with conn.connection.cursor() as cursor:
    
            fetch_data_from_database_quary = '''
                                            SELECT student_ID,name,age,email,cources
                                            FROM `student-table`
                                            '''
    
            cursor.execute(fetch_data_from_database_quary)
            student_info = cursor.fetchall()

            conn.connection.commit()


    return render_template('dashboard_page/dashboard.html',student_info=student_info)




@app.route('/add-student',methods=['GET','POST'])
def add_student():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        age = request.form.get('age', type=int)
        cources = request.form.get('cources')

        if not name or not email or age is None or age < 1 or not cources:
            return 'Name, email, a valid age, and course are required.', 400

        with conn.connection.cursor() as cursor:

            table_creation = '''
                        CREATE TABLE IF NOT EXISTS `student-table`(
                        student_ID INTEGER AUTO_INCREMENT UNIQUE NOT NULL PRIMARY KEY,
                        name VARCHAR(256) NOT NULL,
                        age INTEGER NOT NULL,
                        email VARCHAR(256) NOT NULL,
                        cources VARCHAR(256) NOT NULL
                        )'''
            
            cursor.execute(table_creation)
    
            insert_data_on_table = '''
                                INSERT INTO `student-table`(
                                name,age,email,cources)
                                VALUES( %s, %s, %s, %s)
                                '''
            values = (name, age, email, cources)

            cursor.execute(insert_data_on_table,values)

            conn.connection.commit()
        return redirect(url_for('add_student'))
    return render_template('dashboard_page/add-student.html')



@app.route('/all-student')
def all_student():
    
    with conn.connection.cursor() as cursor:

        fetch_data_from_database_quary = '''
                                        SELECT student_ID, name,cources
                                        FROM `student-table`
                                        '''

        cursor.execute(fetch_data_from_database_quary)
        student_info = cursor.fetchall()
        conn.connection.commit()
    return render_template('dashboard_page/all-student.html', student_info=student_info)



@app.route('/view-profile')
def view_profile():
    with conn.connection.cursor() as cursor:
        student_IDs = request.args.get('student_ID')
        fetch_data_from_database_quary1 ='''
                                    SELECT *
                                    FROM `student-table`
                                    WHERE student_ID = %s
                                    '''

        cursor.execute(fetch_data_from_database_quary1,(student_IDs,) )

        single_student_info = cursor.fetchall()

    return render_template('dashboard_page/view_profile.html',single_student_info=single_student_info)

@app.route('/delete-student')
def delete_student():
    
    return render_template('dashboard_page/delete-student.html')

@app.route('/delete-student1')
def delete_student1():
    with conn.connection.cursor() as cursor:
        student_IDs = request.args.get('student_ID', type=int)
    
        fetch_data_from_database_quary = '''
                                    DELETE FROM `student-table`
                                    WHERE student_ID =%s
                                    '''
    
        cursor.execute(fetch_data_from_database_quary,(student_IDs,) )
        conn.connection.commit()
        return redirect(url_for('all_student'))
        
    
    return render_template('dashboard_page/delete-student.html')

if __name__ == "__main__":
    app.run(debug=True)
