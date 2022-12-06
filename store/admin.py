from django.contrib import admin
from .models import *
import admin_thumbnails
from compare.models import Compare


class CompareInline(admin.TabularInline):
    model = Compare
    extra = 1


class ProductVariantInline(admin.TabularInline):
    model = Variants
    extra = 1


class VariantsAdmin(admin.ModelAdmin):
    ...


@admin_thumbnails.thumbnail('image')
class GalleryInline(admin.TabularInline):
    model = Gallery
    extra = 1


class SpecificationsInline(admin.TabularInline):
    model = Specifications
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'unit_price', 'total_price', 'is_available', 'category_to_str',
        'size_and_color',
        'jalali_created_date',
        'jalali_updated_date', 'image_tag',
    )
    inlines = (ProductVariantInline, GalleryInline, SpecificationsInline, CompareInline)
    filter_horizontal = ('category',)

    def category_to_str(self, obj):
        # another way to join cats in admin
        # return " | ".join([category.title for category in obj.category.all()])
        return [category.title for category in obj.category.get_published_categories().all()]

    category_to_str.short_description = 'دسته بندی'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'status', 'position', 'parent')
    list_editable = ('position', 'parent')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'title', 'rate')


class GalleryAdmin(admin.ModelAdmin):
    list_display = ('product', 'title', 'image_tag')


admin.site.register(Color)
admin.site.register(Size)
admin.site.register(Variants, VariantsAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Gallery, GalleryAdmin)
admin.site.register(Brand)
admin.site.register(Position)
