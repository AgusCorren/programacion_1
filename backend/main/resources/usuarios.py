from flask_restful import Resource
from flask import request
from .. import db
from main.models import UsuarioModel

class Usuarios(Resource):
    def get(self):
        usuarios = UsuarioModel.query.all()
        return [u.to_json() for u in usuarios], 200

    def post(self):
        data = request.get_json()

        nuevo_usuario = UsuarioModel(
            nombre=data.get("nombre"),
            email=data.get("email"),
            telefono=data.get("telefono"),
            direccion=data.get("direccion")
        )

        db.session.add(nuevo_usuario)
        db.session.commit()

        return {
            "mensaje": "Usuario creado exitosamente",
            "usuario": nuevo_usuario.to_json()
        }, 201

class Usuario(Resource):
    def get(self, id):
        usuario = UsuarioModel.query.get(id)
        if usuario:
            return usuario.to_json(), 200
        return {"error": "Usuario no encontrado"}, 404

    def put(self, id):
        usuario = UsuarioModel.query.get(id)
        if not usuario:
            return {"error": "Usuario no encontrado"}, 404

        data = request.get_json()
        usuario.nombre = data.get("nombre", usuario.nombre)
        usuario.email = data.get("email", usuario.email)
        usuario.telefono = data.get("telefono", usuario.telefono)
        usuario.direccion = data.get("direccion", usuario.direccion)

        db.session.commit()
        return {"mensaje": f"Usuario {id} editado"}, 200

    def delete(self, id):
        usuario = UsuarioModel.query.get(id)
        if not usuario:
            return {"error": "Usuario no encontrado"}, 404

        db.session.delete(usuario)
        db.session.commit()
        return {"mensaje": f"Usuario {id} eliminado o suspendido"}, 200
