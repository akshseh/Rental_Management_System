"""rental1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from rental_system import views 


urlpatterns = [
    url(r'^admin/',               admin.site.urls                     ),
    url(r'^$',                    views.home,             name="home"),
    url(r'^login$',               views.login_user,       name="login"),
    url(r'^login/dashboard$',     views.dashboard,        name="dashboard"),
    url(r'^login/ownerDashboard$',views.owner_dashboard,  name="ownerdashboard"),
    url(r'^dashboard$',           views.dashboard,        name="dashboard"),
    url(r'^register$',            views.register,         name="register"),
    url(r'^login/addProperty$',   views.add_property,     name="addProperty"),
    
]
