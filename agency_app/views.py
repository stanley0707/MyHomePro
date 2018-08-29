import json
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
		Appointement,
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

def deviation(num):

	description = {
		1:'объект',
		2:'объекта',
		3:'объектов'
	}
		
	if num % 10 == 1:
		d_des = description.get(1)
		return d_des
	elif 1 < num  % 10 < 5:
		d_des = description.get(2)
		return d_des
	else:
		d_des = description.get(3)
		return d_des


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


class CategoryListView(ListView, CategoryListMixin):
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


class Query_Selector:
	def __init__(self, query):
		self.query = query


	@staticmethod
	def queries_to_json(query):
		memory = open('agency_app/memory.json', 'w')
		
		data = []
		
		for i in City.objects.all():
			data.append(i.name)


		value = [(
			value[0:-1] + 'и',
			value[0:-1] + 'ей',
			value[0:-1] + 'ой',
			value[0:-1] + 'ю',
			value[0:-1] + 'е',
			value[0:-1] + 'ах',
			value[0:-1] + 'ами',
			value[0:-1] + 'я',
			value[0:-1] + 'ем',
			value[0:-1] + 'ом',
			value[0:-1] + 'а',
		) for value in data]

		data = dict(zip(data, value))
		
		json.dump(data, memory, indent=4, ensure_ascii=False)

		return data

	@classmethod
	def query_replace(cls, query):
		memory = open('agency_app/memory.json', 'r')
		memory = json.loads(memory.read())
		
		t = query.title().split()
		for t in t:
			d = []
			d.append(t)

		item = dict(memory.items())
		
		for element in item.keys():
			if set(item[element]) & set(d):
				return element


class Searcher(View):
	def __init__(self):
		self.found_obj = []
		self.query = ''	
	template = "search.html"


	def get(self, request, *args, **kwargs):
		query = self.request.GET.get('q')
		res = query
		data = Query_Selector.queries_to_json(query)
		e = Query_Selector.query_replace(query)
		
		# регистронезависимый поиск одного слова
		query_set = [
			[''.join(query.upper())],
			[''.join(query.lower())],
			[''.join(query.title())]
		]
		
		# регистронезависимый поиск более чем одного слова
		if len(query.title().split()) > 1:
			query_set = [
				query.upper().split(),
				query.lower().split(),
				query.title().split(),
				[query.upper()],
				[query.lower()],
				[query.title()]
			]
		
		for query_s in query_set: # цикл экземпляров списке вариантов регистра
			for q in query_s: # список слов в запросе в цикле! = q
				q = '' if len(q) == 1 else q # запрос правда, если в нем более одного символа иначе он пустая строка!
				found_obj_query = Property.objects.filter(
					Q(id_prop__icontains=q)|
					Q(category__name__icontains=q)|
					Q(appointment__appointment__icontains=q)|
					Q(agent__first_name__icontains=q)|
					Q(agent__last_name__icontains=q)|
					Q(city__name__iexact=q)|
					Q(street__iexact=q)| 
					Q(hnum__icontains=q)|
					Q(area__icontains=q)|
					Q(areafield__icontains=q)|
					Q(flor__icontains=q)|
					Q(title__icontains=q)|
					Q(desc__icontains=q)|
					Q(saler__icontains=q)
				)
				
				if found_obj_query:
					self.found_obj = found_obj_query
				else:
					query_s.append(e)
						


		num = len([i for i in self.found_obj])
		num = deviation(num)
		
		context = {
			'articles': (self.found_obj),
			'categories': Category.objects.all(),
			'qu': (res),
			'word': num,
			'main_media': Advertising.objects.all(),
			'cities': City.objects.all(),
			'question': Qeustions.objects.all(),
			'appointment': Appointement.objects.all(),
		}
		
		return render(self.request, self.template, context)



