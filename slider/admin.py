from django.contrib import admin
from .models import *


class SliderHomeAdmin(admin.ModelAdmin):
    list_display = ('id', 'url', 'image_tag')


admin.site.register(SliderHome, SliderHomeAdmin)
admin.site.register(SliderHomeOffer)
admin.site.register(SliderOfferDate)
admin.site.register(BlogSlider)
