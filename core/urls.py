from django.views.generic import TemplateView
from django.urls import path
from .views import logout,login, regiser
# URLConf
urlpatterns = [
    path('', TemplateView.as_view(template_name='core/index.html'),name='home'),
    path('about-us', TemplateView.as_view(template_name='core/pages/about_us.html'),name='about-us'),
    path('contact-us', TemplateView.as_view(template_name='core/pages/contact_us.html'),name='contact-us'),
    path('register', regiser,name='register'),
    path('login', login,name='login'),
    path('logout',logout, name='logout')
]
