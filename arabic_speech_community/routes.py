import string
import secrets
from datetime import datetime, date
from flask import render_template, url_for, flash, redirect, request, send_from_directory, make_response
from . import app, bcrypt, db, info_mail
from .forms import (RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm,
                    RequestMGB2Form)
from .models import User, MGB2Link
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
        db.session.commit()  # TODO: catch commit exception https://stackoverflow.com/questions/2193670/catching-sqlalchemy-exceptions
        send_confirm_email(user)  # TODO: catch send email exception https://stackoverflow.com/questions/16119746/python-flask-mail-send-error-check-and-log-it
        flash('An email has sent with instructions to confirm your email and complete your registration!', 'info')
        return redirect(url_for('home'))

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
        return redirect(url_for('login'))

    return render_template('reset_token.html', title='Set/Reset Password', form=form)


def send_MGB2_email(user, train_link, test_link, dev_link):
    train_token = train_link.get_MGB2_token()
    test_token = test_link.get_MGB2_token()
    dev_token = dev_link.get_MGB2_token()
    msg = Message('MGB-2 dataset - arabicspeech.org', recipients=[user.email])
    msg.body = f'''Dear {user.fullname},

Thank you for your interest in the Arabic Multi-Dialect Broadcast Media Recognition (MGB-2) corpus. Use the following links to download it:

Training data: wget -c {url_for('mgb2_download', token=train_token, _external=True)} -O train.tar.gz

Development data: wget -c {url_for('mgb2_download', token=dev_token, _external=True)} -O dev.tar.gz

Testing data: wget -c {url_for('mgb2_download', token=test_token, _external=True)} -O test.tar.gz

All the best,
QCRI speech team

'''
    info_mail.send(msg)


@app.route('/mgb2', methods=['POST', 'GET'])
@login_required
def mgb2():
    form = RequestMGB2Form()
    if form.validate_on_submit():
        train_link = MGB2Link(mgb2_part='train', user_id=current_user.id)
        test_link = MGB2Link(mgb2_part='test', user_id=current_user.id)
        dev_link = MGB2Link(mgb2_part='dev', user_id=current_user.id)

        db.session.add(train_link)
        db.session.add(test_link)
        db.session.add(dev_link)

        db.session.commit()

        send_MGB2_email(current_user, train_link, test_link, dev_link)

        flash(f'An email has sent to ({current_user.email}) with instructions to download MGB-2 dataset!', 'info')

    return render_template('mgb2.html', title='MGB 2 Dataset', form=form)


@app.route('/mgb2/<token>', methods=['POST', 'GET'])
def mgb2_download(token):

    mgb2_download_request = MGB2Link.verify_MGB2_token(token)

    if not mgb2_download_request:
        # TODO: think of redirect it to a 404 page
        flash('This is an invalid or expired URL, please generate a new one!', 'warning')
        return redirect(url_for('mgb2'))

    mgb2_download_request.last_date_downloaded = datetime.utcnow()
    mgb2_download_request.n_downloads += 1

    db.session.commit()
    the_response = make_response()

    mgb2_links = {
        'dev':'https://doc-14-8g-docs.googleusercontent.com/docs/securesc/ha0ro937gcuc7l7deffksulhg5h7mbp1/mi7ae7r9rsomh2cjs7cta6hgne4t22n1/1550743200000/07897698524543748950/*/1mWmZiD1GDDW6V2gypK8CP27PaAEFE4mx?e=download',
        'test':'https://doc-0o-8g-docs.googleusercontent.com/docs/securesc/ha0ro937gcuc7l7deffksulhg5h7mbp1/5j76vfr1u77mitdd003ftg4ddmmb50p3/1550743200000/07897698524543748950/*/1RcWVnUJhDmjI5xv759BYJ2wBFaYqPdJk?e=download',
        'train':'https://doc-10-8g-docs.googleusercontent.com/docs/securesc/ha0ro937gcuc7l7deffksulhg5h7mbp1/4bcj79ocne31qj3bmmo2b264qvfh8mq6/1550743200000/07897698524543748950/*/1EVKGtRjZ0To6X9RL1T633ihnbx2oS-wl?e=download'
    }
    # the_response = make_response(send_from_directory('/data/mgb2', f'{mgb2_download_request.mgb2_part}.tar.bz2', as_attachment=True))
    # the_response.headers['Content-Description'] = 'File Transfer'
    # the_response.headers['Content-Disposition'] = f'attachment; filename={mgb2_download_request.mgb2_part}.tar.bz2'
    # the_response.headers['Content-Type'] = 'application/x-tar'
    # the_response.headers['X-Accel-Redirect'] = f'/mgb2/download/{mgb2_download_request.mgb2_part}.tar.bz2'
    #
    # return the_response
    # return send_from_directory('/data/mgb2', f'{mgb2_download_request.mgb2_part}.tar.bz2', as_attachment=True)

    return redirect(mgb2_links[mgb2_download_request.mgb2_part])


