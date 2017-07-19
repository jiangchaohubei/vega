from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect

@csrf_protect
def index(request):
    context = {}
    context['index'] = 'this is index!'
    return render(request, 'templates/index.html', context)

def main(request):
    context = {}
    context['index'] = 'this is index!'
    return render(request, 'templates/pages/main.html', context)