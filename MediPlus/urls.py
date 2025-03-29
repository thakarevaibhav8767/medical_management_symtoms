"""
URL configuration for MediPlus project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from app1 import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),
    path('aboutus/',views.aboutus,name='aboutus'),
    path('contactus/',views.contactus,name='contactus'),
    path('register/',views.registerfrm,name='register'),
    path('symtoms/',views.symtoms,name='symtoms'),
    path('userlogin/',views.userlogin, name='userlogin'),
    path('uwelcome/',views.uwelcome,name='uwelcome'),
    path('awelcome/',views.awelcome,name='uwelcome'),
    path('adminlogin/',views.adminlogin,name='adminlogin'),
    path('insertmed/',views.insertmed,name='insertmed'),
    path('updatemed/',views.updatemed,name='updatemed'),
    path('deleterec/',views.deleterec,name='deleterec'),
    path('display/',views.display,name='display'),
    path('purchase/',views.purchase_med,name='purchase'),
    path('search/',views.search,name='search'),
    path('diseas/',views.diseas_1,name='diseas'),
    path('orderhist/',views.purchasehist,name='orderhist')

]
