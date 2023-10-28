from django.contrib import admin
from .models import Product, Client, Order


@admin.action(description="Сбросить количество в ноль")
def reset_quantity(modeladmin, request, queryset):
    queryset.update(quantity=0)


class ProductAdmin(admin.ModelAdmin):
    """Список продуктов."""
    list_display = ['name', 'price', 'quantity']
    ordering = ['price', 'quantity']
    list_filter = ['creation_date', 'price']
    search_fields = ['description']
    search_help_text = 'Поиск по полю Описание продукта (description)'
    actions = [reset_quantity]

    """Отдельный продукт."""
    readonly_fields = ['creation_date']
    fieldsets = [
        (
            None,
            {
                'classes': ['wide'],
                'fields': ['name'],
            },
        ),
        (
            'Подробности',
            {
                'classes': ['collapse'],
                'description': 'Подробное описание',
                'fields': ['creation_date', 'description'],
            },
        ),
        (
            'Бухгалтерия',
            {
                'fields': ['price', 'quantity'],
            }
        ),
        (
            'Фото',
            {
                'fields': ['photo'],
            }
        ),
    ]


class ClientAdmin(admin.ModelAdmin):
    """Список клиентов."""
    list_display = ['name', 'email', 'phone_number', 'address', 'registration_date']
    ordering = ['name']
    search_fields = ['name', 'email', 'phone_number', 'address']
    list_filter = ['registration_date']

    """Отдельный клиент."""
    readonly_fields = ['registration_date']


class OrderAdmin(admin.ModelAdmin):
    """Список заказов."""
    list_display = ['id', 'client', 'total_amount', 'order_date']
    ordering = ['order_date']
    search_fields = ['client__name', 'total_amount']
    list_filter = ['order_date']

    """Отдельный заказ."""
    readonly_fields = ['order_date']


admin.site.register(Product, ProductAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Order, OrderAdmin)
