from flask_restful import Resource
from flask import request, jsonify, abort
from main.models.valoracion_db import Valoracion as ValoracionModel
from .. import db

class Valoraciones(Resource):
    def get(self):
        # Obtener todas las valoraciones de la base de datos.
        valoraciones = ValoracionModel.query.all()
        
        # --- Código de prueba antiguo (comentado) ---
        # Este bloque se usaba para devolver datos de ejemplo sin conexión a la base de datos.
        #
        # test_data = [
        #     {'id': 1, 'producto_id': 1, 'puntuacion': 5, 'comentario': 'Excelente producto'},
        #     {'id': 2, 'producto_id': 2, 'puntuacion': 3, 'comentario': 'Producto adecuado'}
        # ]
        # return jsonify(test_data)
        # ----------------------------------------------
        
        return jsonify([v.to_json() for v in valoraciones])
    
    def post(self):
        # Obtener el JSON enviado en la solicitud.
        json_data = request.get_json(force=True)
        
        # --- Validaciones adicionales (comentadas originalmente) ---
        # Se validaba que existieran campos obligatorios.
        # required_fields = ['producto_id', 'puntuacion']
        # missing = [field for field in required_fields if field not in json_data]
        # if missing:
        #     return {"error": f"Faltan campos obligatorios: {', '.join(missing)}"}, 400
        # --------------------------------------------------------------
        
        # Validar que los campos obligatorios estén presentes.
        required_fields = ['producto_id', 'puntuacion']
        missing_fields = [field for field in required_fields if field not in json_data]
        if missing_fields:
            abort(400, description=f"Faltan campos obligatorios: {', '.join(missing_fields)}")
        
        try:
            # Crear una nueva instancia de Valoracion utilizando el método from_json del modelo.
            valoracion = ValoracionModel.from_json(json_data)
        except Exception as e:
            abort(500, description=f"Error al convertir JSON a objeto Valoracion: {str(e)}")
        
        try:
            db.session.add(valoracion)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(500, description=f"Error al guardar la valoración en la base de datos: {str(e)}")
        
        # Devolver la valoración creada en formato JSON con código de estado 201 (creado).
        return valoracion.to_json(), 201
