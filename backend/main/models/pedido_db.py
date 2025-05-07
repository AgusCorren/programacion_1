from .. import db

class Pedido(db.Model):
    __tablename__ = 'pedido'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=True)
    producto = db.Column(db.String(100), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    estado = db.Column(db.String(50), default="pendiente")
    
    # Relación bidireccional: un pedido puede pertenecer a un usuario.
    # Se utiliza back_populates para que esta relación sea simétrica con Usuario.pedidos.
    usuario = db.relationship("Usuario", back_populates="pedidos")

    def to_json(self):
        try:
            return {
                'id': self.id,
                'usuario_id': self.usuario_id,
                'usuario': self.usuario.to_json() if self.usuario else None,
                'producto': str(self.producto),
                'cantidad': self.cantidad,
                'estado': str(self.estado)
            }
        except Exception as e:
            return {'error': 'Error al convertir Pedido a JSON', 'detalle': str(e)}
    
    @staticmethod
    def from_json(json_data):
        try:
            return Pedido(
                id=json_data.get('id'),
                usuario_id=json_data.get('usuario_id'),
                producto=json_data.get('producto'),
                cantidad=json_data.get('cantidad'),
                estado=json_data.get('estado', "pendiente")
            )
        except Exception as e:
            raise ValueError(f"Datos inválidos para Pedido: {str(e)}")
