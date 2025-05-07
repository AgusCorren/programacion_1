from flask_restful import Resource
from flask import request, jsonify, abort
from main.models.notificacion_db import Notificacion as NotificacionModel
from .. import db

class Notificaciones(Resource):
    def get(self):
        # Obtenemos todas las notificaciones de la base de datos.
        notificaciones = NotificacionModel.query.all()
        
        # --- Código de prueba antiguo (comentado) ---
        # Este bloque se usaba para pruebas manuales sin conexión a la base de datos,
        # devolviendo datos estáticos de ejemplo.
        #
        # test_data = [
        #     {'id': 1, 'usuario_id': 1, 'tipo': 'info', 'mensaje': 'Mensaje de prueba', 'leida': False},
        #     {'id': 2, 'usuario_id': 2, 'tipo': 'alerta', 'mensaje': 'Alerta de prueba', 'leida': True}
        # ]
        # return jsonify(test_data)
        # -----------------------------------------------

        return jsonify([n.to_json() for n in notificaciones])
    
    def post(self):
        # Se obtiene el JSON de la solicitud.
        # force=True se utiliza para forzar la interpretación del contenido como JSON.
        json_data = request.get_json(force=True)
        
        # --- Validaciones adicionales (comentadas originalmente) ---
        # Se validaba que existieran ciertos campos obligatorios.
        #
        # required_fields = ['usuario_id', 'tipo', 'mensaje']
        # missing = [field for field in required_fields if field not in json_data]
        # if missing:
        #     return {"error": f"Faltan campos obligatorios: {', '.join(missing)}"}, 400
        # --------------------------------------------------------------

        # Validación: verificar que los campos obligatorios estén presentes.
        required_fields = ['usuario_id', 'tipo', 'mensaje']
        missing_fields = [field for field in required_fields if field not in json_data]
        if missing_fields:
            # En versiones anteriores se retornaba un dict con error, ahora se utiliza abort para simplificar.
            abort(400, description=f"Faltan campos obligatorios: {', '.join(missing_fields)}")
        
        # --- Otra validación de tipo utilizada en pruebas (comentada) ---
        # if not isinstance(json_data.get('usuario_id'), int):
        #     return {"error": "El campo 'usuario_id' debe ser un entero"}, 400
        # ---------------------------------------------------------------
        
        try:
            # Se crea una nueva instancia de Notificacion utilizando el método estático from_json.
            notificacion = NotificacionModel.from_json(json_data)
        except Exception as e:
            # Manejo de error: conversión del JSON a objeto falló.
            # Anteriormente se devolvía un mensaje de error detallado.
            # return {"error": "Error al convertir JSON a objeto Notificacion", "detalle": str(e)}, 500
            abort(500, description=f"Error al convertir JSON a objeto Notificacion: {str(e)}")
        
        try:
            db.session.add(notificacion)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            # Manejo de error: fallo al guardar la notificación en la base de datos.
            # En versiones previas se retornaba un dict con error:
            # return {"error": "Error al guardar la notificación en la base de datos", "detalle": str(e)}, 500
            abort(500, description=f"Error al guardar la notificación en la base de datos: {str(e)}")
        
        # Se retorna la notificación creada en formato JSON, con código de estado 201 (creado).
        return notificacion.to_json(), 201
