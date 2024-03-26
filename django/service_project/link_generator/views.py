from django.shortcuts import render

def generate_link(request):
    """ Страница с генератором ссылок. """
    return render(request, 'link_generator/link.html')