from django.db import models


class WeighableMixin(models.Model):
    """Mixin for weighable products.

    This mixin provides a `weight` field and a `convert()` method which
    provides conversiont between (*e.g.*: gram to kilogram).
    """
    weight = models.DecimalField('Weight (g.)', max_length=256, max_digits=6,
                                 decimal_places=2)

    class Meta:
        abstract = True

    def convert(self, target='Kg'):
        """Convert weight (expressed in grams).
        """
        pass


class Product(models.Model):
    name = models.CharField('Name', max_length=256)

    class Meta:
        abstract = True


class Vegetable(Product, WeighableMixin):
    """Marker class for vegetables."""
    class Meta:
        abstract = True


class Fruit(Product, WeighableMixin):
    """Marker class for fruits."""
    class Meta:
        abstract = True


class Potato(Vegetable):
    class Meta:
        ordering = ('name', )

        verbose_name = 'Potato'
        verbose_name_plural = 'Potatoes'


class Tomato(Vegetable):
    class Meta:
        ordering = ('name', )

        verbose_name = 'Tomato'
        verbose_name_plural = 'Tomatoes'


class Eggplant(Vegetable):
    class Meta:
        ordering = ('name', )

        verbose_name = 'Eggplant'
        verbose_name_plural = 'Eggplants'
