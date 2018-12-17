import os
import string
import secrets
from datetime import date
from flask import render_template, url_for, flash, redirect, request
from . import app, bcrypt, db, info_mail
from .forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                    RequestResetForm, ResetPasswordForm)
from .models import User
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message


@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/technologies')
def technologies():
    return render_template('technologies.html', title='Speech Technology')


@app.route('/resources')
def resources():
    return render_template('resources.html', title='Resources')


@app.route('/vacancies')
def vacancies():
    return render_template('vacancies.html', title='Vacancies')


@app.route('/publications')
def publications():
    return render_template('publications.html', title='Publications')


@app.route('/mailinglists')
def mailinglists():
    return render_template('mailinglists.html', title='Mailing lists')


@app.route('/meetings')
def meetings():
    return render_template('meetings.html', title='Meetings')


@app.route('/committee')
def committee():
    return render_template('committee.html', title='Committee')


def generate_random_password():
    char_classes = (string.ascii_lowercase, string.ascii_uppercase, string.digits, string.punctuation)

    s = secrets.choice(range(8, 13))  # Chooses a password length.
    char = lambda: secrets.choice(secrets.choice(
        char_classes))  # Chooses one character, uniformly selected from each of the included character classes.
    print(s)
    return ''.join([char() for _ in range(s)])  # Generates the variable-length password.

def send_confirm_email(user):
    token = user.get_reset_token()
    msg = Message('Email Confirmation - arabicspeech.org',  recipients=[user.email])
    msg.body = f'''A user on "arabicspeech.org" has created an account using this email address.
    
To confirm this email address, go to: {url_for('reset_token', token=token, _external=True)}

If you did not sign up for this site, you can ignore this message.
'''
    info_mail.send(msg)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(generate_random_password()).decode('utf-8')
        user = User(fullname=form.fullname.data, email=form.email.data,
                    password=hashed_password, position=form.position.data,
                    affiliation=form.affiliation.data, department=form.department.data,
                    address=form.address.data, telephone=form.department.data)
        db.session.add(user)
        try:
            db.session.commit()
            send_confirm_email(user)
            flash('An email has sent with instructions to confirm your email and complete your registration!', 'info')
            return redirect(url_for('home'))
        except:
            db.session.rollback()
            flash(f'Error while create account for {form.email.data}!, try again later', 'danger')

    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next', url_for('home'))
            return redirect(next_page)
        else:
            flash('Unsuccessful login, please check Email and/or Password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        
        current_user.fullname = form.fullname.data
        current_user.email = form.email.data

        current_user.position = form.position.data
        current_user.affiliation = form.affiliation.data

        current_user.department = form.department.data
        current_user.address = form.address.data

        current_user.telephone = form.telephone.data
        db.session.commit()
        flash('Your account has been updated successfully', 'success')
        return redirect(url_for('account')) # for the "POST GET REDIRECT pattern" problem
    elif request.method == 'GET':
        form.fullname.data = current_user.fullname
        form.email.data = current_user.email
        
        form.position.data = current_user.position
        form.affiliation.data = current_user.affiliation

        form.department.data = current_user.department
        form.address.data = current_user.address
        form.telephone.data = current_user.telephone
    else:
        flash('Something went wrong with the form', 'warning')
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{field}: {error}", 'danger')

    return render_template('account.html', title='Account page', form=form)


@app.route('/mgb2')
@login_required
def mgb2():
    return render_template('mgb2.html')


@app.route('/license')
@login_required
def license():
    today=date.today().strftime('%A %d %B %Y')
    return render_template('NON-EXCLUSIVE_RESEARCHER_LICENSE_QCRI-AL_JAZEERA_CORPUS.html',today=today)


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    info_mail.send(msg)


@app.route('/reset_password', methods=['POST', 'GET'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has sent with instructions to reset your password!', 'info')
        return redirect(url_for('login'))

    return render_template('reset_request.html', title='Reset Password', form=form)


@app.route('/reset_password/<token>', methods=['POST', 'GET'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    user = User.verify_reset_token(token)

    if not user:
        # TODO: think of redirect it to a 404 page
        flash('This is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Password has been changed successfully', 'success')
        redirect(url_for('login'))

    return render_template('reset_token.html', title='Set/Reset Password', form=form)