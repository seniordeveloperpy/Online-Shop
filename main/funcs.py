from django.shortcuts import render, redirect

def staff_required(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_staff:
            result=func(request, *args, **kwargs)
        else:
            return redirect('front:index')
        return result
    return wrapper