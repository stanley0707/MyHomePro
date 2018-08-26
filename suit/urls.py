from django.conf.urls import url, include
from django.conf import settings
from .views import SearcherAdmin

urlpatterns = [
    url(r'^search_result/$', SearcherAdmin.as_view(), name='search_view'),
]