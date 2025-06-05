from .. import db

class Pedidos(db.Model):
    __tablename__ = 'pedido'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=True)
    fecha = db.Column(db.DateTime, default=db.func.current_timestamp())
    estado = db.Column(db.String(50), default="pendiente")
    total = db.Column(db.Float, default=0.0)
    
    # Relaciones
    usuario = db.relationship("Usuarios", back_populates="pedidos")
    items = db.relationship("ItemsPedidos", back_populates="pedido", cascade="all, delete-orphan")
    
    def to_json(self):
        return {
            'id': self.id,
            'usuario_id': self.usuario_id,
            'fecha': self.fecha.isoformat() if self.fecha else None,
            'estado': self.estado,
            'total': self.total,
            'items': [item.to_json() for item in self.items]
        }