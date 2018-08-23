from django.views.generic.list import MultipleObjectMixin
from agency_app.models import  Pages, Category, Property
from django.urls import reverse
from geopy.geocoders import Yandex


class CategoryListMixin(MultipleObjectMixin):
    def get_context_data(self, *args, **kwargs):
        context = {}
        context['categories'] = Category.objects.all()
        return context

class PageListMixin(MultipleObjectMixin):
    def get_context_data(self, *args, **kwargs):
        context = {}
        context['pages'] = Pages.objects.all()
        return context

class PriceListMixin(MultipleObjectMixin):
    def get_context_data(self, *args, **kwargs):
        context = {}
        context['price'] = Property.objects.all()
        return context

class ContactFormMixin(object):
    
    def form_valid(self, form):
        form.send_email(self.request)
        return super(ContactFormMixin, self).form_valid(form)

    def get_success_url(self):
        return reverse('completed')

class GeoCoorMixin:
    def geoloc(city, adress, hnum):
        geolocator = Yandex()
        w = str(city), str(adress), str(hnum)
        adress = ' '.join(w)
        location = geolocator.geocode(adress)
        return list([location.latitude, location.longitude])