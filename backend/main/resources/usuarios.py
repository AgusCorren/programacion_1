from flask_restful import Resource
from flask import request, jsonify, abort
from main.models.usuario_db import Usuario as UsuarioModel
from .. import db

class Usuarios(Resource):
    def get(self):
        # Obtener la lista de todos los usuarios desde la base de datos.
        usuarios = UsuarioModel.query.all()
        
        # --- Código de prueba antiguo (comentado) ---
        # Este bloque se usaba para devolver datos de ejemplo sin conexión a la base de datos.
        # test_data = [
        #     {'id': 1, 'nombre': 'Usuario A', 'email': 'usuarioA@ejemplo.com', 'telefono': '123456789', 'direccion': 'Calle Falsa 123'},
        #     {'id': 2, 'nombre': 'Usuario B', 'email': 'usuarioB@ejemplo.com', 'telefono': '987654321', 'direccion': 'Avenida Siempre Viva 742'}
        # ]
        # return jsonify(test_data)
        # ----------------------------------------------
        
        return jsonify([u.to_json() for u in usuarios])
    
    def post(self):
        # Se obtiene el JSON enviado en la solicitud.
        json_data = request.get_json(force=True)
        
        # --- Validaciones adicionales (comentadas originalmente) ---
        # Se validaba la presencia de campos obligatorios.
        # required_fields = ['nombre', 'email']
        # missing = [field for field in required_fields if field not in json_data]
        # if missing:
        #     return {"error": f"Faltan campos obligatorios: {', '.join(missing)}"}, 400
        # --------------------------------------------------------------
        
        required_fields = ['nombre', 'email']
        missing_fields = [field for field in required_fields if field not in json_data]
        if missing_fields:
            abort(400, description=f"Faltan campos obligatorios: {', '.join(missing_fields)}")
        
        try:
            # Se crea una instancia de Usuario utilizando el método from_json del modelo.
            usuario = UsuarioModel.from_json(json_data)
        except Exception as e:
            abort(500, description=f"Error al convertir JSON a objeto Usuario: {str(e)}")
        
        try:
            db.session.add(usuario)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(500, description=f"Error al guardar el usuario en la base de datos: {str(e)}")
        
        return usuario.to_json(), 201

class Usuario(Resource):
    def get(self, id):
        # Obtener un usuario por su ID; si no existe, se retorna un error 404.
        usuario = UsuarioModel.query.get_or_404(id)
        return usuario.to_json(), 200

    def put(self, id):
        # Actualizar un usuario existente.
        usuario = UsuarioModel.query.get_or_404(id)
        data = request.get_json(force=True)
        
        # --- Código de prueba antiguo (comentado) ---
        # Este bloque se usaba para actualizar el usuario sin enviar un JSON real.
        # data_example = {
        #     'nombre': 'Nuevo Nombre',
        #     'email': 'nuevo.email@ejemplo.com',
        #     'telefono': '1122334455',
        #     'direccion': 'Nueva dirección 456'
        # }
        # data = data_example
        # ----------------------------------------------
        
        for key, value in data.items():
            setattr(usuario, key, value)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(500, description=f"Error al actualizar el usuario: {str(e)}")
        return usuario.to_json(), 200

    def delete(self, id):
        # Eliminar un usuario por su ID.
        usuario = UsuarioModel.query.get_or_404(id)
        try:
            db.session.delete(usuario)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(500, description=f"Error al eliminar el usuario: {str(e)}")
        return usuario.to_json(), 200
