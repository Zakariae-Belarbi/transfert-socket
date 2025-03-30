# transfert_socket_client.py
import socketio
import os
import logging
import time

# Configuration
sio = socketio.Client()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("CSV-Client")

@sio.event
def connect():
    logger.info("Connecté au serveur")

@sio.event
def csv_response(data):
    if data['status'] == 'success':
        logger.info(f"Succès: {data['message']}")
    else:
        logger.error(f"Erreur: {data['message']}")

@sio.event
def disconnect():
    logger.info("Déconnecté du serveur")

def send_csv():
    try:
        sio.connect('http://localhost:9000')
        
        if not os.path.exists("data.csv"):
            logger.error("Fichier data.csv introuvable")
            return

        with open("data.csv", "r") as blabla:
            csv_data = blabla.read()
        
        logger.info("Envoi du fichier CSV...")
        start_time = time.time()
        sio.emit('csv_upload', csv_data)
        
        # Attendre la réponse
        time.sleep(2)
        logger.info(f"Temps de transfert: {time.time() - start_time:.2f}s")

    except Exception as e:
        logger.error(f"Erreur de connexion: {str(e)}")
    finally:
        sio.disconnect()

if __name__ == '__main__':
    send_csv()