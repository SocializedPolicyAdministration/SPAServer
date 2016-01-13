from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import render

from datetime import datetime, timedelta

from CommunicationServer.models import Transaction
from MergeServer.models import Results
from KeyManager.Util.Paillier import add, mul, sub

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
    setting_reqs = Results.objects.filter(requester=id, count__gt=3)
    if reqs.exists():
        req = reqs.first()
        to_respondent = ' '.join([str(req.request), req.weight, req.paillier_n, req.paillier_g,
                                  req.ope_key, req.settings, req.spa_policies])
        req.delete()
        return HttpResponse(to_respondent)
    elif setting_reqs.exists():
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
        return HttpResponse('merged:' + ','.join(return_req))
    else:
        return HttpResponse('ok')

