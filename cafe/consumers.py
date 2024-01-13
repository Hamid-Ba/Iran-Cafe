# consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer


class OrderConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        cafe_id = self.scope["url_route"]["kwargs"]["cafe_id"]
        self.cafe_group_name = f"cafe_{cafe_id}"

        await self.channel_layer.group_add(self.cafe_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.cafe_group_name, self.channel_name)

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

            # Broadcast the message to all channels in the group
            await self.channel_layer.group_send(
                self.cafe_group_name,
                {
                    "type": "order_message",
                    "cafe": cafe,
                    "order": order,
                    "message": message,
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
        cafe_id = self.scope["url_route"]["kwargs"]["cafe_id"]
        self.cafe_group_name = f"cafe_{cafe_id}"

        await self.channel_layer.group_add(self.cafe_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.cafe_group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        try:
            text_data_json = json.loads(text_data)
            try:
                cafe = text_data_json["cafe"]
                table = text_data_json["table"]
            except:
                await self.send(text_data=json.dumps({"message": "invalid data"}))
                return

            # Broadcast the message to all channels in the group
            await self.channel_layer.group_send(
                self.cafe_group_name,
                {
                    "type": "pager_message",
                    "cafe": cafe,
                    "table": table,
                    "client": self.channel_name,
                },
            )

        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({"message": "invalid data"}))

    async def pager_message(self, event):
        cafe = event["cafe"]
        table = event["table"]
        sender_name = event["client"]

        # Send the cafe message to the current client
        if self.channel_name != sender_name:
            await self.send(text_data=json.dumps({"cafe": cafe, "table": table}))

        if self.channel_name == sender_name:
            await self.send(text_data=json.dumps({"message": "success"}))
