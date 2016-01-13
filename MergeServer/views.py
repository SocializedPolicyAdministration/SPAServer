from django.shortcuts import render
from django.http import HttpResponse, Http404

from MergeServer.models import Results
from KeyManager.Util.Paillier import mul, add

from CommunicationServer.models import Transaction

# Create your views here.

def get_merge_response(request):
    if request.method != 'POST':
        return Http404
    values = request.POST['values'].split(',')
    requester = request.POST['requester']
    requester_number = long(requester)
    respondent = request.POST['respondent']
    paillier_n = long(request.POST['paillier_n'])
    n_square = paillier_n * paillier_n
    paillier_g = long(request.POST['paillier_g'])
    spa_policies = request.POST['spa_policies'].split(',')
    settings = request.POST['settings']
    size = len(spa_policies)

    results = Results.objects.filter(requester=requester_number)
    if results.exists():
        result = results[0].values.split(',')
        count = results[0].count
        new_result = []
        for i in range(size):
            if spa_policies[i] == 'Average':
                [this_value, this_weight] = result[i].split(' ')
                [sum_value, sum_weight] = values[i].split(' ')
                this_result = str(add(long(this_value), long(sum_value), n_square)) \
                              + ' ' + str(add(long(this_weight), long(sum_weight), n_square))
                new_result.append(this_result)
            if spa_policies[i] == 'MaximumValue' or spa_policies[i] == 'MinimumValue':
                this_result = result[i] + ' ' + values[i]
                new_result.append(this_result)
            if spa_policies[i] == 'MajorityPreferred' or spa_policies[i] == 'MinorityPreferred':
                this_result = []
                this_values = values[i].split(' ')
                result_element = result[i].split(' ')
                this_size = len(result_element)
                for j in range(this_size):
                    ans = add(long(this_values[j]), long(result_element[j]), n_square)
                    this_result.append(str(ans))
                new_result.append(' '.join(this_result))
        results.update(values=','.join(new_result), count=count + 1)
    else:
        r = Results(values=request.POST['values']
                    , requester=requester_number
                    , spa_policies=request.POST['spa_policies']
                    , n_square=n_square
                    , settings=settings)
        r.save()


    return HttpResponse('ok')

