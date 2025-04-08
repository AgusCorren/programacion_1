from flask_restful import Resource
from flask import request
from .. import db
from main.models import ProductoModel

class Productos(Resource):
    def get(self):
        productos = ProductoModel.query.all()
        return [p.to_json() for p in productos], 200

    def post(self):
        data = request.get_json()

        nuevo_producto = ProductoModel(
            nombre=data.get("nombre"),
            descripcion=data.get("descripcion"),
            precio=data.get("precio"),
            stock=data.get("stock", 0)
        )

        db.session.add(nuevo_producto)
        db.session.commit()

        return {
            "mensaje": "Producto creado exitosamente",
            "producto": nuevo_producto.to_json()
        }, 201

class Producto(Resource):
    def get(self, id):
        producto = ProductoModel.query.get(id)
        if producto:
            return producto.to_json(), 200
        return {"error": "Producto no encontrado"}, 404

    def put(self, id):
        producto = ProductoModel.query.get(id)
        if not producto:
            return {"error": "Producto no encontrado"}, 404

        data = request.get_json()
        producto.nombre = data.get("nombre", producto.nombre)
        producto.descripcion = data.get("descripcion", producto.descripcion)
        producto.precio = data.get("precio", producto.precio)
        producto.stock = data.get("stock", producto.stock)

        db.session.commit()
        return {"mensaje": f"Producto {id} editado"}, 200

    def delete(self, id):
        producto = ProductoModel.query.get(id)
        if not producto:
            return {"error": "Producto no encontrado"}, 404

        db.session.delete(producto)
        db.session.commit()
        return {"mensaje": f"Producto {id} eliminado"}, 200
