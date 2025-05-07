from .. import db

class Usuario(db.Model):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    telefono = db.Column(db.String(20))
    direccion = db.Column(db.String(255))
    
    # Relaciones bidireccionales:
    # Un usuario tiene muchas notificaciones y muchos pedidos.
    notificaciones = db.relationship("Notificacion", back_populates="usuario", lazy=True)
    pedidos = db.relationship("Pedido", back_populates="usuario", lazy=True)

    def to_json(self):
        try:
            return {
                'id': self.id,
                'nombre': str(self.nombre),
                'email': str(self.email),
                'telefono': str(self.telefono) if self.telefono else '',
                'direccion': str(self.direccion) if self.direccion else '',
                'notificaciones': [n.to_json() for n in self.notificaciones],
                'pedidos': [p.to_json() for p in self.pedidos]
            }
        except Exception as e:
            return {'error': 'Error al convertir Usuario a JSON', 'detalle': str(e)}
    
    @staticmethod
    def from_json(json_data):
        try:
            return Usuario(
                id=json_data.get('id'),
                nombre=json_data.get('nombre'),
                email=json_data.get('email'),
                telefono=json_data.get('telefono'),
                direccion=json_data.get('direccion')
            )
        except Exception as e:
            raise ValueError(f"Datos inválidos para Usuario: {str(e)}")
