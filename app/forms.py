from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FieldList, DateField, TextAreaField, IntegerField, SelectField
from wtforms.validators import DataRequired, Email, Length, Regexp, ValidationError, NumberRange, Length, Optional
from app.models.track import User

class SignUpForm(FlaskForm):
    # Username field with validators for data required, length between 5 and 20 characters.
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=5, max=20, message='Username must be between 5 and 20 characters.')
    ])
  
    # Email field with validators for data required and email format.
    # IMPORTANT: The check_deliverability=False is for DEBUGGING
    email = StringField('Email', validators=[
        DataRequired(),
        Email(check_deliverability=False),
        Email(message='Invalid email address.')
    ])

    # Password field is required and needs:
    # - Minimum 8 characters
    # - At least one uppercase letter
    # - At least one digit
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, message='Password must be at least 8 characters long.'),
        Regexp(r'^(?=.*[A-Z])(?=.*\d).+$', message='Password must contain at least one uppercase letter and one digit.')
    ])

    # Submit button for the form
    submit = SubmitField('Sign Up')

    # Some validation functions for username and email.
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered.')
        

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
    remember_me = BooleanField('Remember Me')


class EditProfile(FlaskForm):
    user_bio = StringField('Bio', validators=[Length(max=300, message='Bio must be less than 300 characters.')])
    instruments_played = FieldList(StringField('Instrument'), min_entries=1, max_entries=5)
    submit = SubmitField('Update Profile')

from flask_wtf import FlaskForm
from datetime import date

class PracticeSessionForm(FlaskForm):
    instrument = SelectField('Instrument', validators=[DataRequired()], choices=[
        'Piano',
        'Guitar',
        'Violin',
        'Drums',
        'Vocals',
        'Other'
    ])
    
    # Setting default to today's date makes the UX much smoother
    date = DateField('Date', validators=[DataRequired()], default=date.today)
    
    # We split duration into two fields for a better UI
    hours = IntegerField('Hours', validators=[NumberRange(min=0)], default=0)
    minutes = IntegerField('Minutes', validators=[NumberRange(min=0, max=59)], default=0)
    
    notes = TextAreaField('Practice Notes', validators=[Optional(), Length(max=3000)])
    
    submit = SubmitField('Log Session')