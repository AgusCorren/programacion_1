from .. import db

class Notificacion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    mensaje = db.Column(db.String(255), nullable=False)
    leida = db.Column(db.Boolean, default=False)

    def to_json(self):
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "tipo": self.tipo,
            "mensaje": self.mensaje,
            "leida": self.leida
        }
