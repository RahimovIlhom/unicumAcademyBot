from django.shortcuts import redirect


def redirect_admin(request):
    return redirect('/admin')
