import time

from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import render

from datetime import datetime, timedelta

from CommunicationServer.models import Transaction
from MergeServer.models import Results
from ResultQuality.models import RequestAssessment
from Assessment.models import Assessment
from KeyManager.Util.Paillier import add, mul, sub
from KeyManager.Util.TimeCost import SPATime

# Create your views here.

def polling_key_manager(request):
    if request.method != 'POST':
        return Http404

    id = request.POST['id']
    if not id.isdigit():
        return HttpResponse("ok")

    id = long(id)

    reqs = Transaction.objects.filter(respondent=id)
    time_threshold = datetime.now() - timedelta(minutes=30)
    # setting_reqs = Results.objects.filter(requester=id, count__gt=3, start_time__lt=time_threshold)
    setting_reqs = Results.objects.filter(requester=id, count__gt=0)
    result_reqs = RequestAssessment.objects.filter(requester=id)
    # assess_reqs = Assessment.objects.filter(requester=id, count__gt=3, start_time__lt=time_threshold)
    assess_reqs = Assessment.objects.filter(requester=id, count__gt=0)
    if reqs.exists():
        req = reqs.first()
        to_respondent = ' '.join([str(req.request), req.weight, req.paillier_n, req.paillier_g,
                                  req.ope_key, req.settings, req.spa_policies])
        req.delete()
        return HttpResponse(to_respondent)
    elif setting_reqs.exists():
        start = time.time()
        values = setting_reqs[0].values.split(',')
        spa_policies = setting_reqs[0].spa_policies.split(',')
        settings = setting_reqs[0].settings.split(',')
        n_square = long(setting_reqs[0].n_square)
        size = len(values)
        return_req = [' '.join(spa_policies), ' '.join(settings)]
        for i in range(size):
            if spa_policies[i] == 'MajorityPreferred' or spa_policies[i] == 'MinorityPreferred':
                select_values = values[i].split(' ')
                select_values_len = len(select_values)
                relations = []

                for j in range(select_values_len):
                    for k in range(j + 1, select_values_len):
                        relations.append(str(sub(long(select_values[j])
                                                 , long(select_values[k])
                                                 , n_square)))
                return_req.append(' '.join(relations))
                # return_req.append(' '.join(select_values))
            elif spa_policies[i] == 'Average':
                return_req.append(values[i])
            else:
                pass
        setting_reqs.delete()
        end = time.time()
        SPATime(end - start)
        return HttpResponse('merged:' + ','.join(return_req))
    elif result_reqs.exists():
        requester = result_reqs[0].requester
        content = result_reqs[0].requester
        result_reqs.delete()
        return HttpResponse('result:' + requester + ': ' + content)
    elif assess_reqs.exists():
        suitable = 0
        malicious = 0
        unknow = 0
        for assess in assess_reqs:
            if assess.assess == 0:
                suitable += 1
            elif assess.assess == 1:
                malicious += 1
            else:
                unknow += 1
        return HttpResponse('assess:' + suitable + ',' + malicious + ',' + unknow)
    else:
        return HttpResponse('ok')

