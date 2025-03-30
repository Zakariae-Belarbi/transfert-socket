# transfert_socket_server.py
from flask import Flask
from flask_socketio import SocketIO, emit
import os
import logging

# Configuration
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("CSV-Server")

@socketio.on('csv_upload')
def handle_csv(data):
    try:
        logger.info("Réception de données CSV...")
        
        # Sauvegarder le fichier
        save_path = os.path.join(os.getcwd(), "received_data.csv")
        with open(save_path, "w") as f:
            f.write(data)
        
        logger.info(f"Fichier sauvegardé sous {save_path}")
        emit('csv_response', {'status': 'success', 'message': 'Fichier reçu'})
        
    except Exception as e:
        logger.error(f"Erreur: {str(e)}")
        emit('csv_response', {'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    logger.info("Serveur démarré sur http://localhost:9000")
    socketio.run(app, host='0.0.0.0', port=9000, debug=True)