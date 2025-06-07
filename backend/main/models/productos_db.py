from .. import db

class Productos(db.Model):
    __tablename__ = 'producto'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(255))
    precio = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)
    
    # Relaciones
    valoraciones = db.relationship('Valoraciones', back_populates='producto', cascade="all, delete-orphan")
    items_pedido = db.relationship('ItemsPedidos', back_populates='producto', cascade='all, delete-orphan')

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
        return Productos(
            id=json_data.get('id'),
            nombre=json_data.get('nombre'),
            descripcion=json_data.get('descripcion'),
            precio=json_data.get('precio'),
            stock=json_data.get('stock', 0)
        )