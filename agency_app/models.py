from django.db import models
from django.urls import reverse
from django.utils import timezone
import random



# icons generator
def generate_icon(instance, filename):
    
    filename = instance.slug + '.svg'
    return '{}'.format(filename)


def generate_filename(instance, filename):
    
    filename = instance.slug + '.jpg'
    return '{}'.format(instance.id_prop) + "/" + '{}'.format(filename)


# images generator
def generate_add_dir(instance, filename):
    return '{}'.format(instance) + "/" + '{}'.format(filename)


def prop_id_generate():
    id_prop = ''.join([random.choice(list('1234567890')) for x in range(5)])
    return id_prop

add_id_prop = prop_id_generate()


def dir_images(instance, filename):
    return '{}'.format(instance.dir_img) + "/" + '{}'.format(filename)

class Advertising(models.Model):

    phonead = models.CharField(max_length=100, null=True)
    adimage = models.ImageField(upload_to=generate_add_dir, verbose_name=u'заглавное изображенe', blank=True, null=True)

    def __str__(self):
        return self.phonead

    class Meta:
        verbose_name = 'рекламу'
        verbose_name_plural = 'реклама'

class Pages(models.Model):
    """ pages to new pages """
    
    name          = models.CharField(max_length=100, null=True, verbose_name=u'название страницы')
    slug          = models.SlugField()
    service_title = models.CharField(max_length=100, null=True, verbose_name=u'заголовок')
    service_text  = models.TextField(max_length=100, null=True, verbose_name=u'описание')
    icon          = models.CharField(max_length=100, null=True, verbose_name=u'иконка для раздела')

    def __str__(self):
        return "услуга: {}, {}".format(
            self.name, self.slug)

    def get_absolute_url(self):
        return reverse('service-detail', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'страницу'
        verbose_name_plural = 'страница'


class Category(models.Model):
    """ category of property object """
    
    name  = models.CharField(max_length=250)
    slug  = models.SlugField()
    icon  = models.FileField(upload_to=generate_icon, verbose_name=u'иконка категории', blank=True, null=True)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('category-detail', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'категорию'
        verbose_name_plural = 'категории'


class Property(models.Model):
    """ property object class """

    id_prop  = models.CharField(max_length=150, verbose_name=u'id объекта/папки', default=add_id_prop, blank=True, null=True)
    category = models.ForeignKey(Category, verbose_name=u'категоря')
    stok     = models.ForeignKey('PartnerStok', verbose_name=u'акция', on_delete=models.PROTECT, blank=True, null=True)
    agent    = models.ForeignKey('Agent', verbose_name=u'агент', on_delete=models.PROTECT)
    appointment = models.ForeignKey('Appointement', verbose_name=u'назначение', on_delete=models.PROTECT)
    coun     = models.PositiveIntegerField(default=0, verbose_name=u'просмотры')

    city     = models.ForeignKey('City', verbose_name=u'город', on_delete=models.PROTECT)
    street   = models.CharField(max_length=150, verbose_name=u'улица', blank=True)
    hnum     = models.CharField(max_length=350, verbose_name=u'номер дома', blank=True)
    romm     = models.CharField(max_length=200, verbose_name=u'кол-во комнат', blank=True)
    
    title    = models.CharField(max_length=600, verbose_name=u'заголовок')
    slug     = models.SlugField()
    desc     = models.TextField(verbose_name=u'описание')
    
    image    = models.ImageField(upload_to=generate_filename, verbose_name=u'заглавное изображенe', blank=True, null=True)
    date     = models.DateTimeField(blank=True, null=True, verbose_name=u'дата публикации')
    status   = models.BooleanField(verbose_name=u'рекламировать')
    
    area     = models.PositiveIntegerField(default=0, verbose_name=u'метраж')
    areafield = models.PositiveIntegerField(default=0, verbose_name=u'площадь')
    flor     = models.PositiveIntegerField(default=1, verbose_name=u'этажи')
    price    = models.PositiveIntegerField(default=0, verbose_name=u'стоимость')
    
    saler    = models.CharField(max_length=150, verbose_name=u'продавец', blank=True)
    salerphone = models.CharField(max_length=150, verbose_name=u'телефон продавца', blank=True)

    def __str__(self):
        return "Объект :  {} ,{}, г. {} , ул. {} , д. {} , собственник : {} {} , цена {} , {} , {}, {}".format(
            self.id_prop,
            self.title,
            self.city,
            self.street,
            self.hnum,
            self.saler, 
            self.salerphone,
            self.price,
            self.appointment,
            self.agent,
            self.category
        )


    def get_absolute_url(self):
        return reverse('object-detail', kwargs={'category': self.category.slug, 'slug': self.slug})

    class Meta:
        db_table = "property"
        verbose_name = 'объект'
        verbose_name_plural = 'объекты'


class PropertyStatistic(models.Model):
    class Meta:
        db_table = "PropertyStatistic"
        verbose_name = 'статистика'
        verbose_name_plural = 'статистика'

    count  = models.ForeignKey(Property, verbose_name=u'просмотры')
    date = models.DateField('Дата', default=timezone.now)   # дата
    views = models.PositiveIntegerField('Просмотры', default=0,  blank=True, null=True)
    url = models.CharField(max_length=150, verbose_name=u'ссылка', default='', blank=True, null=True)
    
    def __str__(self):
        return 'id:{}, {}'.format(self.count.id_prop, self.count.title)



class City(models.Model):
    name     = models.CharField(max_length=50, verbose_name=u'город', blank=True)
    slug     = models.SlugField()
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'город'
        verbose_name_plural = 'города'

class Images(models.Model):
    """ images class """
    album    = models.ForeignKey(Property)
    images   = models.ImageField(upload_to=dir_images, verbose_name=u'изображеня', blank=True, null=True)
    dir_img  = models.CharField(max_length=50, default=add_id_prop, verbose_name=u'название папки')
    
    def __str__(self):
        return "Объект:{}, категория: {}".format(
            self.album.title, self.album.category.name)

    class Meta:
        verbose_name = 'изображение'
        verbose_name_plural = 'изображения'

class Appointement(models.Model):
    appointment = models.CharField(max_length=100, verbose_name=u'назначение')
    slug = models.SlugField()

    def __str__(self):
        return "{}".format(self.appointment)

    class Meta:
        verbose_name = 'назначение'
        verbose_name_plural = 'назначение'


class Agent(models.Model):
    """ Agent class """

    first_name = models.CharField(max_length=50, verbose_name=u'имя')
    last_name  = models.CharField(max_length=50, verbose_name=u'фамилия')
    phone      = models.CharField(max_length=22, verbose_name=u'телефон')
    email      = models.CharField(max_length=50)
    avatar     = models.ImageField(blank=True, null=True)

    def __str__(self):
        return "Агент: {} {}".format(self.first_name, self.last_name)


    class Meta:
        verbose_name = 'агента'
        verbose_name_plural = 'агенты'


class PartnerStok(models.Model):
    """ partner stok class """

    company_name = models.CharField(max_length=100, null=True, verbose_name=u'компания')
    company_url  = models.URLField(blank=True, null=True, verbose_name=u'сайт компании')
    condition    = models.CharField(max_length=220, blank=True, null=True, verbose_name=u'описание')
    amount       = models.DateTimeField(verbose_name=u'срок действия акции до/')
    tag          = models.TextField(default="tagstock")

    def __str__(self):
        return  "Акция {}. Партнер {}".format(self.condition, self.company_name)

    class Meta:
        verbose_name = 'скидку'
        verbose_name_plural = 'скидки'

class Qeustions(models.Model):
    
    quest = models.CharField(max_length=300, null=True, verbose_name=u'вопрос')
    answer = models.CharField(max_length=300, null=True, verbose_name=u'ответ')
    slug  = models.SlugField()

    class Meta:
        verbose_name = 'вопрос'
        verbose_name_plural = 'вопросы'

    def __str__(self):
        return self.quest
