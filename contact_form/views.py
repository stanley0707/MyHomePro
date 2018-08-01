from django.urls import reverse
from django.views.generic import TemplateView, CreateView, FormView


class CompletedPage(TemplateView):
    template_name = "contact_completed.html"


class ContactFormMixin(object):
    
    def form_valid(self, form):
        form.send_email(self.request)
        return super(ContactFormMixin, self).form_valid(form)

    def get_success_url(self):
        return reverse('contact_form:completed')


class ContactFormView(ContactFormMixin, FormView):
    pass


class ContactModelFormView(ContactFormMixin, CreateView):
    pass