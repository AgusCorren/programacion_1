from main import create_app
from main import db
from dotenv import load_dotenv
import os

# Cargar variables del .env
load_dotenv()

app = create_app()
app.app_context().push()

# Ejecutar
if __name__ == '__main__':
    db.create_all()
    app.run(debug=True, host='0.0.0.0', port=os.getenv('PORT'))
