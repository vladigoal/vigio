# -*- coding: utf-8 -*-
from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from models import Product, Color, Size, Category, Collection, \
    ProductImage, Care, Status, Lookbook, LookbookImage
from django import forms
from sorl.thumbnail.admin import AdminImageMixin


class ProductImageInline(admin.StackedInline):
# class ProductImageInline(admin.TabularInline):
    model = ProductImage
    max_num=10
    extra=0


class ProductImageAdmin(AdminImageMixin, admin.ModelAdmin):
  pass

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', )

    inlines = [ProductImageInline,]

    class Media:
        js = [
             '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
             '/static/grappelli/tinymce_setup/tinymce_setup.js',
        ]
        css = {
            'all': ('/static/css/admin_custom.css',)
        }
    # list_filter = ["tm_created", ('tm_created', DateRangeFilter), isWinnerFilter, forRandomOrg]

    # fieldsets = (
    #     (None, {
    #         'fields': ('name', )
    #     }),
    #     ('Advanced options', {
    #         'classes': ('collapse',),
    #         'fields': ('price',)
    #     }),
    # )

    def image_thumb(self):
        return 'oops'


class ColorAdmin(admin.ModelAdmin):
    list_display = ('name',)


class SizeAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_category')

    def get_category(self, obj):
        return "\n".join([p.name for p in obj.category.all()])


class LookbookImageInline(admin.StackedInline):
    model = LookbookImage
    max_num=10
    extra=0
    # form = LookbookImageForm


class LookbookImageAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = ('get_thumbnail_html', 'lookbook')
    list_display_links = ('get_thumbnail_html', )
    ordering = ('lookbook',)


class LookbookAdmin(admin.ModelAdmin):
    list_display = ('name', )

    # inlines = [LookbookImageInline,]

# class LookbookImageAdmin(admin.ModelAdmin):
#     list_display = ('get_thumbnail_html', 'image')
#     list_display_links = ('get_thumbnail_html', 'image')


admin.site.register(Color, ColorAdmin)
admin.site.register(Size, SizeAdmin)
admin.site.register(Category, MPTTModelAdmin)
admin.site.register(Collection)
admin.site.register(Product, ProductAdmin)
admin.site.register(Care)
admin.site.register(Status)
admin.site.register(Lookbook, LookbookAdmin)
admin.site.register(LookbookImage, LookbookImageAdmin)
