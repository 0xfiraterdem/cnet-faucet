from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import FaucetRequest
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from django.http import JsonResponse

import requests

@api_view(['POST'])
def faucet(request):
    recaptcha_response = request.data.get('recaptcha')
    data = {
        'secret': settings.RECAPTCHA_PRIVATE_KEY,
        'response': recaptcha_response
    }
    r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
    result = r.json()

    if not result.get('success'):
        return Response({
            'error': 'Invalid reCAPTCHA. Please try again.'},
            status=status.HTTP_400_BAD_REQUEST)

    wallet_address = request.data.get('wallet_address')

    faucet_request = FaucetRequest.objects.filter(wallet_address=wallet_address).first()

    if faucet_request:
        now = timezone.now()
        elapsed_time = now - faucet_request.request_time
        if elapsed_time < timedelta(hours=24):
            remaining_time = timedelta(hours=24) - elapsed_time
            hours, remainder = divmod(remaining_time.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            return Response({
                'error': f'You can only request once every 24 hours.\n{hours}:{minutes}:{seconds} left'
            },status=status.HTTP_429_TOO_MANY_REQUESTS)

    if not faucet_request:
        faucet_request = FaucetRequest(wallet_address=wallet_address, request_time=timezone.now())
    else:
        faucet_request.request_time = timezone.now()

    # Transaction gönderme işlevini çağırma
    from .send_cnet import send_transaction
    send_transaction(wallet_address)

    faucet_request.save()

    return Response({
        'success': 'Tokens sent successfully.'},
        status=status.HTTP_200_OK)

def custom_404(request, exception=None):
    return JsonResponse({'error': 'Not Found'}, status=404)
