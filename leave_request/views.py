from django.http import JsonResponse
from django.shortcuts import render
from django_currentuser.middleware import get_current_authenticated_user

from .models import LeaveRequest


def actions(request):
    if request.is_ajax and request.method == 'POST':
        _id = request.POST['id']
        status = request.POST['status']
        leave_request_exist = LeaveRequest.objects.get(id=_id)
        if leave_request_exist:
            leave_request_exist.status = status
            leave_request_exist.verified_by = get_current_authenticated_user()
            leave_request_exist.save()
            return JsonResponse({"msg": "SUCCESS"})
        else:
            return JsonResponse({"msg": "NOID"})

    else:
        return JsonResponse({"msg": "ERROR"})


def reject(request):
    if request.method == "POST":
        _id = request.POST['id']
        status = 0
        decline_reasons = request.POST['decline_reasons']
        leave_request_exist = LeaveRequest.objects.get(id=_id)
        if leave_request_exist:
            leave_request_exist.status = status
            leave_request_exist.decline_reasons = decline_reasons
            leave_request_exist.verified_by = get_current_authenticated_user()
            leave_request_exist.save()
            return JsonResponse({"msg": "SUCCESS"})
    return render(request, 'reject.html')
