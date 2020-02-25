import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("connected")
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        print("Room group name", self.room_group_name)
        print("Channel name", self.channel_name)

        # JOIN ROOM GROUP
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, code):
        print("disconnected", code)

        # LEAVE ROOM GROUP
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # RECEIVE MESSAGE FROM WEBSOCKET
    async def receive(self, text_data):
        print("received", text_data)
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # SEND MESSAGE TO ROOM GROUP
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # RECEIVE MESSAGE FROM ROOM GROUP
    async def chat_message(self, event):
        print("CHAT MESSAGE")
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
