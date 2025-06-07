from .. import db

class ItemsPedidos(db.Model):
    __tablename__ = 'item_pedido'
    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedido.id'), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio_unitario = db.Column(db.Float, nullable=False)
    
    # Relaciones
    pedido = db.relationship("Pedidos", back_populates="items")
    producto = db.relationship("Productos", back_populates="items_pedido")
    
    def to_json(self):
        return {
            'id': self.id,
            'producto_id': self.producto_id,
            'cantidad': self.cantidad,
            'precio_unitario': self.precio_unitario,
            'subtotal': self.cantidad * self.precio_unitario
        }