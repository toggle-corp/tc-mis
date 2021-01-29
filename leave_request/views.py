from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django_currentuser.middleware import get_current_authenticated_user

from .models import LeaveRequest, SendEmail


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

            content = "Your request has been approved from {start_date} to {end_date} ." \
                .format(start_date=leave_request_exist.start_date, end_date=leave_request_exist.end_date)
            html_content = render_to_string("email_template.html",
                                            {'name': leave_request_exist.verified_by, 'content': content})
            subject = "Your request has been approved."
            text_content = strip_tags(html_content)

            SendEmail.send_mail(subject, text_content, leave_request_exist.verified_by.email,
                                leave_request_exist.employee.email, html_content)

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

            decline_reasons = leave_request_exist.decline_reasons or ""
            content = "Your request has been rejected from {start_date} to {end_date}. {decline_reasons}" \
                .format(start_date=leave_request_exist.start_date, end_date=leave_request_exist.end_date,
                        decline_reasons=decline_reasons)
            html_content = render_to_string("email_template.html", {'name': request.user, 'content': content})
            subject = "Your request has been rejected."
            text_content = strip_tags(html_content)
            SendEmail.send_mail(subject, text_content, leave_request_exist.verified_by.email,
                                leave_request_exist.employee.email, html_content)
            return redirect('/admin/leave_request/request')
    return render(request, 'reject.html')
