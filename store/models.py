from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from utils.models import Color, Size


class Category(MPTTModel):
    name = models.CharField(verbose_name='Category name', max_length=50, unique=True)
    slug = models.SlugField(verbose_name='Category safe URL', max_length=255, unique=True)
    parent = TreeForeignKey('self', on_delete=models.RESTRICT, null=True, blank=True, related_name='children')
    image = models.ImageField(verbose_name='Category image', upload_to='images/', blank=True)
    is_active = models.BooleanField(default=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class ProductType(models.Model):
    name = models.CharField(verbose_name='Product type', max_length=50)

    def __str__(self):
        return self.name


class ProductProp(models.Model):
    name = models.CharField(verbose_name='Properties name', max_length=50)
    type = models.ForeignKey(ProductType, related_name='props', on_delete=models.RESTRICT)


class Product(models.Model):
    title = models.CharField(verbose_name='Product title', max_length=50)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.RESTRICT)
    type = models.ForeignKey(ProductType, related_name='products', on_delete=models.RESTRICT)
    description = models.TextField(verbose_name='Product description')
    stock = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = [-created_at]


class ProductPropValue(models.Model):
    product = models.ForeignKey(Product, related_name='props', on_delete=models.CASCADE)
    product_prop = models.ForeignKey(ProductProp, related_name='values', on_delete=models.CASCADE)
    value = models.CharField(max_length=50)

    def __str__(self):
        return self.product_prop.name + ':' + self.value


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(verbose_name='Product image', upload_to='images/')
    alt_text = models.CharField(verbose_name='Alternative text', max_length=255, null=True, blank=True)
    is_preview = models.BooleanField(default=False)

    def __str__(self):
        return self.alt_text


class ProductDetail(models.Model):
    product = models.ForeignKey(Product, related_name='details', on_delete=models.CASCADE)
    color = models.ForeignKey(Color, related_name='products', on_delete=models.SET_NULL, null=True)
    sizes = models.ManyToManyField(Size, related_name='products')
# Create your models here.
