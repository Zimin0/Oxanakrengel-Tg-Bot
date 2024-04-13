from django.shortcuts import render, HttpResponse, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
import json
from order.models import BotOrder

@csrf_exempt
def catch_yookassa_response(request):
    """ Улавливает ответы от Yookassa с информацией о заказах. """ 
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        _body = json.loads(body_unicode)
        print(_body)
        _yookassa_object = _body['object']
        payment_status = _yookassa_object['status']
        yookassa_id = _yookassa_object['id']
        django_id = _yookassa_object['metadata']['order_django_id']
        print(f"Статус: {payment_status} Yookassa_id: {yookassa_id}")

        order = get_object_or_404(BotOrder, id=django_id)
        order.payment_id = yookassa_id # сохраняем для удобства админа
        
        ## Обработка статуса заказа ##
        if payment_status == 'succeeded':
            order.status = 'was_paid'
            order.is_paid = True
        elif payment_status == 'canceled':
            order.status = 'canceled'

        order.save()

        return HttpResponse()
    
"""
{'type': 'notification', 'event': 'payment.succeeded', 'object': 
    {'id': '2dac6d98-000f-5000-8000-147368b6575d', 'status': 'succeeded', 'amount': 
        {'value': '1.00', 'currency': 'RUB'}, 
    'income_amount': {'value': '0.96', 'currency': 'RUB'}, 'description': 'Заказ №10 на сумму 1.0 rub', 'recipient': {'account_id': '368783', 'gateway_id': '2226690'}, 'payment_method': {'type': 'yoo_money', 'id': '2dac6d98-000f-5000-8000-147368b6575d', 'saved': False, 'title': 'YooMoney wallet 410011758831136', 'account_number': '410011758831136'}, 'captured_at': '2024-04-13T10:09:59.292Z', 'created_at': '2024-04-13T10:09:28.606Z', 'test': True, 'refunded_amount': {'value': '0.00', 'currency': 'RUB'}, 'paid': True, 'refundable': True, 'metadata': {'order_django_id': '10'}}}
"""

"""
{'type': 'notification', 'event': 'payment.succeeded', 'object': {'id': '2dac72f6-000f-5000-8000-16fcbfbe9e23', 'status': 'succeeded', 'amount': {'value': '15500.00', 'currency': 'RUB'}, 'income_amount': {'value': '14957.50', 'currency': 'RUB'}, 'description': 'Заказ №None на сумму 15500.0 rub', 'recipient': {'account_id': '368783', 'gateway_id': '2226690'}, 'payment_method': {'type': 'yoo_money', 'id': '2dac72f6-000f-5000-8000-16fcbfbe9e23', 'saved': False, 'title': 'YooMoney wallet 410011758831136', 'account_number': '410011758831136'}, 'captured_at': '2024-04-13T10:32:30.687Z', 'created_at': '2024-04-13T10:32:22.056Z', 'test': True, 'refunded_amount': {'value': '0.00', 'currency': 'RUB'}, 'paid': True, 'refundable': True, 'metadata': {}}}
"""