from .. import db

class Usuarios(db.Model):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    telefono = db.Column(db.String(20))
    direccion = db.Column(db.String(255))
    
    # Relaciones
    notificaciones = db.relationship("Notificaciones", back_populates="usuario", cascade="all, delete-orphan")
    pedidos = db.relationship("Pedidos", back_populates="usuario", cascade="all, delete-orphan")
    valoraciones = db.relationship("Valoraciones", back_populates="usuario", cascade="all, delete-orphan")
    
    def to_json(self):
        return {
            'id': self.id,
            'nombre': str(self.nombre),
            'email': str(self.email),
            'telefono': str(self.telefono) if self.telefono else '',
            'direccion': str(self.direccion) if self.direccion else ''
        }
    
    @staticmethod
    def from_json(json_data):
        return Usuarios(
            id=json_data.get('id'),
            nombre=json_data.get('nombre'),
            email=json_data.get('email'),
            telefono=json_data.get('telefono'),
            direccion=json_data.get('direccion')
        )