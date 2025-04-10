from flask_restful import Resource
from flask import request
from .. import db
from main.models import ValoracionModel

class Valoraciones(Resource):
    def get(self):
        valoraciones = ValoracionModel.query.all()
        return [v.to_json() for v in valoraciones], 200

    def post(self):
        data = request.get_json()

        nueva_valoracion = ValoracionModel(
            producto_id=data.get("producto_id"),
            puntuacion=data.get("puntuacion"),
            comentario=data.get("comentario")
        )

        db.session.add(nueva_valoracion)
        db.session.commit()

        return {
            "mensaje": "Valoración agregada exitosamente",
            "valoracion": nueva_valoracion.to_json()
        }, 201
