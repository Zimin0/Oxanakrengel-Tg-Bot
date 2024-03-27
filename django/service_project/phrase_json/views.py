from django.http import JsonResponse, HttpResponseNotFound
from .models import BotPhrases
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
import os

from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def get_bot_phrases(request):
    try:
        bot_phrase = BotPhrases.objects.first()
        if bot_phrase:
            file_path = bot_phrase.phrases.path
            with open(file_path, 'r', encoding='utf-8') as file:
                data = file.read()
                return JsonResponse(data, safe=False, json_dumps_params={'indent': 2})  # safe=False для разрешения объектов верхнего уровня
        return HttpResponseNotFound("Файл с фразами не найден.")
    except ObjectDoesNotExist:
        return HttpResponseNotFound("Запись не найдена.")
    except Exception as e:
        return Response({'error': str(e)}, status=400)
