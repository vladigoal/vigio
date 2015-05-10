from django.views.generic import TemplateView
from .models import Brand

class BrandView(TemplateView):
    template_name = "brand.html"

    def get_context_data(self, **kwargs):
        context = super(BrandView, self).get_context_data(**kwargs)
        context['brands'] = Brand.objects.all()
        return context