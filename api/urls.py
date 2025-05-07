from django.urls import path
from .views import UploadAudioView, TrainModelView, PredictView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("upload/", UploadAudioView.as_view()),
    path("train/", TrainModelView.as_view()),
    path("predict/", PredictView.as_view()),
]
if settings.DEBUG:  # هذا فقط في بيئة التطوير
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
