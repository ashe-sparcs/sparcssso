#-*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.core.exceptions import SuspiciousOperation
from django.shortcuts import redirect
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from apps.oauth.models import AccessToken
import json
import os
import urllib


# Helper functions
def generate_token(user):
    while True:
        uid = os.urandom(10).encode('hex')
        if len(AccessToken.objects.filter(uid=uid)) == 0:
           token = AccessToken(uid=uid, user=user)
           token.save()
           return uid


@login_required
def require(request):
    uid = generate_token(request.user)
    callback = request.GET.get('callback', '')
    args = {
        'uid': uid,
    }
    return redirect(callback + '?' + urllib.urlencode(args))


def info(request):
    uid = request.GET.get('uid', '') 
    token = AccessToken.objects.filter(uid=uid).first()
    if token is None:
        raise Http404()

    user = token.user
    token.delete()

    resp = {}
    resp['username'] = user.username
    return HttpResponse(json.dumps(resp), content_type='application/json')