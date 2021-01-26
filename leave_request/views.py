from django.http import JsonResponse
from django.shortcuts import render,redirect
from django_currentuser.middleware import get_current_authenticated_user

from .models import LeaveRequest


def actions(request):
    if request.is_ajax and request.method == 'POST':
        _id = request.POST['id']
        status = LeaveRequest.STATUSES.ACTIVE
        if request.POST['status'] == "reject":
            status = LeaveRequest.STATUSES.INACTIVE
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
        decline_reasons = request.POST['decline_reasons']
        leave_request_exist = LeaveRequest.objects.get(id=_id)
        if leave_request_exist:
            leave_request_exist.status = LeaveRequest.STATUSES.INACTIVE
            leave_request_exist.decline_reasons = decline_reasons
            leave_request_exist.verified_by = get_current_authenticated_user()
            leave_request_exist.save()
            return redirect('/admin/leave_request/request')
    return render(request, 'reject.html')
