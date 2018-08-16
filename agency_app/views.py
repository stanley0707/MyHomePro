from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from agency_app.models import (
		Pages,
		Category,
		Agent,
		Property,
		Images,
		Advertising,
		City,
		Qeustions,
		Appointement
	)

from django.forms import modelformset_factory
from agency_app.mixins import(
		CategoryListMixin,
		CategoryListMixin,
		ContactFormMixin,
		GeoCoorMixin,

	)

from django.db.models import Q
from django.http import JsonResponse
from django.views import View
from agency import settings
from django.views.generic import TemplateView, CreateView, FormView
from django.shortcuts import render_to_response
from django.template import RequestContext
	

class ObjectListView(ListView):
	model = Property
	template_name = 'objects.html'
	
	def get_context_data(self, *args, **kwargs):
		
		context = super(ObjectListView, self).get_context_data(*args, **kwargs)
		context['categories'] = Category.objects.all()
		context['articles'] = self.model.objects.all()
		context['pages'] = Pages.objects.all()
		context['cities'] = City.objects.all()
		context['main_media'] = Advertising.objects.all()
		context['question'] = Qeustions.objects.all()
		context['appointment'] = Appointement.objects.all()
		
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
		context['main_media'] = Advertising.objects.all()
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


class CompletedPage(TemplateView):
	template_name = "object_send_complete.html"


class ObjectDetailView(ContactFormMixin, GeoCoorMixin, FormView, DetailView):
	model = Property
	template_name = 'object_detail.html'

	def get_context_data(self, *args, **kwargs):
		context = super(ObjectDetailView, self).get_context_data(*args, **kwargs)
		context['categories'] = Category.objects.all()
		context['article'] = self.get_object()
		art_id = self.get_object().pk
		img = Images.objects.all()
		context['imges'] = img.filter(album_id=art_id)
		context['geoposition'] = GeoCoorMixin.geoloc(
								self.get_object().city,
								self.get_object().street,
								self.get_object().hnum
							)
		return context


class ContactModelFormView(ContactFormMixin, CreateView):
	pass


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
	template = "search.html"

	def get(self, request, *args, **kwargs):
		query = self.request.GET.get('q')
		query = query.title().split()
		for query in query:
			found_obj = Property.objects.filter(
							Q(id_prop__icontains=query)| # blank True null True
							Q(category__name__icontains=query)|    #
							Q(agent__first_name__icontains=query)| #
							Q(agent__last_name__icontains=query)|  #
							Q(city__name__iexact=query)|
							Q(street__iexact=query)| 
							Q(hnum__icontains=query)|
							Q(title__icontains=query)| #
							Q(saler__icontains=query) # blank True
							
									 
						)

		context = {
			'found_obj': (found_obj)
		}

		return render(self.request, self.template, context)

 
def error_404(request):
    context = RequestContext(request)
    response = render_to_response('error_404.html', context)
    response.status_code = 404
    return response
 
 
def error_500(request):
    context = RequestContext(request)
    response = render_to_response('error_500.html', context)
    response.status_code = 500
    return response

