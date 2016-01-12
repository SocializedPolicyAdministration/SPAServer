from django.shortcuts import render
from django.http import HttpResponse, Http404

# Create your views here.

def get_merge_response(request):
    if request.method != 'POST':
        return Http404
    print request.POST['values']
    print request.POST['requester']
    return HttpResponse('ok')

