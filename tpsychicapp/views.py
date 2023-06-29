# example/views.py
from datetime import datetime

from django.http import HttpResponse


from django.shortcuts import render, redirect
from django.http import HttpResponse
from tpsychicapp.aphantasia import getDoc,autoco,sentimentAnalysis
from tpsychicapp.models import Ledger as Transactions
import datetime
import requests as req
import json

from rest_framework.decorators import api_view, permission_classes
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework_api_key.models import APIKey
from rest_framework_api_key.permissions import  HasAPIKey
from googletrans import Translator, constants
from pprint import pprint
from datetime import datetime, timedelta,date
import base64
from django.views.decorators.csrf import csrf_protect

def index(request):
    now = datetime.now()
    html = f'''
    <html>
        <body>
            <h1>Hello from Vercel!</h1>
            <p>The current time is { now }.</p>
        </body>
    </html>
    '''
    return HttpResponse(html)

def getAccessToken():
    clientId = "AWmyihi1ip94nQebSLHuF1f8Lw18KL8-HLQX32NgICo4ZFQepQwIN195664eoEUWACxjtMy5C8Jq2G9W"
    appSecret = "EAOQzJCPIWcT5uiBiyWSluRjC-ymxrVnVEO9W3LK-eTxYkqxpiUhgCS7TzrGIYYPTiLSWVKKIwiAQv3o"
    url = "https://api-m.sandbox.paypal.com/v1/oauth2/token"
    secret = clientId + ":" + appSecret
    asciistr=secret.encode('ascii')
    base64bytes = base64.b64encode(asciistr)
    base64str=base64bytes.decode('ascii')
    headers={'Authorization':f"Basic {base64str}",}
    response=req.post(url,data= "grant_type=client_credentials",headers=headers)
    data=response.json()
    return data['access_token']
def updatePayment(request):
    data=json.loads(request.body)
    res=capturePayment(data)
    api_key, key = APIKey.objects.create_key(name="my-remote-service")
    today = date.today()
    expiry  = today + timedelta(days=30)
    transcation = Transactions(email = request.user.email,date=today,amount=data['amt'],expiry=expiry,userid=request.user.id,api_key=api_key,package=data['package'],tokens=10000)
    transcation.save()
    return HttpResponse(json.dumps({'api_key':key}))
def capturePayment(data):
    orderID = data['orderID']
    token=getAccessToken()
    token=f'Bearer {token}'
    print(token)
    url = f'https://api-m.sandbox.paypal.com/v2/checkout/orders/{orderID}/capture'
    print(url)
    headers={'Authorization': token,'Content-Type': 'application/json'}
    response = req.post(url=url,headers=headers)
    return response


def createOrder(request):
    data=json.loads(request.body)
    amt=data['amt']
    token=getAccessToken()
    url = "https://api-m.sandbox.paypal.com/v2/checkout/orders"
    token=f'Bearer {token}'
    headers = {'Authorization': token,'Content-Type': 'application/json'}
    payload={'intent' : 'CAPTURE','purchase_units': [{'amount': {'currency_code': 'USD','value': amt,},},]}
    response = req.post(url=url,json=payload, headers=headers)
    print(response.json())
    return HttpResponse(response)

class TokenSerializer(serializers.Serializer):

    data=serializers.CharField(max_length=200)
    created= serializers.DateTimeField()

class Token(object):
    def __init__(self,data, created = None):
        self.data=data
        self.created=created or datetime.now()

def home(request):
    return render(request, 'index.html')

def guides(request):
    if request.user.is_authenticated:
        #try:
        #    transaction = Transactions.objects.get(email=request.user.email)
            ##show apis
        #    return render(request ,'keys.html',{'transcation':transcation})
        #except Transactions.DoesNotExist:
            ##show checkoutpage
        #    api_key, key = APIKey.objects.create_key(name="my-remote-service")
        #    today = date.today()
        #    expiry  = today + timedelta(days=30)
        #    transcation = Transactions(email = request.user.email,date=today,amount=35,expiry=expiry,userid=request.user.id,api_key=api_key)
        #    transcation.save()
            ##return render(request, 'apis.html',{'key':key,'transcation':transcation}) 
        return render(request, 'guides.html')

def pricing(request):
    return render(request, 'pricing.html')
def dev(request):
    return render(request, 'devCheckout.html')
def bs(request):
    return render(request,'bsCheckout.html')
def bsc(request):
    return render(request, 'bscCheckout.html')

@api_view(['GET'])
@permission_classes([HasAPIKey])
def websumm(request):
    url = request.GET['url']
    ans=getDoc(url)
    #content = Token(data=ans)
    #serializer = TokenSerializer(content)
    return Response(ans)

@api_view(['GET'])
@permission_classes([HasAPIKey])
def autoCorrect(request):
    text = request.GET['text']
    ans=autoco(text)
    return Response(ans)

#@api_view(['GET'])
#@permission_classes([HasAPIKey|Check_API_KEY])
def sentiment(request):
    text = request.GET['text']
    ans=sentimentAnalysis(text)
    return Response(ans)

@api_view(['GET'])
@permission_classes([HasAPIKey])
def langdetect(request):
    text = request.GET['text']
    trans=Translator()
    translation= trans.detect(text)
    ans={'lang':translation.lang,
        'confidence':translation.confidence
        }
    return Response(ans)

@api_view(['GET'])
@permission_classes([HasAPIKey])
def langtranslate(request):
    text = request.GET['text']
    des=request.GET['dest']
    trans=Translator()
    translation= trans.translate(text,dest=des)
    data=f"{translation.origin} ({translation.src}) --> {translation.text} ({translation.dest})"
    return Response(ans)