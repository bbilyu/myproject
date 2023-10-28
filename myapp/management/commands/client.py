import datetime
from django.core.management.base import BaseCommand
from myapp.models import Client

from django.core.management.base import BaseCommand
from datetime import datetime
from myapp.models import Client


# Создание клиента: python manage.py client create --name John --email john@example.com --phone_number 1234567890 --address New York"
# Чтение всех клиентов: python manage.py client read
# Обновление клиента: python manage.py client update --id 1 --name John Doe
# Удаление клиента: python manage.py client delete --id 1

class Command(BaseCommand):
    help = 'CRUD operations on Client model'

    def add_arguments(self, parser):
        parser.add_argument('action', type=str, help='Action to perform: create, read, update, delete')
        parser.add_argument('--id', type=int, help='ID of the client')
        parser.add_argument('--name', type=str, help='Name of the client')
        parser.add_argument('--email', type=str, help='Email of the client')
        parser.add_argument('--phone_number', type=str, help='Phone number of the client')
        parser.add_argument('--address', type=str, help='Address of the client')

    def handle(self, *args, **kwargs):
        client_id = kwargs['id']
        action = kwargs['action']
        name = kwargs['name']
        email = kwargs['email']
        phone_number = kwargs['phone_number']
        address = kwargs['address']
        if action == 'create':
            registration_date = datetime.now().date()
            client = Client.objects.create(name=name, email=email, phone_number=phone_number, address=address,
                                           registration_date=registration_date)
            self.stdout.write(self.style.SUCCESS(f'Successfully created client: {client.id}'))
        elif action == 'read':
            clients = Client.objects.all()
            for client in clients:
                self.stdout.write(
                    f'-\nClient ID: {client.id}\nName: {client.name}\nEmail: {client.email}\nPhone Number: {client.phone_number}\nAddress: {client.address}\nRegistration Date: {client.registration_date}\n')
        elif action == 'update':
            try:
                client = Client.objects.get(pk=client_id)
                if kwargs['name']:
                    client.name = kwargs['name']
                if kwargs['email']:
                    client.email = kwargs['email']
                if kwargs['email']:
                    client.phone_number = kwargs['phone_number']
                if kwargs['address']:
                    client.address = kwargs['address']

                client.save()
                self.stdout.write(self.style.SUCCESS(f'Updated client with ID: {client.id}'))
            except Client.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Client with ID: {client_id} does not exist'))
        elif action == 'delete':
            try:
                client = Client.objects.get(pk=client_id)
                client.delete()
                self.stdout.write(self.style.SUCCESS(f'Deleted client with ID: {client_id}'))
            except Client.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Client with ID: {client_id} does not exist'))
        else:
            self.stdout.write(self.style.ERROR('Invalid action'))
