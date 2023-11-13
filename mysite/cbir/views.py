from django.shortcuts import render
from django.urls import reverse
from django.views.generic.edit import FormView
from .forms import FileFieldForm
from .models import ImageDataSet, ImageSearch
from django.core.paginator import Paginator

# Create your views here.
def home(request):
    images = ImageDataSet.objects.filter(similarity__gt=0.6)
    p = Paginator(ImageDataSet.objects.order_by('-similarity').filter(similarity__gt=0.6), 1)
    page = request.GET.get('page')
    image_list = p.get_page(page)

    context = {
        "images" : images,
        "image_list" : image_list
    }
    return render(request, "cbir/home.html", context)

def konsep_singkat(request):
    return render(request, "cbir/konsep-singkat.html")

def how_to_use(request):
    return render(request, "cbir/how-to-use.html")

def about_us(request):
    return render(request, "cbir/about-us.html")

def upload_data(request):
    if request.method == 'POST':
        image_upload = request.FILES.getlist('image')
        image_data = ImageDataSet.objects.create(
            image = image_upload
        )
