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
		1:' объект',
		2:' объекта',
		3:' объектов'
	}
		
	if num % 10 == 1:
		d_des = str(num) + description.get(1)
		return d_des
	
	elif 1 < num  % 10 < 5:
		d_des = str(num) + description.get(2)
		return d_des
	
	else:
		d_des = str(num) + description.get(3)
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
	
	def __init__(self, found_obj_query, query_set):
		self.found_obj_query = found_obj_query
		self.query_set = query_set

	
	def __writer(key, value):
		memory = open('agency_app/memory.json', 'w')
		data = dict(zip(key, value))
		json.dump(data, memory, indent=4, ensure_ascii=False)

	
	
	def __query_to_json(query_set):
		memory = open('agency_app/memory.json', 'r')
		memory = json.loads(memory.read())
		
		
		for element in memory.keys():
			if set(memory[element]).intersection(set(query_set)):
				pass

	
	def __item_to_json():
		memory = open('agency_app/memory.json', 'w')
		
		data = []
		
		for i in City.objects.all():
			data.append(i.name) # if i.name.split() == 1 else data.append(i.name.split())

		for i in Category.objects.all():
			data.append(i.name) # if i.name.split() == 1 else data.append(i.name.split())
		
		for i in Appointement.objects.all():
			data.append(i.appointment.lower()) # if i.appointment.split() == 1 else data.append(i.appointment.split())

		for i in Agent.objects.all():
			data.append(i.first_name)

	
		
		value = [(
			
				value[0:-1] + 'а',
				value[0:-1] + 'ы',
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
				value[0:-1] + 'ая',
				value[0:-1] + 'ок',
				value[0:-1] + 'р',
				value[0:-1] + 'ра',
				value[0:-1] + 'ре',
				value[0:-1] + 'д',
				value[0:-1] + 'де',
				value[0:-1] + 'с',
				value[0:-1] + 'у',
				value[0:-1] + 'ный',
				value[0:-1] + 'дской',
				value[0:-1] + 'ь',
				value[0:-1] + 'ии',
		
		) for value in data]

		return Query_Selector.__writer(data, value)

	def query_replace(query):
		
		query_out = []
		query_set = []
		
		query_list = query.split()
		
		query_set.append(query.title()) 
		query_set.append(query.upper())
		query_set.append(query.lower())
		
		i = len(query_list)
		
		for q in query_list:
			
			query_set.append(''.join(q.title().split()))
			query_set.append(''.join(q.upper().split()))
			query_set.append(''.join(q.lower().split()))
			
			query_set.append(' '.join(query_list[0:i]))
			i-=1

		Query_Selector.__item_to_json()
		Query_Selector.__query_to_json(query_set)
		
		memory = open('agency_app/memory.json', 'r')
		memory = json.loads(memory.read())
		
		try:
			if int(query):
				query_out.append(query)
		
		except ValueError:	
			for element in memory.keys():
				if set(memory[element]).intersection(set(query_set)):
					query_out.append(element)

		return ' '.join(query_out)
		
	def query_out(found_obj_query, query_set):
		found_obj = []
		if found_obj_query:
			for q_item in found_obj_query:
				found_obj.append(q_item)



		for value_set in found_obj:
			if set(str(query_set).split()).difference(str(value_set).split()):
				indx = found_obj.index(value_set)
				del found_obj[indx]

		return found_obj




class Searcher(View):
	template = "search.html"

	def __init__(self):
		self.found_obj = []
		self.query = ''	 

	def get(self, request, *args, **kwargs):
		query = self.request.GET.get('q') 
		res = query
		
		query_set = Query_Selector.query_replace(query)
			
		for query_s in query_set.split():
			
			found_obj_query = Property.objects.filter(
			
				Q(id_prop__icontains=query_s)|
				Q(category__name__icontains=query_s)|
				Q(appointment__appointment__icontains=query_s)|
				Q(agent__first_name__icontains=query_s)|
				Q(agent__last_name__icontains=query_s)|
				Q(city__name__iexact=query_s)|
				Q(street__iexact=query_s)| 
				Q(hnum__icontains=query_s)|
				Q(area__icontains=query_s)|
				Q(areafield__icontains=query_s)|
				Q(flor__icontains=query_s)|
				Q(title__icontains=query_s)|
				Q(desc__icontains=query_s)|
				Q(saler__icontains=query_s)
			
			)
		
		try:
			if found_obj_query:
				self.found_obj = Query_Selector.query_out(found_obj_query, query_set)
		
		except UnboundLocalError:
			self.found_obj = []
		
		print(self.found_obj)
		
		num = len([i for i in self.found_obj])
		num = deviation(num)
			
		context = {
				'articles': (self.found_obj),
				'categories': Category.objects.all(),
				'qu': res,
				'word': num,
				'main_media': Advertising.objects.all(),
				'cities': City.objects.all(),
				'question': Qeustions.objects.all(),
				'appointment': Appointement.objects.all(),
			}

		return render(self.request, self.template, context)
	