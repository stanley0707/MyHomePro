from django.shortcuts import render
from agency_app.models import Pages, Category, Agent, Property, Images, Advertising, City
from django.db.models import Q
from django.views import View

class SearcherAdmin(View):
    template = "admin/search_result.html"

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
