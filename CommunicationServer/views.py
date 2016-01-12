from django.http import Http404, HttpResponse
from django.shortcuts import render

import json

from models import Transaction

# Create your views here.
def get_spa_request(request):
    if request.method != 'POST':
        return Http404
    raw_j = request.POST['content']
    json_data = json.loads(raw_j)
    policies = ','.join(json_data['policies'])
    settings = ','.join(json_data['settings'])

    if Transaction.objects.filter(request=json_data['requester']).exists():
        return HttpResponse('You have send request')

    for i in range(0, len(json_data['respondents'])):
        Transaction(request=long(json_data['requester']), respondent=long(json_data['respondents'][i])
                    , paillier_n=json_data['paillier_n'], paillier_g=json_data['paillier_g']
                    , ope_key=json_data['ope_key'], weight=json_data['weights'][i]
                    , settings=settings, spa_policies=policies).save()

    return HttpResponse("ok")
