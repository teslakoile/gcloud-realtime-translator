from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

def index(request):
    return render(request, "myapp/index.html")

@csrf_exempt
def start_recording(request):
    # Your recording code goes here, or call the function that does it
    # Remember, it should return the result or store it somewhere that
    # stop_recording can access it
    return JsonResponse({'success': True})

@csrf_exempt
def stop_recording(request):
    # Your code to stop the recording goes here
    return JsonResponse({'success': True})
