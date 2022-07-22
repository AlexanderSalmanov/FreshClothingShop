from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.db.models.signals import pre_save, post_save
from django.db.models import Q
from django.conf import settings


from ecom.utils import unique_slug_generator, random_string_generator

User = settings.AUTH_USER_MODEL
# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, allow_unicode=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('products:category_list', kwargs={'slug':self.slug})


ORDER_TYPE_CHOICES = (
    ('Price', 'price'),
    ('Timestamp', 'timestamp'),
    ('Popularity', 'times_viewed')
)

class ProductQuerySet(models.query.QuerySet):
    def in_stock(self):
        return self.filter(in_stock=True)

    def by_brand(self, brand_name):
        return self.filter(brand=brand_name)

    def out_of_stock(self):
        return self.filter(in_stock=False)

    def search(self, query):
        lookups = Q(title__icontains=query) | Q(description__icontains=query)
        return self.filter(lookups).distinct()

class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def by_brand(self, brand_name):
        return self.get_queryset().by_brand(brand_name)

    def all(self):
        return self.get_queryset().in_stock()

    def outdated(self):
        return self.get_queryset().out_of_stock()

    def search(self, query):
        return self.get_queryset().search(query)



BRAND_CHOICES = (
    ('adidas', 'Adidas'),
    ('puma', 'Puma'),
    ('nike', 'Nike'),
    ('jordan', 'Jordan'),
    ('champion', 'Champion'),
    ('elesse', 'Elesse'),
    ('47-brand', '47 Brand')
)

class Product(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, allow_unicode=True)
    brand = models.CharField(max_length=255, blank=True, null=True, choices=BRAND_CHOICES)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    description = models.TextField(default='No description provided.')
    times_viewed = models.PositiveIntegerField(default=0)
    in_stock = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = ProductManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('products:single', kwargs={'slug': self.slug})

    @property
    def image_URL(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url

    def save(self, *args, **kwargs):
        obj_slug = slugify(self.title)
        qs = Product.objects.filter(slug=obj_slug)
        if qs.count() > 1:
            obj_slug += random_string_generator(5)
        self.slug = obj_slug
        return super().save(*args, **kwargs)


# def pre_save_product_receiver(sender, instance, *args, **kwargs):
#     if instance.slug:
#         instance.slug = unique_slug_generator(instance)
#
# pre_save.connect(pre_save_product_receiver, sender=Product)
