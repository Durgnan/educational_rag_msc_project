import os
from celery import Celery
from flask_socketio import SocketIO, emit
from flask import jsonify, request
from werkzeug.utils import secure_filename
from ed_rag.trainer import Trainer
from web.apis.tasks import train_model, task_complete

def trainer_api(app, session, socketio):
    app.config['UPLOAD_FOLDER'] = 'data/'
    
    @app.route('/upload', methods=['POST'])
    def upload_file():
        if 'files' not in request.files:
            return jsonify({"error": "No files part"}), 400

        files = request.files.getlist('files')
        if len(files) == 0:
            return jsonify({"error": "No selected files"}), 400
        
        filenames = []
        for file in files:
            if file.filename == '':
                return jsonify({"error": "One of the files has no selected file"}), 400

            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            filenames.append(filename)
        
        task = train_model.apply_async(args=[filenames], link=task_complete.s(filenames))

        return jsonify({"task_id": task.id}), 202
    
    @app.route('/status/<task_id>', methods=['GET'])
    def upload_status(task_id):
        task = train_model.AsyncResult(task_id)
        response = {
        'state': task.state,
        'result': task.result
        }
        return jsonify(response)
    
    @socketio.on('connect')
    def handle_connect():
        print('Client connected')

    @socketio.on('disconnect')
    def handle_disconnect():
        print('Client disconnected')