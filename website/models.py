from django.db import models

class clip(models.Model):
    name=models.CharField(max_length=50,verbose_name="تیتر")
    file=models.FileField(upload_to='media/',
        verbose_name="فایل ")
    slug=models.CharField(max_length=50)
    image=models.ImageField(upload_to='media_night',
        default='null',
        verbose_name="تصویر نمایه")
    
    discription=models.CharField(max_length=2000)
    


    meta_title = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="عنوان سئو"
    )
    meta_description = models.TextField(
        blank=True,
        null=True,
        verbose_name="توضیحات سئو"
    )

    class Meta:
        verbose_name = " کلیپ"
        verbose_name_plural = " کلیپ ها"
# Create your models here.
