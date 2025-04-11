import json
from channels.generic.websocket import AsyncWebsocketConsumer

class QueueConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.doctor_id = self.scope['url_route']['kwargs']['doctor_id']
        self.group_name = f'queue_{self.doctor_id}'

        # Join the doctor's queue group.
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def send_queue_update(self, event):
        # Send the updated queue data to the client.
        message = event['message']
        await self.send(text_data=message)
