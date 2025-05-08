# notificaciones.py
from flask_restful import Resource
from flask import request, jsonify
from main.models.notificacion_db import Notificacion as NotificacionModel
from .. import db

class Notificaciones(Resource):
    def get(self):
        notificaciones = NotificacionModel.query.all()
        return jsonify([n.to_json() for n in notificaciones])
    
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