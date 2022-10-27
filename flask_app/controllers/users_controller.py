from flask import render_template, redirect, request, session
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

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')