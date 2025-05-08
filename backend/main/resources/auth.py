# auth.py
from flask_restful import Resource
from flask import request, jsonify
from main.models.usuario_db import Usuario as UsuarioModel

class Login(Resource):
    def post(self):
        data = request.get_json()
        
        if not data or 'email' not in data or 'password' not in data:
            return {'message': 'Email y password requeridos'}, 400
        
        usuario = UsuarioModel.query.filter_by(email=data['email']).first()
        
        if not usuario:
            return {'message': 'Credenciales inválidas'}, 401
            
        # Comparación directa (sin seguridad para desarrollo)
        if usuario.password_hash != data['password']:
            return {'message': 'Credenciales inválidas'}, 401
            
        return {
            'message': 'Login exitoso',
            'usuario': usuario.to_json()
        }, 200

class Logout(Resource):
    def post(self):
        return {'message': 'Sesión cerrada'}, 200