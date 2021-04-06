from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'categories'

class Brand(models.Model):
    name      = models.CharField(max_length=45)
    image_url = models.URLField(max_length=2000)

    class Meta:
        db_table = 'brands'

class Line(models.Model):
    name  = models.CharField(max_length=45)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)

    class Meta:
        db_table = 'brand_lines'

class SubLine(models.Model):
    name       = models.CharField(max_length=45)
    brand_line = models.ForeignKey(Line, on_delete=models.CASCADE)

    class Meta:
        db_table = 'sublines'


class Product(models.Model):
    korean_name   = models.CharField(max_length=100)
    english_name  = models.CharField(max_length=100)
    models_number = models.CharField(max_length=50)
    best_color    = models.CharField(max_length=50)
    release_date  = models.DateField()
    release_price = models.DecimalField(max_digits=10, decimal_places=2)
    sell_count    = models.PositiveIntegerField(default=0)
    category      = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    brand         = models.ForeignKey(Brand, on_delete=models.CASCADE)
    brand_line    = models.ForeignKey(Line, on_delete=models.SET_NULL, null=True)
    sub_line      = models.ForeignKey(SubLine, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'products'

class ProductSize(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size    = models.ForeignKey('Size', on_delete=models.CASCADE)

    class Meta:
        db_table = 'products_sizes'

class ProductImage(models.Model):
    image_url = models.URLField(max_length=2000)
    product   = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        db_table = 'product_images'

class Size(models.Model):
    size     = models.CharField(max_length=45)
    products = models.ManyToManyField(Product, through='ProductSize')

    class Meta:
        db_table = 'sizes'
