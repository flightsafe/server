from django.shortcuts import render

# Create your views here.
from django.urls import reverse


def open_api_view(request):
    url = reverse("spec")
    return render(request, "redoc/index.html", {"title": "Open API Schema", "spec": url})
