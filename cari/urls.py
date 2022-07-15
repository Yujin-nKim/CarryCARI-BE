from django.urls import path
from .views import ResultDetail, UserInfo
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('cari/image', UserInfo.as_view(), name='cari_image'),
    path('cari/result', ResultDetail.as_view(), name='cari_result')
]

# image conversion
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)