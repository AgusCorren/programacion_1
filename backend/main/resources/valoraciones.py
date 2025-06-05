from flask_restful import Resource
from flask import request, abort
from main.models import ValoracionModel
from .. import db

class Valoraciones(Resource):
    def get(self):
        try:
            producto_id = request.args.get('producto_id', type=int)
            page = request.args.get('page', default=1, type=int)
            per_page = request.args.get('per_page', default=10, type=int)

            query = ValoracionModel.query

            if producto_id:
                query = query.filter_by(producto_id=producto_id)

            total = query.count()
            valoraciones = query.offset((page - 1) * per_page).limit(per_page).all()

            return {
                'total': total,
                'page': page,
                'per_page': per_page,
                'total_pages': (total + per_page - 1) // per_page,
                'data': [v.to_json() for v in valoraciones]
            }, 200
        except Exception as e:
            abort(500, description=str(e))

    def post(self):
        json_data = request.get_json(force=True)

        # Campos obligatorios
        required_fields = ['producto_id', 'usuario_id', 'puntuacion']
        missing_fields = [field for field in required_fields if field not in json_data]
        if missing_fields:
            abort(400, description=f"Faltan campos obligatorios: {', '.join(missing_fields)}")

        # Validar rango de puntuación
        if not (1 <= json_data['puntuacion'] <= 5):
            abort(400, description="La puntuación debe estar entre 1 y 5")

        try:
            valoracion = ValoracionModel.from_json(json_data)
        except Exception as e:
            abort(500, description=f"Error al convertir JSON a objeto Valoracion: {str(e)}")

        try:
            db.session.add(valoracion)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(500, description=f"Error al guardar la valoración en la base de datos: {str(e)}")

        return valoracion.to_json(), 201
