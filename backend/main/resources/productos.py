from flask_restful import Resource
from flask import request, jsonify, abort
from main.models.producto_db import Producto as ProductoModel
from .. import db

class Productos(Resource):
    def get(self):
        categoria = request.args.get('categoria')
        query = ProductoModel.query
        
        if categoria:
            query = query.filter_by(categoria=categoria)
        
        return jsonify([p.to_json() for p in query.all()])
    
    def post(self):
        data = request.get_json()
        required = ['nombre', 'precio', 'categoria']
        missing = [f for f in required if f not in data]
        if missing:
            abort(400, description=f"Faltan campos: {', '.join(missing)}")
        
        if data['precio'] <= 0:
            abort(400, description="El precio debe ser mayor a 0")
        
        try:
            producto = ProductoModel.from_json(data)
            db.session.add(producto)
            db.session.commit()
            return producto.to_json(), 201
        except Exception as e:
            db.session.rollback()
            abort(500, description=f"Error al crear producto: {str(e)}")

class Producto(Resource):
    def get(self, id):
        producto = ProductoModel.query.get_or_404(id)
        return producto.to_json()
    
    def put(self, id):
        producto = ProductoModel.query.get_or_404(id)
        data = request.get_json()
        
        if 'precio' in data and data['precio'] <= 0:
            abort(400, description="El precio debe ser mayor a 0")
        
        for key, value in data.items():
            if hasattr(producto, key):
                setattr(producto, key, value)
        
        try:
            db.session.commit()
            return producto.to_json()
        except Exception as e:
            db.session.rollback()
            abort(500, description=f"Error al actualizar producto: {str(e)}")
    
    def delete(self, id):
        producto = ProductoModel.query.get_or_404(id)
        try:
            db.session.delete(producto)
            db.session.commit()
            return {'message': 'Producto eliminado'}, 200
        except Exception as e:
            db.session.rollback()
            abort(500, description=f"Error al eliminar producto: {str(e)}")