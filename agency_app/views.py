from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from agency_app.models import Pages, Category, Agent, Property, Images, MainMedia, City
from django.forms import modelformset_factory
from agency_app.mixins import CategoryListMixin, CategoryListMixin
from django.db.models import Q
from django.http import JsonResponse
from django.views import View


        
class ObjectListView(ListView):
    model = Property
    template_name = 'objects.html'
    
    def get_context_data(self, *args, **kwargs):
        context = super(ObjectListView, self).get_context_data(*args, **kwargs)
        context['categories'] = Category.objects.all()
        context['articles'] = self.model.objects.all()
        context['pages'] = Pages.objects.all()
        context['cities'] = City.objects.all()
        return context




class CategoryListView(ListView):
    model = Category
    template_name = 'index.html'
    
    def get_context_data(self, *args, **kwargs):
        context = super(CategoryListView, self).get_context_data(*args, **kwargs)
        context['categories'] = self.model.objects.all()
        context['articles'] = Property.objects.all()
        context['agents'] = Agent.objects.all()
        context['pages'] = Pages.objects.all()
        context['main_media'] = MainMedia.objects.all()
        return context



class CategoryDetailView(DetailView, CategoryListMixin):
    
    model = Category
    template_name = 'category_detail.html'
    
    def get_context_data(self, *args, **kwargs):
        context = super(CategoryDetailView, self).get_context_data(*args, **kwargs)
        context['category'] = self.get_object()
        context['categories'] = Category.objects.all()
        context['object_from_category'] = self.get_object().property_set.all()
        
        return context

class ObjectDetailView(DetailView, CategoryListMixin):
    model = Property
    template_name = 'object_detail.html'

    def get_context_data(self,  *args, **kwargs):
        context = super(ObjectDetailView, self).get_context_data(*args, **kwargs)
        context['categories'] = Category.objects.all()
        context['article'] = self.get_object()
        art_id = self.get_object().pk
        img = Images.objects.all()
        context['imges'] = img.filter(album_id=art_id)
        return context 



class DynamicCategoryImage(View):
    
    def get(self, request, *args, **kwargs):
        category_id = request.GET.get('category_id')
        category = Category.objects.get(id=category_id)
        data = {
            'category_image': category.icon.url
        }
        return JsonResponse(data)


class PagesDetailView(DetailView, CategoryListMixin):
    
    model = Pages
    template_name = 'service-detail.html'
    
    def get_context_data(self, *args, **kwargs):
        context = super(PagesDetailView, self).get_context_data(*args, **kwargs)
        context['pages_article'] = self.get_object()
        return context


class DynamicPageImage(View):
    def get(self, request, *args, **kwargs):
        page_id = request.GET.get('page_id')
        page = Pages.objects.get(id=page_id)
        data = {
            'page_image': page.service_icon.url
        }
        return JsonResponse(data)


class Searcher(View):
    template_name = "search.html"

    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('q')
        found_obj = Property.objects.filter(
                        Q(title__icontains=query)|
                        Q(desc__icontains=query)
                    )
        context = {
            'found_obj': found_obj
        }
    
        return render(self.request, self.template_name, context)

