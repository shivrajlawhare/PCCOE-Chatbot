from flask_mysqldb import MySQL

mysql = MySQL()

def init_db(app):
    mysql.init_app(app)

def add_student(data):
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO students (name, email) VALUES (%s, %s)", (data['name'], data['email']))
    mysql.connection.commit()
    cur.close()

def add_parent(data):
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO parents (student_id, name, contact) VALUES (%s, %s, %s)",
                (data['student_id'], data['name'], data['contact']))
    mysql.connection.commit()
    cur.close()

def add_teacher(data):
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO teachers (name, subject) VALUES (%s, %s)", (data['name'], data['subject']))
    mysql.connection.commit()
    cur.close()

def add_holiday(data):
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO holidays (holiday_name, date) VALUES (%s, %s)", (data['holiday_name'], data['date']))
    mysql.connection.commit()
    cur.close()

def get_all(table):
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT * FROM {table}")
    data = cur.fetchall()
    cur.close()
    return data

def get_all_students():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, name FROM students")  # Assuming 'id' is the primary key for students
    data = cur.fetchall()
    cur.close()
    return data

def get_admin_by_username(username):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM admin WHERE username = %s", (username,))
    admin = cur.fetchone()
    cur.close()
    return admin

def get_all(table):
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT * FROM {table}")
    data = cur.fetchall()
    cur.close()
    return data