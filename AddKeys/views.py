from django.shortcuts import render

from django.http import HttpResponse, Http404
import json

from models import KeyManager

from KeyManager.Util.OPE import getOPEKey
from KeyManager.Util.Paillier import Paillier


# Create your views here.
def add_keys(request):
    if request.method != 'POST':
        return Http404
    phone = int(request.POST['id'])

    if KeyManager.objects.filter(phone=phone).exists():
        return HttpResponse("you got keys already!")

    paillier = Paillier(2048)
    ope = getOPEKey()

    def to_binary(num):
        return '{0:b}'.format(num)

    paillierPublic = ' '.join(map(to_binary, paillier.get_public_key()))
    paillierPrivate = ' '.join(map(to_binary, paillier.get_private_key()))
    opeKey = to_binary(ope)
    p = KeyManager(phone=phone, paillier_private=paillierPrivate, paillier_public=paillierPublic, ope_key=opeKey)
    p.save()
    keys = paillierPrivate + ' ' + paillierPrivate + ' ' + opeKey
    return HttpResponse(keys)


def polling_key_manager(request):
    if request.method != 'POST':
        return Http404
    print("polling_key_manager")
    return HttpResponse("ha")


def get_spa_request(request):
    if request.method != 'POST':
        return Http404
    json_data = json.load(request.body)

    return HttpResponse("ha")
