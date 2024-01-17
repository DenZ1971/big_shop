from django.db import models
from django.utils.text import slugify
import random
import string
from django.urls import reverse


def rand_slug():
    """
    Generates a random slug.

    Returns:
        str: A randomly generated slug consisting of three characters.
    """
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(3))

class Category(models.Model):
    """
    Represents a category.
    
     Attributes:
        name (str): The name of the category.
        parent (Category): The parent category of the current category.
        slug (str): The URL slug associated with the category.
        created_at (datetime): The date and time when the category was created.
    """
        
    name = models.CharField('Category',max_length=255, db_index=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children', null=True, blank=True)
    slug = models.SlugField('URL', max_length=255, unique=True, null=False, editable=True)
    created_at = models.DateTimeField('Date of creation', auto_now_add=True)
    
    class Meta:
        unique_together = (['slug', 'parent'])
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        """
        Convert the object to a string representation.
        
        """
        full_pass = [self.name]
        k = self.parent
        while k is not None:
            full_pass.append(k.name)
            k = k.parent
        return ' > '.join(full_pass[::-1])

    def save(self, *args, **kwargs):
        """
        Save the object to the database.

        """
        if not self.slug:
            self.slug = slugify(rand_slug() + '-picBetter' +self.name)
        super(Category, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("shop:category-list", args=[str(self.slug)])
    



class Product(models.Model):

    """
    Represents a product in the shop.

    """
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    title = models.CharField('Title', max_length=255)
    brand = models.CharField('Brand', max_length=255)
    description = models.TextField('Description', blank=True)
    slug = models.SlugField('URL', max_length=255)
    price = models.DecimalField('Price', max_digits=7, decimal_places=2, default=99.99)
    image = models.ImageField('Image',upload_to='products/products/%Y/%m/%d', blank=True)
    available = models.BooleanField('Available', default=True)
    created_at = models.DateTimeField('Date of creation', auto_now_add=True)
    updated_at = models.DateTimeField('Date of update', auto_now=True)

    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'

    def __str__(self):
        """
        Returns a string representation of the object.

        :return: The object's title.
        :rtype: str
        """
        return self.title

    def get_absolute_url(self):
        return reverse("shop:product-detail", args=[str(self.slug)])


class ProductManager(models.Manager):
    def get_queryset(self):
        """
        Returns a queryset of products that are available.

        :param self: The instance of the ProductManager class.
        :return: A queryset of products that are available.
        """
        return super(ProductManager, self).get_queryset().filter(available=True)


class ProductProxy(Product):

    object = ProductManager()

    class Meta:
        proxy = True
    