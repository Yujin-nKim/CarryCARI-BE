from django.urls import path
from .views import ResultDetail, UserInfo

urlpatterns = [
    path('cari/image', UserInfo.as_view()),
    path('cari/result', ResultDetail.as_view())
]
