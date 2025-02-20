from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.conf import settings
import os

def index(request):
    return render(request, 'budget_app/index.html')

@csrf_exempt
def update_budget(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # Will add Google Sheets integration here
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@csrf_exempt
def add_expense(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # Will add Google Sheets integration here
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@csrf_exempt
def sync_sheets(request):
    if request.method == 'GET':
        try:
            # Will add Google Sheets sync functionality here
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)