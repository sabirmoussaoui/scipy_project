from django.urls import path, include, re_path
from django.conf.urls import  url
from . import views

urlpatterns = [
     path('index/', views.index, name='index'),
    #route (processing Images)
         path('processingImg/', views.processingImg, name='processingImg'),
         path('getProcessingImage/', views.getProcessingImage, name='getProcessingImage'),
    # route (Optimisation)
         path('showNuage/', views.showNuage, name='showNuage'),
         path('getModel', views.getModel,name='getModel'),
    # route (Minimisation)
         path('showCurve/', views.showCurve, name='showCurve'),
         path('getMinimumValue/', views.getMinimumValue, name='getMinimumValue'),
 # route (Minimisation)
         path('getSignalTrend/', views.getSignalTrend, name='getSignalTrend'),
         path('getSignalDetrend/', views.getSignalDetrend, name='getSignalDetrend')
          ]
