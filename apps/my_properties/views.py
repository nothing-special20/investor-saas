import os

from django.shortcuts import render
from django.core.files.storage import FileSystemStorage, default_storage

from .models import MyProperties

def index(request):
    my_properties = list(MyProperties.objects.all().values())[0]

    return render(request, 'my_properties/my_properties.html', {'my_properties': my_properties})

def add_property(request):
    return render(request, 'my_properties/add_property.html')

def add_property_upload(request):
    print(request.POST)
    print(request.FILES)
    pin = request.POST.get('pin')
    title = request.POST.get('title')
    property_details = request.POST.get('property-details')
    property_photos = request.FILES.getlist('property-photos')

    for photo in property_photos:
        fss = FileSystemStorage()
        file = fss.save(photo.name, photo)

    doc = MyProperties(
                PIN=pin,
                TITLE=title, 
                PROPERTY_DETAILS=property_details, 
                PROPERTY_PHOTOS=property_photos
                )
    doc.save()

    my_properties = list(MyProperties.objects.all().values())[0]
    
    return render(request, 'my_properties/my_properties.html', {'my_properties': my_properties})
