from datetime import datetime

from django.core.management.base import BaseCommand
from myapp.models import Order, Client, Product


# Создание ордера: python manage.py order create --client_id 2 --product_id 1 --total_amount 10
# Чтение всех ордеров: python manage.py order read
# Обновление ордера: python manage.py order update --order_id 1 --client_id 2
# Удаление ордера: python manage.py order delete --id 1

class Command(BaseCommand):
    help = 'CRUD operations for the Order model.'

    def add_arguments(self, parser):
        parser.add_argument('action', type=str, help='Specify the action to perform (create, read, update, delete).')
        parser.add_argument('--client_id', type=int, help='ID of the client')
        parser.add_argument('--product_id', type=int, help='ID of the product')
        parser.add_argument('--total_amount', type=float, help='ID of the client')
        parser.add_argument('--order_id', type=int, help='ID of the order')
    def handle(self, *args, **kwargs):
        action = kwargs['action']
        client_id = kwargs['client_id']
        product_id = kwargs['product_id']
        total_amount = kwargs['total_amount']
        order_id = kwargs['order_id']

        if action == 'create':
            order_date =  datetime.now().date()
            client = Client.objects.get(pk=client_id)
            product = Product.objects.get(pk=product_id)
            order = Order.objects.create(client=client, total_amount=total_amount,order_date=order_date)
            order.products.set([product])
            self.stdout.write(f'Successfully created Order with ID: {order.id}')

        elif action == 'read':
            orders = Order.objects.all()
            for order in orders:
                self.stdout.write(f'ID: {order.id}, Client: {order.client}, Total Amount: {order.total_amount}, Order Date: {order.order_date}')

        elif action == 'update':
            order = Order.objects.get(id=order_id)
            if kwargs['client_id']:
                client = Client.objects.get(pk=kwargs['client_id'])
                order.client = client
            if kwargs['product_id']:
                product = Product.objects.get(pk=product_id)
                order.products.set([product])
                order.total_amount = kwargs['total_amount']
            if kwargs['total_amount']:
                order.total_amount = kwargs['total_amount']

            order.save()
            self.stdout.write(f'Successfully updated Order with ID: {order.id}')

        elif action == 'delete':
            order = Order.objects.get(id=order_id)
            order.delete()
            self.stdout.write(f'Successfully deleted Order with ID: {order_id}')

        else:
            self.stdout.write('Invalid action. Please specify a valid action (create, read, update, delete).')