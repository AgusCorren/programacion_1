from flask_restful import Resource
from flask import request, jsonify, abort
from main.models.usuario_db import Usuario as UsuarioModel
from .. import db

class Usuarios(Resource):
    def get(self):
        try:
            usuarios = UsuarioModel.query.all()
            return jsonify([u.to_json() for u in usuarios])
        except Exception as e:
            abort(500, description=str(e))
    
    def post(self):
        data = request.get_json()
        
        if not data or 'email' not in data or 'nombre' not in data:
            return {'message': 'Nombre y email requeridos'}, 400
            
        if UsuarioModel.query.filter_by(email=data['email']).first():
            return {'message': 'El email ya está registrado'}, 400
            
        try:
            usuario = UsuarioModel(
                nombre=data['nombre'],
                email=data['email'],
                password_hash=data.get('password', '')  # Sin hash por ahora
            )
            db.session.add(usuario)
            db.session.commit()
            return usuario.to_json(), 201
        except Exception as e:
            db.session.rollback()
            abort(500, description=str(e))

class Usuario(Resource):
    def get(self, id):
        usuario = UsuarioModel.query.get_or_404(id)
        return usuario.to_json()
    
    # ... (resto de los métodos sin decoradores JWT)