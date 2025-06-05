from flask_restful import Resource
from flask import request, jsonify, abort
from main.models import ProductoModel, ItemPedidoModel, PedidoModel
#from main.models.pedidos_db import Pedido as PedidoModel
#from main.models.item_pedidos_db import ItemPedidoModel
from .. import db

class Pedidos(Resource):
    def get(self):
        # Soporte para filtrado por usuario_id y estado
        usuario_id = request.args.get('usuario_id', type=int)
        estado = request.args.get('estado')

        # Paginación
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=10, type=int)

        query = PedidoModel.query

        if usuario_id:
            query = query.filter_by(usuario_id=usuario_id)
        if estado:
            query = query.filter_by(estado=estado)

        total = query.count()
        pedidos = query.offset((page - 1) * per_page).limit(per_page).all()

        return {
            'total': total,
            'page': page,
            'per_page': per_page,
            'total_pages': (total + per_page - 1) // per_page,
            'data': [p.to_json() for p in pedidos]
        }

    def post(self):
        json_data = request.get_json(force=True)
        
        # Validaciones
        required_fields = ['usuario_id', 'items']
        missing_fields = [field for field in required_fields if field not in json_data]
        if missing_fields:
            abort(400, description=f"Faltan campos obligatorios: {', '.join(missing_fields)}")
        
        if not isinstance(json_data['items'], list) or len(json_data['items']) == 0:
            abort(400, description="El pedido debe contener al menos un item")
        
        try:
            # Crear pedido
            pedido = PedidoModel(
                usuario_id=json_data['usuario_id'],
                estado='pendiente',
                total=0  # Se calcula abajo
            )
            
            # Agregar items
            total = 0
            for item_data in json_data['items']:
                if not all(k in item_data for k in ['producto_id', 'cantidad']):
                    abort(400, description="Cada item debe tener producto_id y cantidad")
                
                producto = ProductoModel.query.get(item_data['producto_id'])
                if not producto:
                    abort(404, description=f"Producto {item_data['producto_id']} no encontrado")
                
                item = ItemPedidoModel(
                    producto_id=item_data['producto_id'],
                    cantidad=item_data['cantidad'],
                    precio_unitario=producto.precio
                )
                pedido.items.append(item)
                total += item.cantidad * item.precio_unitario
            
            pedido.total = total
            db.session.add(pedido)
            db.session.commit()
            return pedido.to_json(), 201
            
        except Exception as e:
            db.session.rollback()
            abort(500, description=f"Error al crear pedido: {str(e)}")

class Pedido(Resource):
    def get(self, id):
        pedido = PedidoModel.query.get_or_404(id)
        return pedido.to_json()
    
    def put(self, id):
        pedido = PedidoModel.query.get_or_404(id)
        data = request.get_json()
        
        # Solo permitir actualizar estado
        if 'estado' in data:
            estados_validos = ['pendiente', 'preparacion', 'listo', 'entregado', 'cancelado']
            if data['estado'] not in estados_validos:
                abort(400, description=f"Estado inválido. Use: {', '.join(estados_validos)}")
            pedido.estado = data['estado']
        
        try:
            db.session.commit()
            return pedido.to_json()
        except Exception as e:
            db.session.rollback()
            abort(500, description=f"Error al actualizar pedido: {str(e)}")
    
    def delete(self, id):
        pedido = PedidoModel.query.get_or_404(id)
        try:
            db.session.delete(pedido)
            db.session.commit()
            return {'message': 'Pedido eliminado'}, 200
        except Exception as e:
            db.session.rollback()
            abort(500, description=f"Error al eliminar pedido: {str(e)}")