from django.shortcuts import render
from .models import Result

# Create your views here.


def index(request):

    return render(
        request,
        'cari/index.html',
    )
