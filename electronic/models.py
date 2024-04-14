from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

NULLABLE = {'null': True, 'blank': True}


class Product(models.Model):
    """ Модель продуктов """

    title = models.CharField(max_length=150, verbose_name='Наименование продукта')
    model = models.CharField(max_length=150, verbose_name='Модель продукта', **NULLABLE)
    release_date = models.DateField(verbose_name='Дата выхода продукта на рынок', **NULLABLE)

    def __str__(self):
        return f'{self.title} {self.model}'

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'


class Network(models.Model):
    """
    Модель для представления объекта сети.
    """

    LEVEL_CHOICES = (
        (0, 'Завод'),
        (1, 'Розничная сеть'),
        (2, 'Индивидуальный предприниматель'),
    )

    name = models.CharField(max_length=255, verbose_name="название")
    level = models.IntegerField(choices=LEVEL_CHOICES, **NULLABLE, verbose_name="уровень")
    email = models.EmailField(verbose_name="email")
    country = models.CharField(max_length=100, verbose_name="страна")
    city = models.CharField(max_length=100, verbose_name="город")
    street = models.CharField(max_length=100, verbose_name="улица")
    house_number = models.CharField(max_length=10, verbose_name="номер дома")
    products = models.ManyToManyField(Product, related_name='network_modes', verbose_name="продукты")
    supplier = models.ForeignKey('self', on_delete=models.SET_NULL, **NULLABLE, verbose_name="поставщик")
    debt_to_supplier = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="задолженность")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="дата создания")

    def __str__(self):
        """
        Возвращает строковое представление объекта сети.
        """
        return f"{self.name}, {self.email}, {self.country}"

    class Meta:
        ordering = ["id"]
        verbose_name = "Объект сети"
        verbose_name_plural = "Объекты сети"


@receiver(pre_save, sender=Network)
def set_network_level(sender, instance, **kwargs):
    """
    Обработчик сигнала pre_save, устанавливает уровень (level) объекта сети.
    """
    if instance.supplier:
        instance.level = instance.supplier.level + 1
    else:
        # Если у объекта нет поставщика, он считается заводом (уровень 0)
        instance.level = 0
