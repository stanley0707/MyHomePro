from django.views.generic.list import MultipleObjectMixin
from agency_app.models import  Pages, Category


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
