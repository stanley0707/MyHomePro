from django.views.generic.list import MultipleObjectMixin
from agency_app.models import  Pages, Category
from django.urls import reverse


class CategoryListMixin(MultipleObjectMixin):
    def get_context_data(self, *args, **kwargs):
        context = {}
        context['categories'] = Category.objects.all()
        return context

class CategoryListMixin(MultipleObjectMixin):
    def get_context_data(self, *args, **kwargs):
        context = {}
        context['pages'] = Pages.objects.all()
        return context

class ContactFormMixin(object):
    
    def form_valid(self, form):
        form.send_email(self.request)
        return super(ContactFormMixin, self).form_valid(form)

    def get_success_url(self):
        return reverse('completed')