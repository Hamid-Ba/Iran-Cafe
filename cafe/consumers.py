# consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer


class OrderConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = "order_group"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        try:
            text_data_json = json.loads(text_data)
            try:
                cafe = text_data_json["cafe"]
                order = text_data_json["order"]
                message = text_data_json["message"]
            except:
                await self.send(text_data=json.dumps({"message": "invalid data"}))
                return
            # Send the cafe message to all clients in the group, excluding the sender
            await self.channel_layer.group_send(
                self.group_name,
                {
                    "type": "order_message",
                    "order": f"{order}",
                    "cafe": f"{cafe}",
                    "message": f"{message}",
                    "client": self.channel_name,
                },
            )
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({"message": "invalid data"}))

    async def order_message(self, event):
        order = event["order"]
        cafe = event["cafe"]
        message = event["message"]
        sender_name = event["client"]

        # Send the cafe message to the current client
        if self.channel_name != sender_name:
            await self.send(text_data=json.dumps({"order": order, "cafe": cafe}))

        if self.channel_name == sender_name:
            await self.send(text_data=json.dumps({"message": message}))


class PagerConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = "pager_group"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        try:
            text_data_json = json.loads(text_data)
            try:
                cafe = text_data_json["cafe"]
            except:
                await self.send(text_data=json.dumps({"message": "invalid data"}))
                return
            # Send the cafe message to all clients in the group, excluding the sender
            await self.channel_layer.group_send(
                self.group_name,
                {
                    "type": "pager_message",
                    "cafe": cafe,
                    "client": self.channel_name,
                },
            )
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({"message": "invalid data"}))

    async def pager_message(self, event):
        cafe = event["cafe"]
        sender_name = event["client"]

        # Send the cafe message to the current client
        if self.channel_name != sender_name:
            await self.send(text_data=json.dumps({"cafe": cafe}))

        if self.channel_name == sender_name:
            await self.send(text_data=json.dumps({"message": "success"}))
