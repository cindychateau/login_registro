from flask_app.config.mysqlconnection import connectToMySQL

from flask import flash #flash es el encargado de mostrar mensaje/errores

import re #Importando expresiones regulares
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') #Expresion regular de email

class User:

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    #Validar todos los datos del usuario
    @staticmethod
    def valida_usuario(formulario):
        #formulario = Diccionario con todos los names y los valores que el usuario va a ingresar
        es_valido = True
        
        #Validar que el nombre del usuario tenga al menos 3 caracteres
        if len(formulario['first_name']) < 3:
            es_valido = False
            flash("Nombre debe de tener al menos 3 caracteres", "registro")
        
        #Validar que el apellido del usuario tenga al menos 3 caracteres
        if len(formulario['last_name']) < 3:
            es_valido = False
            flash("Apellido debe de tener al menos 3 caracteres", "registro")
        
        #Validar que el password tenga al menos 6 caracteres
        if len(formulario['password']) < 6:
            es_valido = False
            flash("Contraseña debe tener al menos 6 caracteres", "registro")
        
        #Verificamos que las contraseñas coincidan
        if formulario['password'] != formulario['confirm_password']:
            es_valido = False
            flash("Contraseñas no coinciden", "registro")
        
        #Revisamos que el email tenga el formato correcto -> Expresiones regulares
        if not EMAIL_REGEX.match(formulario['email']):
            es_valido = False
            flash("E-mail inválido", "registro")
        
        #Consultamos si existe el email
        query = "SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL('login_reg').query_db(query, formulario)
        if len(results) >= 1:
            es_valido = False
            flash("E-mail registrado previamente", "registro")
        
        return es_valido


    #Registramos el usuario
    @classmethod
    def save(cls, formulario):
        #formulario = {first_name: "Elena", last_name:"De Troya", email: "elena@cd.com", password: "jksdnkadh12891312nkldsa"}
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s) "
        result = connectToMySQL('login_reg').query_db(query, formulario)
        return result #el ID del nuevo registro que se realizó
    
    #Función que reciba un diccionario con un correo electrónico y que me regrese si el usuario existe o no
    @classmethod
    def get_by_email(cls, formulario):
        #formulario = {email: elena@codingdojo.com, password: 123}
        query = "SELECT * FROM users WHERE email = %(email)s"
        result = connectToMySQL('login_reg').query_db(query, formulario) #SELECT me regresa una lista
        if len(result) < 1: #Significa que mi lista está vacía, NO existe ese email
            return False
        else:
            #Me regresa una LISTA con un solo registro
            #result = [ 
            #    {id: 1, first_name: Elena, last_name: De Troya .....}  ->POSICION 0
            #] 
            user = cls(result[0]) #Crea una instancia en base a lo que se recibio en la lista
            return user
    
    @classmethod
    def get_by_id(cls, formulario):
        #formulario = {id: 1}
        query = "SELECT * FROM users WHERE id = %(id)s"
        result = connectToMySQL('login_reg').query_db(query, formulario)
        #result = [ 
        #    {id: 1, first_name: Elena, last_name: De Troya .....}  ->POSICION 0
        #] 
        user = cls(result[0]) #Creamos una instancia de usuario
        return user