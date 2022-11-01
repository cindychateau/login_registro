from flask import render_template, redirect, request, session, flash
from flask_app import app

#Importamos Modelo
from flask_app.models.users import User

#Importación de BCrypt
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    #Validamos la info que recibimos
    if not User.valida_usuario(request.form):
        return redirect('/')
    
    #Encriptar mi contraseña
    pwd = bcrypt.generate_password_hash(request.form['password'])

    #Creamos un diccionario con todos los datos del request.form
    formulario = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pwd
    }

    id = User.save(formulario) #Recibiendo el id del nuevo usuario registrado

    session['user_id'] = id

    return redirect('/dashboard')

@app.route('/login', methods=['POST'])
def login():
    #Verificar que existe el email en nuestra Base de Datos
    user = User.get_by_email(request.form) #2 opciones. 1.- Nos regrese False. 2.- Nos regresa el usuario

    if not user: #variable user = False
        flash('E-mail no encontrado', 'inicio_sesion')
        return redirect('/')
    
    #user = una instancia con todos los datos mi usuario
    #bcrypt.check_password_hash(PASSWORD ENCRIPTADO, PASSWORD SIN ENCRIPTAR) ->True si sí coinciden, False si no coinciden
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash('Password incorrecto', 'inicio_sesion')
        return redirect('/')
    
    session['user_id'] = user.id #Guardando en sesión el id del usuario
    return redirect('/dashboard')


@app.route('/dashboard')
def dashboard():
    #Verifico que exista user_id en sesión
    if 'user_id' not in session:
        return redirect('/')

    #Yo sé que en sesión tengo guardado el id del usuario que inició sesión -> session['user_id']
    #Queremos que en base a la función get_by_id, mandemos un diccionario con el id y nos regrese el usuario
    formulario = {"id": session['user_id']} #Diccionario con los datos del id que queremos
    user = User.get_by_id(formulario)

    return render_template('dashboard.html', user=user)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')