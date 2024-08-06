from mongoengine import Document, StringField, ListField, ReferenceField, CASCADE, DateTimeField, UUIDField
import uuid
import datetime

class Message(Document):
    message_id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False, binary=False)
    chat_id = UUIDField(required=True, binary=False)
    type_of_message = StringField(required=True)
    text = StringField(required=True)
    timestamp = DateTimeField(required=True, default=datetime.datetime.now)
    
    def to_json(self):
        return {
            'message_id': self.message_id,
            'chat_id': self.chat_id,
            'type_of_message': self.type_of_message,
            'text': self.text,
            'timestamp': self.timestamp.isoformat()
        }

class Chat(Document):
    chat_id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False, binary=False, dbref=False)
    title = StringField()
    messages = ListField(ReferenceField(Message, reverse_delete_rule=CASCADE))
    timestamp = DateTimeField(required=True, default=datetime.datetime.now)

    def to_json(self): 
        messages_json = []
        for message in self.messages:
            if isinstance(message, Message):
                messages_json.append(message.to_json())
            else:
                try:
                    dereferenced_message = Message.objects.get(message_id=message.id)
                    messages_json.append(dereferenced_message.to_json())
                except Exception as e:
                    print(f"Error serializing message: {e}")
                    print(f"Message: {message}")
                    continue
        return {
            'chat_id': self.chat_id,
            'title': self.title,
            'messages': messages_json,
            'timestamp': self.timestamp.isoformat()
        }
    
    def to_history(self):
        return {
            'chat_id': self.chat_id,
            'title': self.title,
            'timestamp': self.timestamp.isoformat()
        }