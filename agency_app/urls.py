from django.conf.urls import url, include
from agency_app.views import ( 
        CategoryListView, 
        DynamicCategoryImage, 
        ObjectDetailView, 
        CategoryDetailView,
        PagesDetailView,
        DynamicPageImage,
        ObjectListView,
        Searcher,
    )

urlpatterns = [
    # full category view of models
    url(r'^$', CategoryListView.as_view(), name='base_show'),

    url(r'^contact/', include('contact_form.urls', namespace='contact_form')),

    # detail view category lict from category-space
    url(r'^category/(?P<slug>[-\w]+)/$', CategoryDetailView.as_view(), name='category-detail'),

    url(r'^objects/', ObjectListView.as_view(), name='category-detail'),
    
    # detail view page from pages-pace (Pages)
    url(r'^service/(?P<slug>[-\w]+)/$', PagesDetailView.as_view(), name='service-detail'),
    
    # detail view object-page from same category
    url(r'^(?P<category>[-\w]+)/(?P<slug>[-\w]+)/$', ObjectDetailView.as_view(), name='object-detail'),
    
    # cftegory img URL 
    url(r'^show_category_image/$', DynamicCategoryImage.as_view(), name='category_image'),
    
    # detail page view
    url(r'^service/(?P<slug>[-\w]+)/$', PagesDetailView.as_view(), name='service-detail'),
    
    # page navigte images
    url(r'^page_image/$', DynamicPageImage.as_view(), name='page_image'),

    # search url
    url(r'^search_result/$', Searcher.as_view(), name="saerch_view"),


]
