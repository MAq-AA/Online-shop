from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from auth_user.models import Profile


class Product(models.Model):
    objects = models.Manager()
    slug = models.SlugField(null=True, default="")
    title = models.CharField(max_length=100, null=True, verbose_name='Название')
    img = models.ImageField(upload_to='images/product', null=False, verbose_name='Фото')
    description = models.TextField(null=False, verbose_name='Описание')
    shortdescription = models.CharField(max_length=100, null=True, verbose_name='Краткое описание')
    price = models.PositiveIntegerField(null=False, verbose_name='Цена')
    provider = models.ForeignKey('Provider', null=True, verbose_name='Поставщик', on_delete=models.SET_NULL)
    animal_sort = models.ForeignKey('AnimalSort', null=True, verbose_name='Вид животного', on_delete=models.SET_NULL)
    subcategory = models.ForeignKey('SubCategory', null=True, verbose_name='Подкатегория', on_delete=models.SET_NULL)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class AnimalSort(models.Model):
    object = models.Manager()
    slug = models.SlugField(null=True, default="slug")
    title = models.CharField(max_length=30, null=False, verbose_name='Название')
    description = models.TextField(null=False, verbose_name='Описание')
    category = models.ManyToManyField('Category', verbose_name='Категории')
    subcategory = models.ManyToManyField('Subcategory', verbose_name='Подкатегории')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Вид животное'
        verbose_name_plural = 'Виды животных'


class Category(models.Model):
    object = models.Manager()
    slug = models.SlugField(null=True, default="slug")
    title = models.CharField(max_length=30, null=False, verbose_name='Название')
    description = models.TextField(null=False, verbose_name='Описание')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Subcategory(models.Model):
    object = models.Manager()
    slug = models.SlugField(null=True)
    title = models.CharField(max_length=30, null=False, verbose_name='Название')
    description = models.TextField(null=False, verbose_name='Описание')
    img = models.ImageField(null=False, upload_to='images/subcat', default='images/default.png', verbose_name='Фото')
    category = models.ForeignKey('Category', verbose_name='Категории', null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'


class Provider(models.Model):
    object = models.Manager()
    company = models.CharField(max_length=100, null=False, verbose_name='Название')
    phone_number = PhoneNumberField(null=False, verbose_name='Телефон')
    delegate_fullName = models.CharField(max_length=100, null=False, verbose_name='Имя представителя')
    address = models.TextField(null=False, verbose_name='Адрес компании')
    img = models.ImageField(null=False, upload_to='images/provider', default='images/default.png', verbose_name='Фото')

    def __str__(self):
        return self.company

    class Meta:
        verbose_name = 'Поставщик'
        verbose_name_plural = 'Поставщики'


class Feedback(models.Model):
    objects = models.Manager()
    profile = models.ForeignKey(Profile, null=True, on_delete=models.CASCADE)
    score = models.IntegerField(null=False, verbose_name='Оценка товара')
    text = models.TextField(max_length=1000, null=True, verbose_name='Отзыв')
    products = models.ForeignKey("Product", null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class Basket(models.Model):
    object = models.Manager()
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    products = models.ManyToManyField("Product", related_name="shop_basket_product")
    bought = models.ManyToManyField("Product")
