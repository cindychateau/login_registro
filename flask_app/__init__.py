from flask import Flask

app = Flask(__name__) #Inicializamos app

app.secret_key = "Llave super secreta"