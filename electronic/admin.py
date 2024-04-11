from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from electronic.models import Network, Product


@admin.register(Network)
class NetworkAdmin(admin.ModelAdmin):
    """
    Административная модель для класса Network.
    """

    actions = ['clear_debt_to_supplier']
    fields = (
        'name', 'email', 'level', 'country', 'city', 'street', 'house_number', 'products', 'supplier',
        'debt_to_supplier')
    raw_id_fields = ('supplier',)

    list_display = ('name', 'email', 'level', 'country', 'city', 'supplier_link')
    list_filter = ('city',)

    def clear_debt_to_supplier(self, request, queryset):
        """
        Очистка задолженности перед поставщиком у выбранных объектов.
        """
        for obj in queryset:
            if obj.supplier:
                obj.debt_to_supplier = 0
                obj.save(update_fields=['debt_to_supplier'])
        count = queryset.count()
        if count == 1:
            message_bit = "1 объект"
        else:
            message_bit = f"{count} объектов"
        self.message_user(request, f"Задолженность перед поставщиком очищена у {message_bit}.")

    clear_debt_to_supplier.short_description = "Очистить задолженность перед поставщиком"

    def supplier_link(self, obj):
        """
        Генерирует ссылку на страницу поставщика.
        """
        if obj.supplier:
            link = reverse('admin:electronic_network_change', args=[obj.supplier.id])
            return format_html('<a href=%s>%s(%s)</a>' % (link, obj.supplier.name, obj.supplier.country))
        return None

    supplier_link.short_description = 'Поставщик'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Административная модель для класса Product.
    """
    pass
