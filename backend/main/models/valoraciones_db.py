from .. import db

class Valoraciones(db.Model):
    __tablename__ = 'valoracion'
    id = db.Column(db.Integer, primary_key=True)
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    puntuacion = db.Column(db.Integer, nullable=False)
    comentario = db.Column(db.String(255), nullable=True)

    # Relaciones
    producto = db.relationship("Productos", back_populates="valoraciones")
    usuario = db.relationship("Usuarios", back_populates="valoraciones")

    def to_json(self):
        return {
            'id': self.id,
            'producto_id': self.producto_id,
            'usuario_id': self.usuario_id,
            'puntuacion': self.puntuacion,
            'comentario': str(self.comentario) if self.comentario else ''
        }

    @staticmethod
    def from_json(json_data):
        return Valoraciones(
            id=json_data.get('id'),
            producto_id=json_data.get('producto_id'),
            usuario_id=json_data.get('usuario_id'), 
            puntuacion=json_data.get('puntuacion'),
            comentario=json_data.get('comentario')
        )