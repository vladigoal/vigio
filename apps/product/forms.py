from django import forms
from .models import ProductImage, LookbookImage




class ProductImageForm(forms.ModelForm):

        class Meta:
            model = ProductImage

        def image_thumb(self, clean_data):
            return 'oops'
#         size = clean_data.get('size')
#         return self.product.variants.get(size=size,
#                                          product__color=self.product.color)



