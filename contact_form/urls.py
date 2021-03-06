from django.conf.urls import url

from contact_form import views, forms


app_name = 'contact_form'
urlpatterns = [
    url(r'^$', views.ContactFormView.as_view(
        template_name="contact.html",
        form_class=forms.BasicContactForm,
    ), name="contact"),


    url(r'^complted/$', 
        views.CompletedPage.as_view(
            template_name="contact_completed.html",
        ),
        name='completed'),
]



