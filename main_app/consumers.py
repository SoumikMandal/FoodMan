import json
from channels.generic.websocket import AsyncWebsocketConsumer

class SupplierConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        supplier_id = self.scope['url_route']['kwargs']['supplier_id']

        self.group_name = f'supplier_{supplier_id}'

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        order_id = data['order_id']
        action = data['action']
        reason = data.get('reason', '')

        if action == 'accept':
            await self.accept_order(order_id)
        elif action == 'reject':
            await self.reject_order(order_id, reason)

    async def accept_order(self, order_id):
        await self.send(text_data=json.dumps({
            'status': 'accepted',
            'order_id': order_id,
            'message': 'Order has been accepted.'
        }))

    async def reject_order(self, order_id, reason):
        await self.send(text_data=json.dumps({
            'status': 'rejected',
            'order_id': order_id,
            'message': f'Order has been rejected. Reason: {reason}'
        }))

    async def order_notification(self, event):
        await self.send(text_data=json.dumps({
            'order': event['order']
        }))
