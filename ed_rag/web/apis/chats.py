from flask import jsonify
from flask import request

from web.models.Chat import Chat, Message
from ed_rag.rag import AdvancedRAG


def chats_api(app, session):
    
    def add_prompt_and_answer(chat_id, data):
        
        type_of_message = data['type_of_message']
        text = data['text']
        chat = Chat.objects(chat_id=chat_id).first()
        if not chat:
            raise Exception('Chat not found')
        message = Message(type_of_message=type_of_message, text=text, chat_id=chat_id)
        message.save()
        chat.update(push__messages=message)
        return message
    
    @app.route('/chat/create', methods=['POST'])
    def create_chat():
        reuqest_data = request.get_json()
        chat = Chat()
        chat.save()
        return jsonify(chat.to_json())
    
    @app.route('/chats/<chat_id>/', methods=['GET'])
    def get_chat(chat_id):
        if chat_id == 'initial':
            chat = Chat.objects.order_by('-timestamp').first()
        else:
            chat = Chat.objects(chat_id=chat_id).first()
        if not chat:
            return jsonify({'error': 'Chat not found'}), 404
        return jsonify(chat.to_json()), 200
        

    @app.route('/chats/<chat_id>/prompt', methods=['POST'])
    def prompt(chat_id):
        reuqest_data = request.get_json()
        print(reuqest_data)
        model = reuqest_data.get('model')
        prompt = reuqest_data.get('prompt')
        rag = AdvancedRAG(model=model)
        answer = rag.answer_question(prompt)
        prompt = add_prompt_and_answer(chat_id, {'type_of_message': 'user', 'text': prompt})
        answer = add_prompt_and_answer(chat_id, {'type_of_message': 'bot', 'text': answer})
        
        return jsonify(answer.to_json()), 200
    
    @app.route('/chats/<chat_id>/message', methods=['POST'])
    def add_message(chat_id):
        data = request.get_json()
        type_of_message = data.get('type_of_message')
        text = data.get('text')
        chat = Chat.objects(chat_id=chat_id).first()
        if not chat:
            return jsonify({'error': 'Chat not found'}), 404
        message = Message(type_of_message=type_of_message, text=text, chat_id=chat_id)
        message.save()
        chat.update(push__messages=message)
        return jsonify(message.to_json()), 201
    
    @app.route('/add_data', methods=['GET'])
    def add_data():
    

    

    

    

    
        chats = []
    
        messages = [ 
            { 
                "chat_id": "eaa4ca62-f177-4266-873c-00d51ce2d0b2", 
                'message_id': "bb6dccdf-8c10-43ca-9009-78d74de4f921", 
                'text': 'Hello', 
                'timestamp': 1234567890 
            },
            { 
                "chat_id": "eaa4ca62-f177-4266-873c-00d51ce2d0b2", 
                "message_id": "45ed13d6-d058-47f9-8240-831700f23578", 
                'text': 'Hi', 
                'timestamp': 1234567891
            },
            {
                "chat_id": "eaa4ca62-f177-4266-873c-00d51ce2d0b2",
                "message_id": "12460a68-a3e8-4b60-8748-5cc73c3ffa94",
                'text': 'How are you?',
                'timestamp': 1234567892
            },
            {
                "chat_id": "eaa4ca62-f177-4266-873c-00d51ce2d0b2",
                "message_id": "fe0cc4af-50a0-45e5-a04d-258fb4a9c9a1",
                'text': 'I am fine',
                'timestamp': 1234567893
            },
            {
                "chat_id": "eaa4ca62-f177-4266-873c-00d51ce2d0b2",
                "message_id": "4861dbe0-b183-4f1e-886a-a545d5163e5b",
                'text': 'Good to hear',
                'timestamp': 1234567894
            },
            {
                "chat_id": "eaa4ca62-f177-4266-873c-00d51ce2d0b2",
                "message_id": "160aa365-a2e6-4da1-9ec4-ec755d894695",
                'text': 'Goodbye',
                'timestamp': 1234567895
            }
        ]
        
        
