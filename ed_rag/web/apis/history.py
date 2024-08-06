
from flask import jsonify
from web.models.Chat import Chat

def history_api(app, session):

    @app.route('/history', methods=['get'])
    def get_history():
        chats = Chat.objects()
        return jsonify([chat.to_history() for chat in chats]), 200