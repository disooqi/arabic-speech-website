from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, RadioField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from .models import User


class RegistrationForm(FlaskForm):
    fullname = StringField('Full name', validators=[DataRequired(), Length(min=1, max=50)])
    email = StringField('Email address', validators=[DataRequired(), Email()])
    
    # password = PasswordField('Password', validators=[DataRequired()])
    # confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo("password")])

    position = StringField('Position/Title', validators=[DataRequired(), Length(max=100)])
    affiliation = StringField('Affiliation', validators=[DataRequired(), Length(max=120)])
    department = StringField('Department/Group', validators=[DataRequired(), Length(max=120)])
    address = StringField('Postal address', validators=[DataRequired(), Length(max=200)])

    telephone = StringField('Telephone number', validators=[DataRequired(), Length(max=15)])
    
    submit = SubmitField('Create Account')

    def validate_field(self, field):
        if True:
            raise ValidationError('Validation Message')

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
    fullname = StringField('Full name', validators=[DataRequired(), Length(min=1, max=50)])
    email = StringField('Email address', validators=[DataRequired(), Email()])

    position = StringField('Position/Title', validators=[DataRequired(), Length(max=100)])
    affiliation = StringField('Affiliation', validators=[DataRequired(), Length(max=120)])
    department = StringField('Department/Group', validators=[DataRequired(), Length(max=120)])
    address = StringField('Postal address', validators=[DataRequired(), Length(max=200)])

    telephone = StringField('Telephone number', validators=[DataRequired(), Length(max=15)])
    
    submit = SubmitField('Update Account')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError(f'The email "{email.data}" is already exist.')


class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])

    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError(f'No Account is associated with email "{email.data}", '
                                  f'you may want to register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo("password")])

    submit = SubmitField('Reset Password')


class RequestMGB2Form(FlaskForm):
    submit = SubmitField('I Accept and Send me download links')

