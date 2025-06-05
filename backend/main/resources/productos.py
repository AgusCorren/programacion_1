from flask_restful import Resource
from flask import request, jsonify, abort
from main.models import ProductoModel
from .. import db

class Productos(Resource):
    def get(self):
        try:
            # Obtener filtros y paginación
            categoria = request.args.get('categoria')
            page = request.args.get('page', default=1, type=int)
            per_page = request.args.get('per_page', default=10, type=int)

            query = ProductoModel.query

            if categoria:
                query = query.filter_by(categoria=categoria)

            total = query.count()
            productos = query.offset((page - 1) * per_page).limit(per_page).all()

            return {
                'total': total,
                'page': page,
                'per_page': per_page,
                'total_pages': (total + per_page - 1) // per_page,
                'data': [p.to_json() for p in productos]
            }, 200
        except Exception as e:
            abort(500, description=str(e))
    
    def post(self):
        data = request.get_json()
        required = ['nombre', 'precio', 'descripcion']
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