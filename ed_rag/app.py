from dotenv import load_dotenv
from web.apis.history import history_api
from web.apis.upload import trainer_api
from web.apis.healthcheck import healthcheck_api
from web.apis.chats import chats_api
from web.apis.db.session import connect_db
from flask_socketio import SocketIO


from web.core import app

load_dotenv()
db = connect_db()
socketio = SocketIO()
socketio.init_app(app, message_queue='redis://localhost:6379/0', cors_allowed_origins='*')
for route in [history_api, healthcheck_api, chats_api]:
    route(app, db)

trainer_api(app, db, socketio)

if __name__ == "__main__":
    
    socketio.run(app, host="0.0.0.0", port=8080, debug=True)
    # app.run(host="0.0.0.0", port=8080, debug=True)