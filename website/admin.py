# admin.py
from django.contrib import admin
from django import forms
from django.utils.html import format_html
from .models import clip  # حتماً با حرف بزرگ!


# فرم سفارشی برای Textarea
class ClipAdminForm(forms.ModelForm):
    class Meta:
        model = clip
        fields = '__all__'
        widgets = {
            'discription': forms.Textarea(attrs={
                'rows': 5,
                'cols': 60,
                'placeholder': 'توضیحات کامل کلیپ را اینجا وارد کنید...',
                'class': 'vLargeTextField'
            }),
        }


@admin.register(clip)
class ClipAdmin(admin.ModelAdmin):
    form = ClipAdminForm  # استفاده از فرم سفارشی

    list_display = (
        "name",
        "slug",
        "meta_title",
        "image_preview",
    )

    search_fields = ("name", "slug", "meta_title", "meta_description")
    prepopulated_fields = {"slug": ("name",)}

    fieldsets = (
        ("اطلاعات اصلی", {
            "fields": ("name", "file", "image", "discription")
        }),
        ("سئو", {
            "classes": ("collapse",),
            "fields": ("meta_title", "meta_description"),
        }),
        ("سایر", {
            "fields": ("slug",),
        }),
    )

    readonly_fields = ("image_preview",)

    # پیش‌نمایش امن تصویر
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="100" height="60" style="border-radius:8px; object-fit:cover;" />',
                obj.image.url
            )
        return "بدون تصویر"

    image_preview.short_description = "پیش‌نمایش"


# تنظیمات پنل ادمین
admin.site.site_header = "پنل مدیریتی کانون میراث النبی (ص)"
admin.site.site_title = "مدیریت رسانه‌ها"
admin.site.index_title = "داشبورد مدیریت"