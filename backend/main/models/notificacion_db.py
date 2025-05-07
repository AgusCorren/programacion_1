from .. import db

class Notificacion(db.Model):
    __tablename__ = 'notificacion'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    mensaje = db.Column(db.String(255), nullable=False)
    leida = db.Column(db.Boolean, default=False)

    # Relación bidireccional: una notificación pertenece a un usuario.
    usuario = db.relationship("Usuario", back_populates="notificaciones", uselist=False)

    def to_json(self):
        try:
            return {
                'id': self.id,
                'usuario_id': self.usuario_id,
                'usuario': self.usuario.to_json() if self.usuario else None,
                'tipo': str(self.tipo),
                'mensaje': str(self.mensaje),
                'leida': self.leida
            }
        except Exception as e:
            return {'error': 'Error al convertir Notificacion a JSON', 'detalle': str(e)}

    @staticmethod
    def from_json(json_data):
        try:
            return Notificacion(
                id=json_data.get('id'),
                usuario_id=json_data.get('usuario_id'),
                tipo=json_data.get('tipo'),
                mensaje=json_data.get('mensaje'),
                leida=json_data.get('leida', False)
            )
        except Exception as e:
            raise ValueError(f"Datos inválidos para Notificacion: {str(e)}")
