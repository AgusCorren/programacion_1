from .. import db

class Producto(db.Model):
    __tablename__ = 'producto'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(255))
    precio = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)
    
    # Relación: un producto puede tener muchas valoraciones
    valoraciones = db.relationship("Valoracion", backref="producto", lazy=True)

    def to_json(self):
        return {
            'id': self.id,
            'nombre': str(self.nombre),
            'descripcion': str(self.descripcion) if self.descripcion else '',
            'precio': self.precio,
            'stock': self.stock
        }
    
    @staticmethod
    def from_json(json_data):
        return Producto(
            id=json_data.get('id'),
            nombre=json_data.get('nombre'),
            descripcion=json_data.get('descripcion'),
            precio=json_data.get('precio'),
            stock=json_data.get('stock', 0)
        )
