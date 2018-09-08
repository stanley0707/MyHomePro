from functools import wraps
from django.db.models import F
from agency_app.models import PropertyStatistic, Property
from django.db import DatabaseError, transaction
#from agency_app.views import ObjectDetailView

def counted(f):
	@wraps(f)
	def decorator(request, *args, **kwargs):
		with transaction.atomic():
			counter, created = PropertyStatistic.objects.get_or_create(count_id=request.object.id)
			counter.views = F('views') + 1
			counter.url = F('count') + request.object.title
			counter.save()

			counter2, created2 = Property.objects.get_or_create(id=request.object.id)
			counter2.coun = F('coun') + 1
			counter2.save()
		return f(request, *args, **kwargs)
	return decorator