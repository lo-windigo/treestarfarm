from __future__ import unicode_literals

from django.contrib import admin

from mezzanine.core.admin import TabularDynamicInlineAdmin
from mezzanine.pages.admin import PageAdmin
from models import HerbGallery, Herb


class HerbGalleryAdmin(PageAdmin):

    class Media:
        css = {"all": ("mezzanine/css/admin/gallery.css",)}


admin.site.register(HerbGallery, HerbGalleryAdmin)
admin.site.register(Herb)
