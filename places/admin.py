from django.contrib import admin
from django.utils.html import format_html
from adminsortable2.admin import SortableAdminBase, SortableInlineAdminMixin

from .models import Place, Image


class ImageInlineAdmin(SortableInlineAdminMixin, admin.TabularInline):
    model = Image
    extra = 1
    fields = ('image_preview', 'picture', 'serial_number')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.picture:
            return format_html(
                '<img src="{}" style="max-height: 200px; max-width: 200px;" />',
                obj.picture.url
            )

        return "No image"
    
    image_preview.short_description = "Preview"


@admin.register(Place)
class PlaceAdmin(SortableAdminBase, admin.ModelAdmin):
    inlines = [
        ImageInlineAdmin,
    ]


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    raw_id_fields = ['place']
    ordering = ['serial_number']
