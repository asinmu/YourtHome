from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import ArrayField


class Type(models.Model):
    type = models.CharField('Тип', max_length=100)

    class Meta:
        verbose_name = 'Тип недвижимости'
        verbose_name_plural = 'Типы недвижимости'

    def __str__(self):
        return self.type


class Room(models.Model):
    room = models.CharField('Количество комнат', max_length=100)

    class Meta:
        verbose_name = 'Комната'
        verbose_name_plural = 'Комнаты'

    def __str__(self):
        return self.room


class Floor(models.Model):
    floor = models.IntegerField('Этаж')

    class Meta:
        verbose_name = 'Этаж'
        verbose_name_plural = 'Этажи'

    def __str__(self):
        return str(self.floor)


class Series(models.Model):
    name = models.CharField('Серия', max_length=100)

    class Meta:
        verbose_name = 'Серия'
        verbose_name_plural = 'Серии'

    def __str__(self):
        return self.name


class Construction(models.Model):
    name = models.CharField('Тип постройки', max_length=100)

    class Meta:
        verbose_name = 'Тип постройки'
        verbose_name_plural = 'Типы постройки'

    def __str__(self):
        return self.name


class State(models.Model):
    name = models.CharField('Состояние', max_length=100)

    class Meta:
        verbose_name = 'Состояние'
        verbose_name_plural = 'Состояния'

    def __str__(self):
        return self.name


class Area(models.Model):
    total_area = models.FloatField('Общая площадь', blank=True, null=True)
    living_area = models.FloatField('Жилая площадь', blank=True, null=True)

    class Meta:
        verbose_name = 'Площадь'
        verbose_name_plural = 'Площадь'

    def __str__(self):
        return f'Общая площадь: {self.total_area}, Жилая площадь: {self.living_area}'


class Country(models.Model):
    name = models.CharField('Страна', max_length=100)

    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'

    def __str__(self):
        return self.name


class ObjectsInApartment(models.Model):
    name = models.CharField('В доме есть', max_length=100)

    class Meta:
        verbose_name = 'В доме есть'
        verbose_name_plural = 'В доме есть'

    def __str__(self):
        return self.name


class NearbyObjects(models.Model):
    name = models.CharField('Рядом есть', max_length=100)

    class Meta:
        verbose_name = 'Рядом есть'
        verbose_name_plural = 'Рядом есть'

    def __str__(self):
        return self.name


class Region(models.Model):
    name = models.CharField('Регион', max_length=100)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, verbose_name='Страна')

    class Meta:
        verbose_name = 'Регион'
        verbose_name_plural = 'Регионы'

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField('Город', max_length=100)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, verbose_name='Регион')

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

    def __str__(self):
        return self.name


class District(models.Model):
    name = models.CharField('Район', max_length=100)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, verbose_name='Город')

    class Meta:
        verbose_name = 'Район'
        verbose_name_plural = 'Районы'

    def __str__(self):
        return self.name


class Location(models.Model):
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, verbose_name='Страна')
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, verbose_name='Регион')
    city = models.CharField(max_length=70, default="Бишкек", verbose_name='Город')
    district = models.CharField(max_length=170, default="8 микрорайон", verbose_name='Район')
    street = models.CharField('Улица', max_length=100)
    house_number = models.CharField('Номер дома', max_length=15, blank=True, null=True)
    latitude = models.FloatField('Широта', blank=True, null=True)
    longitude = models.FloatField('Долгота', blank=True, null=True)

    def __str__(self):
        return f'Страна: {self.country}, Регион: {self.region}, Город: {self.city}, Улица: {self.street}, ' \
               f'Номер дома: {self.house_number}'

    class Meta:
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'


class Detail(models.Model):
    furniture = models.BooleanField('Мебель', blank=True, null=True)
    heat = models.BooleanField('Отопление', blank=True, null=True)
    gas = models.BooleanField('Газ', blank=True, null=True)
    electricity = models.BooleanField('Электричество', blank=True, null=True)
    internet = models.BooleanField('Интернет', blank=True, null=True)
    phone = models.BooleanField('Телевонная линия', blank=True, null=True)
    parking = models.BooleanField('Парковка', blank=True, null=True)
    elevator = models.BooleanField('Лифт', blank=True, null=True)
    security = models.BooleanField('Охрана', blank=True, null=True)

    class Meta:
        verbose_name = 'Характеристика'
        verbose_name_plural = 'Характеристики'

    def __str__(self):
        return f'Мебель: {self.furniture}, Отопление: {self.heat}, Газ: {self.gas}, Электричество: {self.electricity}, ' \
               f'Интернет: {self.internet}'


class Currency(models.Model):
    name = models.CharField('Валюта', max_length=100)

    class Meta:
        verbose_name = 'Валюта'
        verbose_name_plural = 'Валюты'

    def __str__(self):
        return self.name


