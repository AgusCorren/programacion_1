from flask_restful import Resource
from flask import request, jsonify, abort
from main.models.producto_db import Producto as ProductoModel
from .. import db

class Productos(Resource):
    def get(self):
        # Obtenemos todos los productos de la base de datos.
        productos = ProductoModel.query.all()
        
        # --- Código de prueba antiguo (comentado) ---
        # Este bloque se usaba para devolver datos de ejemplo sin conexión a la base de datos.
        # test_data = [
        #     {'id': 1, 'nombre': 'Producto A', 'descripcion': 'Ejemplo de descripción A', 'precio': 9.99, 'stock': 100},
        #     {'id': 2, 'nombre': 'Producto B', 'descripcion': 'Ejemplo de descripción B', 'precio': 19.99, 'stock': 50}
        # ]
        # return jsonify(test_data)
        # ----------------------------------------------
        
        return jsonify([p.to_json() for p in productos])
    
    def post(self):
        # Se obtiene el JSON de la solicitud
        json_data = request.get_json(force=True)
        
        # --- Validaciones adicionales (comentadas originalmente) ---
        # Se validaba que existieran campos obligatorios.
        # required_fields = ['nombre', 'precio']
        # missing = [field for field in required_fields if field not in json_data]
        # if missing:
        #     return {"error": f"Faltan campos obligatorios: {', '.join(missing)}"}, 400
        # --------------------------------------------------------------
        
        # Validación: los campos 'nombre' y 'precio' son obligatorios.
        required_fields = ['nombre', 'precio']
        missing_fields = [field for field in required_fields if field not in json_data]
        if missing_fields:
            abort(400, description=f"Faltan campos obligatorios: {', '.join(missing_fields)}")
        
        try:
            # Se crea una instancia de Producto utilizando el método from_json del modelo.
            producto = ProductoModel.from_json(json_data)
        except Exception as e:
            abort(500, description=f"Error al convertir JSON a objeto Producto: {str(e)}")
        
        try:
            db.session.add(producto)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(500, description=f"Error al guardar el producto en la base de datos: {str(e)}")
        
        return producto.to_json(), 201

class Producto(Resource):
    def get(self, id):
        # Obtener un producto por su ID; si no existe, se retorna un error 404.
        producto = ProductoModel.query.get_or_404(id)
        return producto.to_json(), 200

    def put(self, id):
        # Actualizar un producto existente.
        producto = ProductoModel.query.get_or_404(id)
        data = request.get_json(force=True)
        
        # --- Código de prueba antiguo (comentado) ---
        # Este bloque se usaba para actualizar productos sin enviar un JSON real.
        # data_example = {
        #     'nombre': 'Producto actualizado',
        #     'descripcion': 'Nueva descripción actualizada',
        #     'precio': 29.99,
        #     'stock': 30
        # }
        # data = data_example
        # ----------------------------------------------
        
        for key, value in data.items():
            setattr(producto, key, value)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(500, description=f"Error al actualizar el producto: {str(e)}")
        return producto.to_json(), 200

    def delete(self, id):
        # Eliminar un producto de la base de datos.
        producto = ProductoModel.query.get_or_404(id)
        try:
            db.session.delete(producto)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(500, description=f"Error al eliminar el producto: {str(e)}")
        return producto.to_json(), 200
