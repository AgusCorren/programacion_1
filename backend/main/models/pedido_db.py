from .. import db

class Pedido(db.Model):
    __tablename__ = 'pedido'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=True)
    producto = db.Column(db.String(100), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    estado = db.Column(db.String(50), default="pendiente")
    
    def to_json(self):
        return {
            'id': self.id,
            'usuario_id': self.usuario_id,
            'producto': str(self.producto),
            'cantidad': self.cantidad,
            'estado': str(self.estado)
        }
    
    @staticmethod
    def from_json(json_data):
        return Pedido(
            id=json_data.get('id'),
            usuario_id=json_data.get('usuario_id'),
            producto=json_data.get('producto'),
            cantidad=json_data.get('cantidad'),
            estado=json_data.get('estado', "pendiente")
        )
