from .. import db

class Notificaciones(db.Model):
    __tablename__ = 'notificacion'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    mensaje = db.Column(db.String(255), nullable=False)
    leida = db.Column(db.Boolean, default=False)

    # Relación: muchas notificaciones para un usuario
    usuario = db.relationship('Usuarios', back_populates='notificaciones')

    def to_json(self):
        return {
            'id': self.id,
            'usuario_id': self.usuario_id,
            'tipo': str(self.tipo),
            'mensaje': str(self.mensaje),
            'leida': self.leida
        }
    
    @staticmethod
    def from_json(json_data):
        return Notificaciones(
            id=json_data.get('id'),
            usuario_id=json_data.get('usuario_id'),
            tipo=json_data.get('tipo'),
            mensaje=json_data.get('mensaje'),
            leida=json_data.get('leida', False)
        )