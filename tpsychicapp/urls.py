# example/urls.py
from django.urls import path

from tpsychicapp import views


urlpatterns = [
    path('home',views.home),
    path('',views.home),
    path('guides',views.guides),
    path('pricing',views.pricing),
    path('bscCheckout',views.bsc),
    path('bsCheckout',views.bs),
    path('devCheckout',views.dev),
    path('createOrder',views.createOrder),

    path('orders', views.createOrder),
    path('orders/capture',views.updatePayment),
    path('websumm',views.websumm),
    path('correct',views.autoCorrect),
    path('sentiment', views.sentiment),
    path('langdetect',views.langdetect),
    path('langtranslate',views.langtranslate),

    ##path('embeddings',views.embeddings),
    ##path('tokenization',views.tokenization),
    ##path('pos',views.pos),
    ##path('lemma',views.lemma),
    
    ##path('getsummary',views.summary),
    ##path('text2image', views.textToImage),
    
    ##path('entityextract',views.entityextract),
    
    ##path('headlinegen', views.headlinegen),
    ##path('blogpostgen', views.blogpostgen),
    
]