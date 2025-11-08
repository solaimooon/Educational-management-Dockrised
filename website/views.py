from django.shortcuts import render
from .models import *
def index(request):
    clips=clip.objects.all().order_by("-id")
    return render(request,'new_template/index.html',{"clips":clips})

def clip_view(request, slug):
    clip_media=clip.objects.get(slug=slug)
    return render(request, 'website/clip_single.html', {"clip": clip_media})
