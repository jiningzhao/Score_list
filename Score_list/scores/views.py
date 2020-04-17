from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
from scores.models import ScoreList
import json


def index(request):
    return HttpResponse("Hello Django!")


def update_score(request):
    if request.POST:

        customer_id, score = int(request.POST.get("customer_id")), int(request.POST.get("score"))
        if customer_id not in [i.get('customer_id') for i in ScoreList.objects.all().values('customer_id')]:
            print("customer_id不在数据库中,插入数据customer_id:{},score:{}".format(customer_id, score))
            ScoreList.objects.create(customer_id=customer_id, score=score)
        else:
            print("customer_id:{}在数据库中,修改数据库score:{}".format(customer_id, score))
            ScoreList.objects.filter(customer_id=customer_id).update(score=score)
        return JsonResponse({"customer_id": customer_id, "score": score})
    else:
        return render(request, "update_score.html")


def select_list(request):
    if request.GET:
        begin = int(request.GET.get("begin"))
        off = int(request.GET.get("off"))
        customer_id = int(request.GET.get("customer_id"))
        score_list = sorted(list(ScoreList.objects.all().values_list('customer_id', 'score')), key=lambda x: x[1],
                            reverse=False)[begin:off+1]

        customer = [i for i in list(ScoreList.objects.all().values_list("customer_id", "score")) if i[0] == customer_id][0]

        print(customer)
        if customer_id not in [i.get('customer_id') for i in ScoreList.objects.all().values('customer_id')]:
            return HttpResponse("数据不存在，请返回后重新输入！")
        else:
            print(score_list)
            return JsonResponse({'code': 200, 'msg': "查询成功！", "rows": score_list, "customer": customer})
    else:
        return render(request, "select_list.html")

