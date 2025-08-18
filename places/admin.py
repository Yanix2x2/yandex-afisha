from django.contrib import admin
from django.utils.safestring import mark_safe
from adminsortable2.admin import SortableAdminBase, SortableInlineAdminMixin

from .models import Place, Image


class ImageInlineAdmin(SortableInlineAdminMixin, admin.TabularInline):
    model = Image
    extra = 1
    fields = ('image_preview', 'picture', 'serial_number')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.picture:
            return mark_safe(f'<img src="{obj.picture.url}" style="max-height: 200px;" />')
        return "No image"
    
    image_preview.short_description = "Preview"


@admin.register(Place)
class PlaceAdmin(SortableAdminBase, admin.ModelAdmin):
    inlines = [
        ImageInlineAdmin,
    ]


admin.site.register(Image)
