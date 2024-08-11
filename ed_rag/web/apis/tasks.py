from celery import Celery
import os
import logging
from flask_socketio import SocketIO
from ed_rag.trainer import Trainer
import multiprocessing

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("tasks")

# Set the start method to 'spawn' if running on macOS
multiprocessing.set_start_method('spawn', force=True)

celery = Celery('tasks', broker='redis://localhost:6379/0')

@celery.task
def task_complete(result, filenames):
    logger.info(f"Task complete: {result}")
    socket = SocketIO(message_queue='redis://localhost:6379/0')
    socket.emit('training_complete', {'message': 'Training complete for files: {}'.format(", ".join(filenames))})
    

@celery.task
def train_model(filenames):
    logger.info(os.getcwd())
    logger.info("Training started")
    for filename in filenames:
        filepath = os.path.join('data', filename)
        logger.info(f"Processing file: {filepath}")
        trainer = Trainer(filepath)
        trainer.train()
    logger.info('Training completed train_model')
    return "Training completed"
