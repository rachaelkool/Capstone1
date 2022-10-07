from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, DateField, IntegerField, BooleanField, HiddenField, SelectMultipleField
from wtforms.validators import InputRequired, Length


classlist = [('1001', '1001- John Jenkins'), ('1002', '1002- Barbara Jones')]

class TeacherRegisterForm(FlaskForm):
    '''Teacher register account form.'''
    id = IntegerField('Teacher ID #', validators=[InputRequired()], render_kw={"placeholder": '###'})
    email = StringField('Email', validators=[InputRequired(), Length(max=50)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6, max=55)])
    email = StringField('Email', validators=[InputRequired(), Length(max=50)])
    first_name = StringField('First Name', validators=[InputRequired(), Length(max=30)])
    last_name = StringField('Last Name', validators=[InputRequired(), Length(max=30)])


class TeacherLoginForm(FlaskForm):
    '''Teacher login form.'''
    email = StringField('Email', validators=[InputRequired(), Length(max=50)])
    password = PasswordField('Password',validators=[InputRequired(), Length(min=6, max=55)])


class StudentRegisterForm(FlaskForm):
    '''Student register account form.'''
    id = IntegerField('Student ID #', validators=[InputRequired()], render_kw={"placeholder": '####'})
    email = StringField('Email', validators=[InputRequired(), Length(max=50)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6, max=55)])
    email = StringField('Email', validators=[InputRequired(), Length(max=50)])
    first_name = StringField('First Name', validators=[InputRequired(), Length(max=30)])
    last_name = StringField('Last Name', validators=[InputRequired(), Length(max=30)])
    grade = SelectField('Grade', choices=[('9', '9th'), ('10', '10th'), ('11', '11th'), ('12', '12th')])


class StudentLoginForm(FlaskForm):
    '''Student login form.'''
    email = StringField('Email', validators=[InputRequired(), Length(max=50)])
    password = PasswordField('Password',validators=[InputRequired(), Length(min=6, max=55)])


class AssignmentForm(FlaskForm):
    '''Teacher create an assignment form.'''
    name = StringField('Name', validators=[InputRequired(), Length(max=50)])
    due_date = DateField('Due Date', render_kw={"placeholder": 'YYYY-MM-DD'})
    students = SelectMultipleField(choices=classlist, default=['1001', '1002'])
    teacher_id = IntegerField('Enter Teacher ID to confirm new assignment creation', render_kw={"placeholder": '###'})
    
    
class ScoresForm(FlaskForm):
    '''Teacher update a student score form.'''
    student_id = HiddenField('StudentID')
    assignment_id = HiddenField('AssignmentID')
    score = IntegerField('Score', render_kw={"placeholder": '0'})  
    passed = BooleanField('Passed')