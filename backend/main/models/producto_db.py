from .. import db

class Producto(db.Model):
    __tablename__ = 'producto'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(255))
    precio = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)
    
    # Relación bidireccional: un producto puede tener muchas valoraciones.
    # Se emplea back_populates para la relación simétrica con Valoracion.producto.
    valoraciones = db.relationship("Valoracion", back_populates="producto", lazy=True)

    def to_json(self):
        try:
            return {
                'id': self.id,
                'nombre': str(self.nombre),
                'descripcion': str(self.descripcion) if self.descripcion else '',
                'precio': self.precio,
                'stock': self.stock,
                'valoraciones': [v.to_json() for v in self.valoraciones]
            }
        except Exception as e:
            return {'error': 'Error al convertir Producto a JSON', 'detalle': str(e)}
    
    @staticmethod
    def from_json(json_data):
        try:
            return Producto(
                id=json_data.get('id'),
                nombre=json_data.get('nombre'),
                descripcion=json_data.get('descripcion'),
                precio=json_data.get('precio'),
                stock=json_data.get('stock', 0)
            )
        except Exception as e:
            raise ValueError(f"Datos inválidos para Producto: {str(e)}")
