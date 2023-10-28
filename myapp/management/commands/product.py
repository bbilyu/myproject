from django.core.management.base import BaseCommand
from django.utils import timezone
from myapp.models import Product

# Создание продукта: python manage.py product_commands create --name "Product 1" --description "Description of Product 1" --price 10.50 --quantity 100
# Чтение всех продукта по id:python manage.py product read --id 1
# Чтение всех продуктов: python manage.py product read
# Обновление продукта: python manage.py product update --id 1 --name "Updated Product 1" --price 15.00
# Удаление продукта: python manage.py product delete --id 1

class Command(BaseCommand):
    help = 'CRUD operations on Product model'

    def add_arguments(self, parser):
        parser.add_argument('action', type=str, help='CRUD operation to perform')
        parser.add_argument('--id', type=int, nargs='?', help='Product ID')
        parser.add_argument('--name', type=str, nargs='?', help='Product name')
        parser.add_argument('--description', type=str, nargs='?', help='Product description')
        parser.add_argument('--price', type=float, nargs='?', help='Product price')
        parser.add_argument('--quantity', type=int, nargs='?', help='Product quantity')

    def handle(self, *args, **kwargs):
        action = kwargs['action']
        id = kwargs.get('id')
        name = kwargs.get('name')
        description = kwargs.get('description')
        price = kwargs.get('price')
        quantity = kwargs.get('quantity')

        if action == 'create':
            product = Product(name=name, description=description, price=price, quantity=quantity,creation_date=timezone.now())
            product.save()
            self.stdout.write(self.style.SUCCESS('Product created successfully.'))

        elif action == 'read':
            if id:
                try:
                    product = Product.objects.get(id=id)
                    self.stdout.write(f'-\nProduct ID: {product.id}\nProduct name: {product.name}\nProduct description: {product.description}\nProduct price: {product.price}\nProduct quantity: {product.quantity}\nProduct creation date: {product.creation_date}')
                except Product.DoesNotExist:
                    self.stdout.write(self.style.ERROR('Product does not exist.'))

            else:
                products = Product.objects.all()
                if products.exists():
                    for product in products:
                        self.stdout.write(f'-\nProduct ID: {product.id}\nProduct name: {product.name}\nProduct description: {product.description}\nProduct price: {product.price}\nProduct quantity: {product.quantity}\nProduct creation date: {product.creation_date}')
                else:
                    self.stdout.write(self.style.NOTICE('No products found.'))

        elif action == 'update':
            if id:
                try:
                    product = Product.objects.get(id=id)
                    if name:
                        product.name = name
                    if description:
                        product.description = description
                    if price:
                        product.price = price
                    if quantity:
                        product.quantity = quantity
                    product.save()
                    self.stdout.write(self.style.SUCCESS('Product updated successfully.'))
                except Product.DoesNotExist:
                    self.stdout.write(self.style.ERROR('Product does not exist.'))
            else:
                self.stdout.write(self.style.ERROR('Please provide a product ID.'))

        elif action == 'delete':
            if id:
                try:
                    product = Product.objects.get(id=id)
                    product.delete()
                    self.stdout.write(self.style.SUCCESS('Product deleted successfully.'))
                except Product.DoesNotExist:
                    self.stdout.write(self.style.ERROR('Product does not exist.'))
            else:
                self.stdout.write(self.style.ERROR('Please provide a product ID.'))

        else:
            self.stdout.write(self.style.ERROR('Invalid action.'))