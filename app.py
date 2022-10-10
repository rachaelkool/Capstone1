from flask import Flask, render_template, redirect, session, flash
from sqlalchemy import exc
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, Teacher, Student, Assignment, StudentAssignment
from forms import TeacherRegisterForm, TeacherLoginForm, StudentRegisterForm, StudentLoginForm, AssignmentForm, ScoresForm
import pusher

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///gradebook_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'secretkey'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)

toolbar = DebugToolbarExtension(app)


# ----- General Routes -----

@app.route('/')
def view_options():
    '''Select teacher or student view.'''
    return render_template('view.html')


@app.route('/logout')
def logout():
    '''Logout user.'''
    session.clear()
    flash('Goodbye!', 'primary')
    return redirect('/')

# ----- Teacher Routes -----

@app.route('/teachers/<id>')
def teacher_dashboard(id):
    '''Displays teacher dashboard with list of assignments/ due dates and option to add new assignment.'''
    if 'id' not in session:      
        flash('Please login first!', 'danger')
        return redirect('/teachers/login')
    else:
        teacher = Teacher.query.get(id)
        return render_template('/teacher/teacher_dashboard.html', teacher=teacher)


@app.route('/teachers/register', methods=['GET', 'POST'])
def teacher_register():
    '''Register teacher account.'''
    if 'id' in session:
        return redirect(f"/teachers/{session['id']}")
    form = TeacherRegisterForm()
    if form.validate_on_submit():
        id = form.id.data
        email = form.email.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        new_teacher = Teacher.register(id,email, password, first_name, last_name)

        db.session.add(new_teacher)
        db.session.commit()
        session['id'] = new_teacher.id
        flash('Welcome! Your account was created successfully! Begin adding assignments to create your gradebook.', 'success')
        return redirect(f"/teachers/{new_teacher.id}")

    return render_template('/teacher/teacher_register.html', form=form)


@app.route('/teachers/login', methods=['GET', 'POST'])
def teacher_login():
    '''Login to teacher account.'''
    form = TeacherLoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        teacher = Teacher.authenticate(email, password)
        if teacher:
            flash(f"Welcome Back, {teacher.first_name}!", 'primary')
            session['id'] = teacher.id
            return redirect(f"/teachers/{teacher.id}")
        else:
            form.email.errors = ['Invalid email/password.']

    return render_template('/teacher/teacher_login.html', form=form)

# ----- Student Routes -----

@app.route('/students/<id>')
def student_dashboard(id):
    '''Displays student dashboard with list of assignments/ grades and option to request another attempt on an assignment.'''
    if 'id' not in session:      
        flash('Please login first!', 'danger')
        return redirect('/students/login')
    else:
        student = Student.query.get(id)
        return render_template('student/student_dashboard.html', student=student)


@app.route('/students/register', methods=['GET', 'POST'])
def student_register():
    '''Register student account.'''
    if 'id' in session:
        return redirect(f"/students/{session['id']}")
    form = StudentRegisterForm()
    if form.validate_on_submit():
        id = form.id.data
        email = form.email.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        grade = form.grade.data
        new_student = Student.register(id, email, password, first_name, last_name, grade)

        db.session.add(new_student)
        db.session.commit()
        session['id'] = new_student.id
        flash('Welcome! Your account was created successfully! Your teacher must add you to their gradebook in order to view assignments.', 'success')
        return redirect(f"/students/{new_student.id}")

    return render_template('student/student_register.html', form=form)


@app.route('/students/login', methods=['GET', 'POST'])
def student_login():
    '''Login to teacher account.'''
    form = StudentLoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        student = Student.authenticate(email, password)
        if student:
            flash(f"Welcome Back, {student.first_name}!", 'primary')
            session['id'] = student.id
            return redirect(f"/students/{student.id}")
        else:
            form.email.errors = ['Invalid email/password.']

    return render_template('student/student_login.html', form=form)

# ----- Assignment Routes -----

@app.route('/assignments/<id>')
def assignment_info(id):
    '''Displays all students added to assignment and their scores'''
    if 'id' not in session:      
        flash('Please login first!', 'danger')
        return redirect('/teachers/login')
    else:
        assignment = Assignment.query.get(id)
        return render_template('assignment/assignment.html', assignment=assignment)


