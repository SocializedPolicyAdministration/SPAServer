from django.http import Http404, HttpResponse
from django.shortcuts import render

from models import RequestAssessment

# Create your views here.

def get_result_quality(request):
    if request.method != 'POST':
        return Http404
    users = request.POST['ids'].split(' ')
    requester = long(request.POST['requester'])
    content = request.POST['content']
    for user in users:
        ra = RequestAssessment(respondent=long(user), requester=requester, content=content)
        ra.save()
    return HttpResponse('ok')


