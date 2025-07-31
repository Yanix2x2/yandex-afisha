from django.shortcuts import render


def show_affiches(request):
    return render(request, 'index.html')