class Role(models.Model):
    name = models.CharField('Тип арендодатора', max_length=100)

    class Meta:
        verbose_name = 'Тип арендотатора'
        verbose_name_plural = 'Типы арендодатора'

    def __str__(self):
        return self.name


class Contact(models.Model):
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, verbose_name='Тип арендодатора')
    phone = models.CharField('Номер телефона', max_length=25, blank=True, null=True)
    name = models.CharField('Имя', max_length=30, blank=True, null=True)
    surname = models.CharField('Фамилия', max_length=30, blank=True, null=True)

    class Meta:
        verbose_name = 'Контактные данные'
        verbose_name_plural = 'Контактные данные'

    def __str__(self):
        return f'{self.surname} {self.name}, номер телефона: {self.phone}'


class Apartment(models.Model):
    type = models.ForeignKey(Type, on_delete=models.SET_NULL, null=True, verbose_name='Тип недвижимости')
    room = models.PositiveSmallIntegerField(default=1, verbose_name='Количество комнат')
    floor = models.PositiveSmallIntegerField(default=1, verbose_name='Этаж')
    storey = models.PositiveSmallIntegerField(default=9, verbose_name='Этажность')
    area = models.ForeignKey(Area, on_delete=models.SET_NULL, null=True, verbose_name='Площадь', related_name='area')
    series = models.ForeignKey(Series, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Серия')
    construction_type = models.ForeignKey(Construction, on_delete=models.SET_NULL, null=True,
                                          verbose_name='Тип сторения')
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, verbose_name='Состояние')
    detail = models.ForeignKey(Detail, on_delete=models.SET_NULL, null=True, verbose_name='Характеристики',
                               related_name='detail')
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, verbose_name='Расположение',
                                 related_name='location')

    price = models.FloatField('Цена')
    title = models.CharField(max_length=150, verbose_name='Заголовок', null=True, blank=True)
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True, verbose_name='Валюта')
    preview_image = models.ImageField('Главное фото', upload_to='photos/', blank=True, null=True)
    description = models.TextField('Описание', blank=True, null=True)
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    contact = models.ForeignKey(Contact, on_delete=models.SET_NULL, null=True, verbose_name='Контактиные данные',
                                related_name='contact')
    another_price = models.FloatField('Конвертированная цена.', null=True, blank=True, default=0)
    status = models.BooleanField('Статус объекта недвижимости', default=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name='Владелец')

    nearby_objects = ArrayField(models.CharField(max_length=250, blank=True, null=True), null=True, blank=True,
                                default=list, verbose_name='Рядом есть')

    objects_in_apartment = ArrayField(models.CharField(max_length=250, blank=True, null=True), null=True, blank=True,
                                      default=list, verbose_name='В квартире есть')

    def save(self, *args, **kwargs):
        try:
            import requests
            from bs4 import BeautifulSoup
            DOLLAR_SOM = 'https://www.akchabar.kg/ru/exchange-rates/dollar/'
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}

            full_page = requests.get(DOLLAR_SOM, headers=headers)
            soup = BeautifulSoup(full_page.content, 'html.parser')
            convert = soup.findAll("h2")
            if str(self.currency) == '$' or self.currency == 2:
                self.another_price = round(float(convert[1].text) * float(self.price), 2)
            elif str(self.currency) == 'сом' or self.currency == 1:
                self.another_price = round(float(self.price) / float(convert[1].text), 2)
        except:
            super(Apartment, self).save(*args, **kwargs)
        finally:
            super(Apartment, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Объект недвижимости'
        verbose_name_plural = 'Объекты недвижимости'

    def __str__(self):
        return self.title or ''


class Comment(models.Model):
    apartment = models.ForeignKey(Apartment, on_delete=models.SET_NULL, null=True, verbose_name='Объект недвижимости',
                                  related_name='comments')
    name_of_publication = models.CharField('Заголовок', blank=True, null=True, max_length=100, default=' ',
                                           help_text='Введите заголовок')
    text_of_publication = models.TextField('Текст публикации', blank=True, null=True, help_text='Введите текст')
    date_of_publication = models.DateTimeField('Дата публикации', auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name='Владелец')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.name_of_publication


class Booking(models.Model):
    apartment = models.ForeignKey(Apartment, on_delete=models.SET_NULL, null=True, verbose_name='Объект недвижимости',
                                  related_name='orders')
    arrival_date = models.DateField('Дата прибытия', help_text='гггг-мм-дд', blank=True, null=True, )
    departure_date = models.DateField('Дата отбытия', help_text='гггг-мм-дд', blank=True, null=True, )

    class Meta:
        verbose_name = 'Система бронирования'
        verbose_name_plural = 'Система бронирования'

    def __str__(self):
        return f'{self.arrival_date} - {self.departure_date}'


class ApartmentImage(models.Model):
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, related_name='apartment_image')
    image = models.FileField(blank=True, null=True, verbose_name='Фотография')

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'

    def __str__(self):
        return str(self.image)
