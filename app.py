from flask import Flask, render_template, request, redirect, url_for, session, flash
from models import add_student, add_parent, add_teacher, add_holiday, get_all, get_all_students, get_admin_by_username, init_db
from config import Config
from flask_mysqldb import MySQL

app = Flask(__name__, static_folder='static')
app.config.from_object(Config)
init_db(app)

app.secret_key = Config.SECRET_KEY

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query = request.form.get('query').lower()
        if query == 'students':
            students = get_all('students')
            return render_template('chat.html', query=query, result=students, table_headers=['ID', 'Name', 'Email'])
        elif query == 'teachers':
            teachers = get_all('teachers')
            return render_template('chat.html', query=query, result=teachers, table_headers=['ID', 'Name', 'Subject'])
        elif query == 'holidays':
            holidays = get_all('holidays')
            return render_template('chat.html', query=query, result=holidays, table_headers=['ID', 'Holiday Name', 'Date'])
        else:
            message = "I can't understand the query. Please try 'students', 'teachers', or 'holidays'."
            return render_template('chat.html', query=query, message=message)
    return render_template('chat.html')

# Admin Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        admin = get_admin_by_username(username)
        if admin and admin[2] == password:  
            session['admin'] = username
            return render_template('base.html')
        else:
            flash('Wrong credentials. Please try again.', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('login'))

@app.route('/add_student', methods=['GET', 'POST'])
def add_student_route():
    if 'admin' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        data = {
            'name': request.form['name'],
            'email': request.form['email']
        }
        add_student(data)
        return redirect(url_for('add_student_route'))
    
    students = get_all('students')
    return render_template('add_student.html', students=students)

@app.route('/add_parent', methods=['GET', 'POST'])
def add_parent_route():
    if 'admin' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        data = {
            'student_id': request.form['student_id'],
            'name': request.form['name'],
            'contact': request.form['contact']
        }
        add_parent(data)
        return redirect(url_for('add_parent_route'))
    
    parents = get_all('parents')
    students = get_all_students()  
    return render_template('add_parent.html', parents=parents, students=students)

@app.route('/add_teacher', methods=['GET', 'POST'])
def add_teacher_route():
    if 'admin' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        data = {
            'name': request.form['name'],
            'subject': request.form['subject']
        }
        add_teacher(data)
        return redirect(url_for('add_teacher_route'))
    
    teachers = get_all('teachers')
    return render_template('add_teacher.html', teachers=teachers)

@app.route('/add_holiday', methods=['GET', 'POST'])
def add_holiday_route():
    if 'admin' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        data = {
            'holiday_name': request.form['holiday_name'],
            'date': request.form['date']
        }
        add_holiday(data)
        return redirect(url_for('add_holiday_route'))
    
    holidays = get_all('holidays')
    return render_template('add_holiday.html', holidays=holidays)

if __name__ == '__main__':
    app.run(debug=True)
