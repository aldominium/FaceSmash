from flask import (Flask, g, render_template, flash, url_for, redirect)
from flask_bcrypt import check_password_hash
from flask_login import (LoginManager, login_user, login_required, current_user,
                        logout_user)

import models
import forms

DEBUG = True
PORT = 8000
HOST = '0.0.0.0'

app = Flask(__name__)
app.secret_key = 'ASFDXCYE!lfasdasd'';nljnAFON,.ASDOJJNLwuhebjlks23451'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None


@app.before_request
def before_request():
    """Conecta a la base de Datos antes de cada request"""
    g.db = models.DATABASE
    if g.db.is_closed():
        g.db.connect()
        g.user = current_user


@app.after_request
def after_request(response):
    """Cerramos la conexión a la BD"""
    g.db.close()
    return response




@app.route('/register', methods=('GET', 'POST'))
def register():
    form = forms.RegisterForm()
    if form.validate_on_submit():
        flash('Fuiste Registrado!!!', 'success')
        models.User.create_user(
            username = form.username.data,
            email = form.email.data,
            password= form.password.data
        )
        return redirect(url_for('index'))
    return render_template('register.html', form=form)


@app.route('/login', methods=('GET', 'POST'))
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.email == form.email.data)
        except models.DoesNotExist:
            flash('Tu nombre de usuario o contraseña no existe', 'error')
        else:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash('Has iniciado sesión', 'success')
                return redirect(url_for('index'))
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has salido de FaceSmash!', 'success')
    return redirect(url_for('index'))


@app.route('/new_post', methods=('GET', 'POST'))
def post():
    form = forms.PostForm()
    if form.validate_on_submit():
        models.Post.create(user=g.user._get_current_object(),
                           content=form.content.data.strip())
        flash('Mensaje Posteado!', 'success')
        return redirect(url_for('index'))
    return render_template('post.html', form=form)


@app.route('/')
def index():
    return  'Hey'


if __name__ == '__main__':
    models.initialize()
    models.User.create_user(
        username='aldo',
        email='aldo1314@hotmail.com',
        password='aldo1314',
    )
    app.run(debug=DEBUG, host=HOST, port=PORT)
