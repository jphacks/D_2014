from django.contrib.auth import logout
from django.shortcuts import redirect


def logoutfunc(request):
    logout(request)
    return redirect('esuits:index')
