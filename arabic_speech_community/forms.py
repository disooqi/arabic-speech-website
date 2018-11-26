from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, RadioField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from .models import User


class RegistrationForm(FlaskForm):
    fullname = StringField('Full name', validators=[DataRequired(), Length(min=10, max=50)])
    username = StringField('Username',
                           validators=[
                               DataRequired(message="Disooqi says its required"),
                               Length(min=5, max=20)
                           ])
    email = StringField('Email address', validators=[DataRequired(), Email()])
    # telephone = StringField('Phone number', validators=[Length(min=8)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField('Create Account')

    def validate_field(self, field):
        if True:
            raise ValidationError('Validation Message')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(f'The user "{username.data}" is already exist.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(f'The email "{email.data}" is already exist.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    fullname = StringField('Full name', validators=[DataRequired(), Length(min=10, max=50)])
    username = StringField('Username',
                           validators=[
                               DataRequired(message="Disooqi says its required"),
                               Length(min=5, max=20)
                           ])
    email = StringField('Email address', validators=[DataRequired(), Email()])
    picture = FileField('Profile picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])

    position = StringField('Position/Title', validators=[Length(max=100)])
    affiliation = StringField('Affiliation', validators=[Length(max=120)])
    department = StringField('Department/Group', validators=[Length(max=120)])
    address = StringField('Postal address', validators=[Length(max=200)])

    telephone = StringField('Telephone number', validators=[Length(max=15)])
    fax = StringField('Fax number', validators=[Length(max=15)])

    submit = SubmitField('Update Account')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(f'The user "{username.data}" is already exist.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError(f'The email "{email.data}" is already exist.')


class MGB2LicenseForm(FlaskForm):
    contribution = RadioField('Are You willing to contribute to the Corpus for future releases?',
                              choices=[('Yes', 'I am definitely contributing to the Corpus.'),
                                       ('No', 'I am definitely not contributing to the Corpus.'),
                                       ('Possibly', 'I didn\'t make my mind yet.')],
                              validators=[DataRequired()]
                              )


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])

    submit = SubmitField('Post')
