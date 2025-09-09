import json
import pickle

from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from ... import helper_functions


def index_view(request):
    return render(request, "dist/index.html", {})


# User Authentication Views
@require_POST
def login_view(request):
    data = json.loads(request.body)
    username = data.get("username")
    password = data.get("password")

    if username is None or password is None:
        return JsonResponse(
            {"detail": "Please provide username and password."}, status=400
        )

    user = authenticate(username=username, password=password)

    if user is None:
        return JsonResponse({"detail": "Invalid credentials."}, status=400)

    login(request, user)
    return JsonResponse({"detail": "Successfully logged in."})


# User Authentication Views
@require_POST
def logout_view(request):
    if not request.user.is_authenticated:
        return JsonResponse({"detail": "You're not logged in."}, status=400)

    logout(request)
    return JsonResponse({"detail": "Successfully logged out."})


# CSRF Token View
@ensure_csrf_cookie
def session_view(request):
    if not request.user.is_authenticated:
        return JsonResponse({"isAuthenticated": False})

    return JsonResponse({"isAuthenticated": True})


# Who Am I View
def whoami_view(request):
    if not request.user.is_authenticated:
        return JsonResponse({"isAuthenticated": False})

    return JsonResponse({"username": request.user.username})


# File Upload and Processing View
@require_POST
def upload_file(request):
    if request.method == "POST" and request.FILES.get("file"):

        uploaded_file = request.FILES["file"]
        
        # Save file using Django's storage system
        filename = default_storage.save(f'temp/{uploaded_file.name}', ContentFile(uploaded_file.read()))
        file_path = default_storage.path(filename)

        # Parse PDB
        residue_data = helper_functions.parse_pdb(file_path)

        mean_plddt = residue_data.mean()
        if mean_plddt >= 90:
            mean_plddt_str = "Very High Average Confidence"
        elif mean_plddt >= 70:
            mean_plddt_str = "High Average Confidence"
        elif mean_plddt >= 50:
            mean_plddt_str = "Low Average Confidence"
        else:
            mean_plddt_str = "Very Low Average Confidence"

        with open('backend/ml_model/regressor_model.pkl', 'rb') as f:
            regressor_model = pickle.load(f)
        segments = helper_functions.find_low_confidence_segments(residue_data, threshold=70)
        max_segment = max(segments, key=len)
        X = [[
            residue_data.mean(),
            (residue_data < 50).mean() * 100,
            (residue_data < 70).mean() * 100,
            max_segment[-1] - max_segment[0]
        ]]
        score = regressor_model.predict(X)[0]

        notes = [mean_plddt_str]
        if X[0][1] >= 25:
            notes.append("Highly disordered")
        if sum(residue_data < 50) > 20:
            notes.append("Long disordered C-terminus")
        if max_segment[-1] - max_segment[0] < 10:
            notes.append("Well folded")

        response = {
            "approximate_ptm_score": round(score, 5),
            "median_plddt": round(residue_data.median(), 5),
            "metrics": {
                "mean_plddt": round(mean_plddt, 5),
                "percent_below_50": round((residue_data < 50).mean() * 100, 2),
                "percent_below_70": round((residue_data < 70).mean() * 100, 2),
                "longest_low_confidence_segment": [max_segment[0], max_segment[-1]]
            },
            "notes": notes
        }

        return JsonResponse(response)
    
    return JsonResponse({"error": "No file received"}, status=400)