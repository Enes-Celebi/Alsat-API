import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from app.services.auth_service import signup, signin
import traceback

@csrf_exempt
def signup_view(request):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    try:
        data = json.loads(request.body)
        email = data.get("email")
        password = data.get("password")
        full_name = data.get("full_name", None)

        if not email or not password:
            return JsonResponse({"error": "Email and Password are required!"}, status=400)

        user = signup(email, password, full_name)
        return JsonResponse({"message": "User created successfully", "user_id": user.id}, status=201)

    except ValueError as e:
        return JsonResponse({"error": str(e)}, status=400)

    except Exception as e:
        error_details = {
            "error": "An unexpected error occurred.",
            "details": str(e),
            "traceback": traceback.format_exc() 
        }
        return JsonResponse(error_details, status=500)


def signin_view(request):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    try:
        data = json.loads(request.body)
        print("Received data:", data)  

        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return JsonResponse({"error": "Email and Password are required!"}, status=400)  

        user = signin(email, password)
        return JsonResponse({"message": "Login successful", "user_id": user.id}, status=200)

    except ValueError as e:
        return JsonResponse({"error": str(e)}, status=400)

    except Exception as e:
        error_details = {
            "error": "An unexpected error occurred.",
            "details": str(e),
            "traceback": traceback.format_exc() 
        }
        return JsonResponse(error_details, status=500)
