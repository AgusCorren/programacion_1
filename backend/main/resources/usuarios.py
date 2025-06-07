from flask_restful import Resource
from flask import request, jsonify, abort
from main.models import UsuarioModel
from .. import db

class Usuarios(Resource):
    def get(self):
        try:
            # Obtener parámetros de paginación
            page = request.args.get('page', default=1, type=int)
            per_page = request.args.get('per_page', default=10, type=int)
            nombre = request.args.get('nombre', type=str)

            query = UsuarioModel.query

            # Filtro opcional por nombre
            if nombre:
                query = query.filter(UsuarioModel.nombre.ilike(f"%{nombre}%"))

            # Total antes de aplicar limit/offset
            total = query.count()

            # Aplicar paginación
            usuarios = query.offset((page - 1) * per_page).limit(per_page).all()

            return {
                'total': total,
                'page': page,
                'per_page': per_page,
                'total_pages': (total + per_page - 1) // per_page,
                'data': [u.to_json() for u in usuarios]
            }, 200

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