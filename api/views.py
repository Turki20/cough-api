from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import pandas as pd
import os
import joblib
from .utils import extract_features
from sklearn.neighbors import KNeighborsClassifier
from django.core.files.storage import default_storage

CSV_FILE = "dataset.csv"
MODEL_FILE = "model.pkl"

class UploadAudioView(APIView):
    def post(self, request):
        label = request.data.get("label")
        files = request.FILES.getlist("audio_file")

        if not files or not label:
            return Response({"error": "يرجى رفع ملف صوتي وتحديد التصنيف"}, status=400)

        rows = []
        for file in files:
            path = default_storage.save("temp.wav", file)
            features = extract_features(path)
            features["label"] = label
            rows.append(features)

        df = pd.DataFrame(rows)
        if os.path.exists(CSV_FILE):
            df.to_csv(CSV_FILE, mode='a', index=False, header=False)
        else:
            df.to_csv(CSV_FILE, index=False)

        return Response({"message": f"تم حفظ {len(rows)} ملف/ملفات كـ '{label}'"})


class TrainModelView(APIView):
    def post(self, request):
        if not os.path.exists(CSV_FILE):
            return Response({"message": "لا يوجد بيانات لتدريب النموذج"}, status=400)

        df = pd.read_csv(CSV_FILE)
        X = df.drop("label", axis=1)
        y = df["label"]

        model = KNeighborsClassifier(n_neighbors=3)
        model.fit(X, y)
        joblib.dump(model, MODEL_FILE)

        return Response({"message": "تم تدريب النموذج وحفظه"})


class PredictView(APIView):
    def post(self, request):
        file = request.FILES.get("audio_file")
        if not file or not os.path.exists(MODEL_FILE):
            return Response({"error": "تأكد أنك قمت برفع الملف الصحيح .wav"}, status=400)

        path = default_storage.save("temp.wav", file)
        full_path = default_storage.path(path)
        features = extract_features(full_path)
        X = pd.DataFrame([features])

        model = joblib.load(MODEL_FILE)
        prediction = model.predict(X)[0]
        label_ar = "مصاب" if prediction == "infected" else "غير مصاب"

        default_storage.delete(path)
        return Response({"result": f"{label_ar}"})

