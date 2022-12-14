from crypt import methods
from flask_login import current_user, login_required, login_user
from app import app, db
from flask import render_template, redirect, url_for, request
from flask_login import logout_user
from werkzeug.urls import url_parse
from app.forms import LoginForm, RegistrationForm, CreateTodo, UpdateTodo
from app.models import User, Todo

@app.route('/')
@app.route('/index')
def index():

    return render_template("index.html", title="Dashboard")

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    # Checkiing if the user is authenticated
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()

    # Login form handling. If the user isn't found or the password is wrong
    # The user is returned to the login page
    # TODO show a message to the user if one of the above creteria is wrong
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            return redirect(url_for('signin'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc!='':
            next_page = url_for('dashboard')
        return redirect(next_page)

    return render_template("signin.html", title="signin page", form=form)

@app.route('/signup', methods=['GET','POST'])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password_1.data
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('signin'))

    return render_template("signup.html", title="Create an account", form=form)

@app.route('/logout')
def logout():
    logout_user()
    
    return redirect(url_for('index'))

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    user = User.query.filter_by(username=current_user.username).first()
    todos = Todo.query.filter_by(author=user).all()
    form = CreateTodo()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        todo = Todo(title=title, content=content, author=user)
        db.session.add(todo)
        db.session.commit()
        return redirect(url_for('dashboard'))

    return render_template("dashboard.html", title="Dashboard",\
         username=user.username, form=form, todos=todos)

@app.route('/updatetodo/<todo_id>', methods=['GET', 'POST'])
@login_required
def updatetodo(todo_id):
    user = User.query.filter_by(username=current_user.username).first()
    todo = Todo.query.filter_by(id=todo_id, author=user).first()
    if not todo:
        return redirect(url_for('dashboard'))
    form = UpdateTodo(obj=todo)

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        todo.title = title
        todo.content = content
        db.session.add(todo)
        db.session.commit()
        return redirect(url_for('dashboard'))

    return render_template("updatetodo.html", title="Uodating the Todo", form=form)