from .. import db

class Valoracion(db.Model):
    __tablename__ = 'valoracion'
    id = db.Column(db.Integer, primary_key=True)
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=False)
    puntuacion = db.Column(db.Integer, nullable=False)
    comentario = db.Column(db.String(255), nullable=True)
    
    def to_json(self):
        return {
            'id': self.id,
            'producto_id': self.producto_id,
            'puntuacion': self.puntuacion,
            'comentario': str(self.comentario) if self.comentario else ''
        }
    
    @staticmethod
    def from_json(json_data):
        return Valoracion(
            id=json_data.get('id'),
            producto_id=json_data.get('producto_id'),
            puntuacion=json_data.get('puntuacion'),
            comentario=json_data.get('comentario')
        )
