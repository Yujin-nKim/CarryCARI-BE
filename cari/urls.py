from django.urls import path
from .views import ResultDetail

urlpatterns = [
    path('cari/result', ResultDetail.as_view())
]
