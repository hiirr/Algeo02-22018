import os
import time
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.views.generic.edit import FormView
from .forms import ImageUploadForm, ImageSearchForm
from .models import ImageDataSet, ImageSearch
from django.core.paginator import Paginator
from django.core.files.storage import FileSystemStorage
from .CollectData import read_to_collect_vector, read_image
from .CBIR_Texture import process_chedec, compare
from .CBIR_Colour import rgb_to_hsv, cosine_similarity_block

search_time = 0
upload_time = 0

imageSearchTexture = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
imageSearchColor = [1.0, 1.0, 1.0]

imageDataTexture = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
imageDataColor = [1.0, 1.0, 1.0]

# Create your views here.
def home(request):
    global search_time
    global upload_time

    search_image = None
    if ImageSearch.objects.count() > 0:
        search_image = ImageSearch.objects.get()
    images = ImageDataSet.objects.filter(similarity__gt=60)
    p = Paginator(ImageDataSet.objects.order_by('-similarity').filter(similarity__gt=60), 6)
    page = request.GET.get('page')
    image_list = p.get_page(page)

    context = {
        "images" : images,
        "search_image" : search_image,
        "image_list" : image_list,
        "upload_time" : upload_time,
        "search_time" : search_time
    }
    return render(request, "cbir/home.html", context)

def upload_search(request):
    global imageSearchTexture
    global imageSearchColor

    if request.method == "POST":
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Process the form data
            file = request.FILES.get('file')
            fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, "image_search"))
            saved_file = fs.save(file.name, file)
            image_url = os.path.join("image_search", saved_file)

            image_path = os.path.join(settings.MEDIA_ROOT, "image_search", saved_file)
            search_texture, search_color = read_to_collect_vector(image_path)

            for i in range(6):
                imageSearchTexture[i] = search_texture[i]
            
            for i in range(3):
                imageSearchColor[i] = search_color[i]

            instance = ImageSearch(image=image_url)
            instance.save()
            return redirect(reverse('home'))
        
    return JsonResponse({"Pesan" : "Gagal"})

def search_cbir(request):
    global imageSearchColor
    global imageSearchTexture
    global imageDataColor
    global imageDataTexture
    global search_time

    start = time.time()

    if request.method == "POST":
        search = request.POST.get('search_cbir')
        image_data = ImageDataSet.objects.all()
        if search == "tekstur":
            for data in image_data:
                imageDataTexture = process_chedec(read_image(os.path.join(settings.MEDIA_ROOT, str(data.image))))
                sim = compare(imageDataTexture, imageSearchTexture)
                sim = round(sim, 2)
                data.similarity = sim
                data.save()
        else:
            for data in image_data:
                imageDataColor = rgb_to_hsv(read_image(os.path.join(settings.MEDIA_ROOT, str(data.image))))
                sim = cosine_similarity_block(imageDataColor, imageSearchColor, 10, 4)
                sim = round(sim, 2)
                data.similarity = sim
                data.save()
        end = time.time()
        search_time = round(end - start, 5)
        return redirect(reverse('home'))

def upload_dataset(request):
    global upload_time

    if request.method == "POST":
        start = time.time()
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            files = request.FILES.getlist('file')
            for file in files:
                fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, "image_data"))
                saved_file = fs.save(file.name, file)
                image_url = os.path.join("image_data", saved_file)

                image_path = os.path.join(settings.MEDIA_ROOT, "image_data", saved_file)

                instance = ImageDataSet(image=image_url)
                instance.save()
            end = time.time()
            upload_time = round(end-start, 5)
            
            return redirect('home')
        else:
            return JsonResponse({"pesan" : form.errors})
        
                
    return JsonResponse({"pesan" : "Upload gagal"})
        
def refresh(request):
    global imageSearchColor
    global imageSearchTexture
    global imageDataColor
    global imageDataTexture
    global exe_time
    global search_time

    if request.method == "POST":
        imageSearchTexture = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
        imageSearchColor = [1.0, 1.0, 1.0]
        imageDataTexture = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
        imageDataColor = [1.0, 1.0, 1.0]
        exe_time = 0
        search_time = 0

        ImageDataSet.objects.all().delete()
        ImageSearch.objects.all().delete()

        return redirect(reverse('home'))

def konsep_singkat(request):
    return render(request, "cbir/konsep-singkat.html")

def how_to_use(request):
    return render(request, "cbir/how-to-use.html")

def about_us(request):
    return render(request, "cbir/about-us.html")
