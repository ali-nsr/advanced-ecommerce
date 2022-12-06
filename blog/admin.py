from django.contrib import admin
from .models import *

admin.site.register(Article)
admin.site.register(BlogCategory)
admin.site.register(BlogTag)
admin.site.register(BlogComment)
