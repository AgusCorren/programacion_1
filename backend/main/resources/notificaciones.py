# notificaciones.py
from flask_restful import Resource
from flask import request, jsonify
from main.models import NotificacionModel
from .. import db

class Notificaciones(Resource):
    def get(self):
        usuario_id = request.args.get('usuario_id', type=int)
        tipo = request.args.get('tipo')

        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=10, type=int)

        query = NotificacionModel.query

        if usuario_id:
            query = query.filter_by(usuario_id=usuario_id)
        if tipo:
            query = query.filter_by(tipo=tipo)

        total = query.count()
        notificaciones = query.offset((page - 1) * per_page).limit(per_page).all()

        return {
            'total': total,
            'page': page,
            'per_page': per_page,
            'total_pages': (total + per_page - 1) // per_page,
            'data': [n.to_json() for n in notificaciones]
        }
    
    def post(self):
        data = request.get_json()
        
        # Validación simple
        if not data or 'usuario_id' not in data or 'mensaje' not in data:
            return {'message': 'usuario_id y mensaje son requeridos'}, 400
            
        try:
            notificacion = NotificacionModel(
                usuario_id=data['usuario_id'],
                mensaje=data['mensaje'],
                tipo=data.get('tipo', 'info'),  # Valor por defecto
                leida=False
            )
            db.session.add(notificacion)
            db.session.commit()
            return notificacion.to_json(), 201
        except Exception as e:
            db.session.rollback()
            return {'message': str(e)}, 500
