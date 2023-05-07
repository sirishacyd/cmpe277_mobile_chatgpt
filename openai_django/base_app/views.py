from django.shortcuts import render
from django.http import JsonResponse
from .oai_queries import get_completion
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def query_view(request):
    if request.method == 'POST':
        prompt = request.POST.get('prompt')
        response = get_completion(prompt)
        return JsonResponse({'response': response})
    return JsonResponse({'error': 'Invalid request method'}, status=405)
