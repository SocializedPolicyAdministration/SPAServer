from django.http import Http404, HttpResponse
from django.shortcuts import render

from models import Assessment

# Create your views here.
def send_assessment(request):
    if request.method != 'POST':
        return Http404
    requester = long(request.POST['requester'])
    assessment = long(request.POST['assess'])
    ass = Assessment(requester=requester, assess=assessment)
    ass.save()
    return HttpResponse('ok')
