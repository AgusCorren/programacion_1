from flask_restful import Resource
from flask import request, jsonify, abort
from main.models.pedido_db import Pedido as PedidoModel
from .. import db

class Pedido(Resource):
    def get(self, id):
        # Obtener un pedido por su ID; si no existe, se retorna un error 404.
        pedido = PedidoModel.query.get_or_404(id)
        return pedido.to_json(), 200

    def put(self, id):
        # Actualizar un pedido existente.
        pedido = PedidoModel.query.get_or_404(id)
        data = request.get_json(force=True)

        # --- Código de prueba antiguo (comentado) ---
        # Este bloque se usaba para pruebas de actualización sin enviar un JSON real.
        # data_example = {
        #     'producto': 'Producto de prueba',
        #     'cantidad': 1,
        #     'estado': 'pendiente'
        # }
        # data = data_example
        # ----------------------------------------------

        for key, value in data.items():
            setattr(pedido, key, value)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(500, description=f"Error al actualizar el pedido: {str(e)}")
        return pedido.to_json(), 200

    def delete(self, id):
        # Eliminar un pedido por su ID.
        pedido = PedidoModel.query.get_or_404(id)
        try:
            db.session.delete(pedido)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(500, description=f"Error al eliminar el pedido: {str(e)}")
        return pedido.to_json(), 200

class Pedidos(Resource):
    def get(self):
        # Obtener la lista de todos los pedidos.
        pedidos = PedidoModel.query.all()
        
        # --- Código de prueba antiguo (comentado) ---
        # Este bloque se usaba para devolver datos de ejemplo sin conexión a la base de datos.
        # test_data = [
        #     {'id': 1, 'producto': 'Producto A', 'cantidad': 2, 'estado': 'pendiente'},
        #     {'id': 2, 'producto': 'Producto B', 'cantidad': 1, 'estado': 'completado'}
        # ]
        # return jsonify(test_data)
        # ----------------------------------------------
        
        return jsonify([p.to_json() for p in pedidos])
    
    def post(self):
        # Crear un nuevo pedido.
        json_data = request.get_json(force=True)
        
        # --- Validaciones adicionales (comentadas originalmente) ---
        # Se validaba que existieran campos obligatorios como 'producto' y 'cantidad'.
        # required_fields = ['producto', 'cantidad']
        # missing = [field for field in required_fields if field not in json_data]
        # if missing:
        #     return {"error": f"Faltan campos obligatorios: {', '.join(missing)}"}, 400
        # --------------------------------------------------------------
        
        required_fields = ['producto', 'cantidad']
        missing_fields = [field for field in required_fields if field not in json_data]
        if missing_fields:
            abort(400, description=f"Faltan campos obligatorios: {', '.join(missing_fields)}")
        
        try:
            pedido = PedidoModel.from_json(json_data)
        except Exception as e:
            abort(500, description=f"Error al convertir JSON a objeto Pedido: {str(e)}")
        
        try:
            db.session.add(pedido)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(500, description=f"Error al guardar el pedido en la base de datos: {str(e)}")
        
        return pedido.to_json(), 201
