from flask_restful import Resource
from flask import request

class Login(Resource):
    def post(self):
        data = request.get_json()
        username = data.get("username")
        # Acá se puede integrar validación contra la base de datos; por ahora se retorna un mensaje simple.
        return {"mensaje": "Login exitoso", "usuario": username}, 200

class Logout(Resource):
    def post(self):
        return {"mensaje": "Sesión cerrada correctamente"}, 200
