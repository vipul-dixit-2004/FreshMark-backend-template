import os
from app import create_app

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Use 'PORT', not 'FLASK_RUN_PORT' for Render
    app.run(host='0.0.0.0', port=port)

