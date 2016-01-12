from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import render

from CommunicationServer.models import Transaction

# Create your views here.

def polling_key_manager(request):
    if request.method != 'POST':
        return Http404

    id = request.POST['id']
    if not id.isdigit():
        return HttpResponse("ok")

    id = long(id)

    if Transaction.objects.filter(respondent=id).exists():
        obj = Transaction.objects.get(respondent=id)
        to_respondent = ' '.join([str(obj.request), obj.weight, obj.paillier_n, obj.paillier_g,
                                  obj.ope_key, obj.settings])
        #obj.delete()
        return HttpResponse(to_respondent)
    else:
        return HttpResponse("ok")

