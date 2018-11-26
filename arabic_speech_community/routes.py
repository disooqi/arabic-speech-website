import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from . import app, bcrypt, db
from .forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from .models import User, Post
from flask_login import login_user, current_user, logout_user, login_required


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


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(fullname=form.fullname.data, username=form.username.data, email=form.email.data,
                    password=hashed_password)
        db.session.add(user)
        try:
            db.session.commit()
            flash(f'Account is created for {form.username.data}!', 'success')
            return redirect(url_for('login'))
        except:
            db.session.rollback()
            flash(f'Error while create account for {form.username.data}!, try again later', 'danger')

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


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, picture_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + picture_ext
    picture_path = os.path.join(app.root_path, 'static', 'images', 'profile_pcs', picture_fn)

    image_resize_to = (300, 360)
    i = Image.open(form_picture)
    i.thumbnail(image_resize_to)
    i.save(picture_path)

    return picture_fn


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    image_file = current_user.image_file
    image_path = url_for('static', filename=f'images/profile_pcs/{image_file}')
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.fullname = form.fullname.data
        current_user.position = form.position.data
        current_user.institution = form.affiliation.data
        current_user.department = form.department.data
        db.session.commit()
        flash('Your account has been updated successfully', 'success')
        return redirect(url_for('account')) # for the "POST GET REDIRECT pattern" problem
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.fullname.data = current_user.fullname
        form.email.data = current_user.email
        form.position.data = current_user.position
        form.affiliation.data = current_user.institution
        form.department.data = current_user.department
    else:
        flash('Something wrong with the form', 'warning')
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{field}: {error}", 'danger')

    # image_path = url_for('static', filename=f'images/profile_pcs/citations.jpeg')
    return render_template('account.html', title='Account page', image_path=image_path, form=form)


@app.route('/mgb2')
@login_required
def mgb2():
    return render_template('mgb2.html')


@app.route('/license')
@login_required
def license():
    return render_template('NON-EXCLUSIVE_RESEARCHER_LICENSE_QCRI-AL_JAZEERA_CORPUS.html')


@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post', form=form)