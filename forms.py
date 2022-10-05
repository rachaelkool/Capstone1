from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, DateField, IntegerField, BooleanField, HiddenField, SelectMultipleField
from wtforms.validators import InputRequired, Length


classlist = [('1001', '1001- John Jenkins'), ('1002', '1002- Barbara Jones')]

class TeacherRegisterForm(FlaskForm):
    id = IntegerField('Teacher ID #', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), Length(max=50)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6, max=55)])
    email = StringField('Email', validators=[InputRequired(), Length(max=50)])
    first_name = StringField('First Name', validators=[InputRequired(), Length(max=30)])
    last_name = StringField('Last Name', validators=[InputRequired(), Length(max=30)])


class TeacherLoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Length(max=50)])
    password = PasswordField('Password',validators=[InputRequired(), Length(min=6, max=55)])


class StudentRegisterForm(FlaskForm):
    id = IntegerField('Student ID #', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), Length(max=50)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6, max=55)])
    email = StringField('Email', validators=[InputRequired(), Length(max=50)])
    first_name = StringField('First Name', validators=[InputRequired(), Length(max=30)])
    last_name = StringField('Last Name', validators=[InputRequired(), Length(max=30)])
    grade = SelectField('Grade', choices=[('9', '9th'), ('10', '10th'), ('11', '11th'), ('12', '12th')])


class StudentLoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Length(max=50)])
    password = PasswordField('Password',validators=[InputRequired(), Length(min=6, max=55)])


class AssignmentForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired(), Length(max=50)])
    due_date = DateField('Due Date')
    teacher_id = IntegerField('Enter Teacher ID to confirm new assignment creation')
    students = SelectMultipleField(choices=classlist, default=['1001', '1002'])
    
    
class ScoresForm(FlaskForm):
    student_id = HiddenField('StudentID')
    assignment_id = HiddenField('AssignmentID')
    score = IntegerField('Score', default=0)  
    passed = BooleanField('Passed')