from django.urls import path
from .views import UploadAudioView, TrainModelView, PredictView

urlpatterns = [
    path("upload/", UploadAudioView.as_view()),
    path("train/", TrainModelView.as_view()),
    path("predict/", PredictView.as_view()),
]
