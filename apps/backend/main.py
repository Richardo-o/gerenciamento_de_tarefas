import sys
import os

backend_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(backend_dir, 'src')

sys.path.insert(0, backend_dir)
sys.path.insert(0, src_dir)

from app import create_app
from database import db

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
