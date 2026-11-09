from django.db import models
from core.models import BaseModel

class ProductStock(BaseModel):
    barbershop = models.ForeignKey(to='Barbershop', on_delete=models.CASCADE, verbose_name='барбершоп', related_name='stocks')
    product = models.ForeignKey(to='Product', on_delete=models.CASCADE, verbose_name='товар', related_name='stocks')
    stock = models.PositiveIntegerField(verbose_name='остаток',  default=0)


    class Meta:
        db_table = 'product_stock'
        verbose_name = 'остаток товара'
        verbose_name_plural = 'остатки товара'

        unique_together = ('barbershop', 'product')

    def __str__(self):
        return f"{self.product} в {self.barbershop}: {self.stock} шт."

    # остаток конкретного товара в определённом барбершопе
    # Один филиал может хранить много разных товаров, а один товар может быть в разных филиалах