@app.route('/teachers/<id>/assignments/add', methods=["GET", "POST"])
def add_assignment(id):
    '''Teacher can create a new assignment and assign it to students.'''
    if 'id' not in session:      
        flash('Please login first!', 'danger')
        return redirect('/teachers/login')
    else:
        teacher = Teacher.query.get(id)
        form = AssignmentForm()
        if form.validate_on_submit():
            name = form.name.data
            due_date = form.due_date.data
            teacher_id = form.teacher_id.data
            students = form.students.data
            new_assignment = Assignment(name=name, due_date=due_date, teacher_id=teacher_id)
            db.session.add(new_assignment)
            db.session.commit()
            for student in students: 
                new_student_assignment = StudentAssignment(assignment_id=new_assignment.id, student_id=student)
                db.session.add(new_student_assignment)

            db.session.commit()
            return redirect(f'/teachers/{teacher_id}')
        else:
            return render_template('assignment/new_assignment.html', form=form, teacher=teacher)


@app.route('/assignments/<id>/edit', methods=["GET", "POST"])
def edit_assignment(id):
    '''Teacher can edit an existing assignment.'''
    if 'id' not in session:      
        flash('Please login first!', 'danger')
        return redirect('/teachers/login')
    else:
        assignment = Assignment.query.get_or_404(id)
        form = AssignmentForm(obj=assignment)
        if form.validate_on_submit():
            assignment.name = form.name.data
            assignment.due_date = form.due_date.data
            assignment.teacher_id = form.teacher_id.data
            assignment.students = form.students.data

            db.session.commit()
            for student in assignment.students: 
                update_assignment = StudentAssignment(assignment_id=assignment.id, student_id=student)
                try:
                    db.session.add(update_assignment)
                    db.session.commit()
                except exc.IntegrityError:
                    db.session.rollback()
               
                    

            db.session.commit()      

            return redirect(f'/teachers/{assignment.teacher_id}')
        else:
            return render_template('assignment/edit_assignment.html', form=form, assignment=assignment)


@app.route('/assignments/<id>/delete', methods=["GET", "POST"])
def delete_assignment(id):
    '''Teacher can delete an assignment.'''
    if 'id' not in session:      
        flash('Please login first!', 'danger')
        return redirect('/teachers/login')
    else:
        assignment = Assignment.query.get_or_404(id)

        assignment_scores = StudentAssignment.query.filter_by(assignment_id=assignment.id).all()
        for score in assignment_scores:
            db.session.delete(score)
        db.session.delete(assignment)
        db.session.commit()
        return redirect(f'/teachers/{assignment.teacher_id}')


@app.route('/assignments/score/<id>/edit', methods=["GET", "POST"])
def edit_score(id):
    '''Teacher can edit student scores on an assignment.'''
    if 'id' not in session:      
        flash('Please login first!', 'danger')
        return redirect('/teachers/login')
    else:
        score = StudentAssignment.query.get_or_404(id)
        form = ScoresForm(obj=score)

        if form.validate_on_submit():
            score.student_id = form.student_id.data
            score.assignment_id = form.assignment_id.data
            score.score = form.score.data
            score.passed = form.passed.data
           
            db.session.commit()
            return redirect(f"/assignments/{score.assignments.id}")
        else:
            return render_template('assignment/edit_assignment_score.html', form=form)

# ----- Notification Route -----

@app.route('/publish/attempt/<id>', methods=['GET', 'POST'])
def attempt(id):
    '''Student can click to request a failed assignment to be reopened. Sends a nofiication to the teacher.'''
    
    pusher_client = pusher.Pusher(
    app_id='1482892',
    key='9baa0a10e519235937c4',
    secret='cf27901637558523012c',
    cluster='us2',
    ssl=True
    )

    student_assignment = StudentAssignment.query.get(id)
    message_body = (f'{student_assignment.students.first_name} {student_assignment.students.last_name} requests another attempt on {student_assignment.assignments.name}')

    pusher_client.trigger('my-channel', 'my-event', {'message': message_body})
    flash('Request sent.', 'primary')
    return redirect(f'/students/{student_assignment.students.id}')