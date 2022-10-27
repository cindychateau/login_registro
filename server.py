from flask_app import app

#Importamos nuestros controladores
from flask_app.controllers import users_controller

#Ejecutamos aplicación
if __name__ == "__main__":
    app.run(debug=True)