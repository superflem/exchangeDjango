"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views, view_login

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', views.signup, name='signup'), # se il pecorso è '/signup/' esegue la view signup
    path('login/', view_login.login, name='login'), # se il pecorso è '/login/' esegue la view login
    path('query/', views.queryy, name='query'), # se il pecorso è '/query/' esegue la view query
    path('withdraw/', views.deposit_withdraw_buy, name='withdraw'), # se il pecorso è '/withdraw/' esegue la view withdraw
    path('deposit/', views.deposit_withdraw_buy, name='deposit'), # se il pecorso è '/deposit/' esegue la view deposit
    path('logout/', views.logout, name='logout'), # se il pecorso è '/logout/' esegue la view logout
    path('buy/', views.deposit_withdraw_buy, name='buy'), # se il pecorso è '/buy/' esegue la view buy
    path('listTransactions/', views.listTransactions, name='listTransactions'), # se il pecorso è '/listTransactions/' esegue la view listTransactions
    path('uploadImage/', views.uploadImage, name='uploadImage'), # se il pecorso è '/uploadImage/' esegue la view uploadImage
    path('getImage/', views.getImage, name='getImage'), # se il pecorso è '/getImage/' esegue la view getImage
    path('cambio/', views.cambio, name='cambio'), # se il pecorso è '/cambio/' esegue la view che restituisce il tasso di cambio attuale

]
