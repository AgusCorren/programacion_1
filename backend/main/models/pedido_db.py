from .. import db

class Pedido(db.Model):
    __tablename__ = "pedido"
    id = db.Column(db.Integer, primary_key=True)
    cliente = db.Column(db.String(100), nullable=False)
    producto = db.Column(db.String(100), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    estado = db.Column(db.String(50), default="pendiente")

    def to_json(self):
        return {
            "id": self.id,
            "cliente": self.cliente,
            "producto": self.producto,
            "cantidad": self.cantidad,
            "estado": self.estado
        }