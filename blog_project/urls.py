"""blog_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.contrib.auth import views as auth_views
#from . import views
from django.urls import path, include
from users import views as user_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('register',user_views.register,name='register'),
    path('login/',auth_views.LoginView.as_view(template_name='users/login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='users/logout.html'),name='logout'),
    path('profile/',user_views.profile,name='user-profile'),
    path('ajax/validate_username/',user_views.validate_username, name='validate_username'),
    path('',include(('blogs.urls','blogs'),namespace='blogs')),
    path('verify-email/',user_views.send_verification_mail,name='verify-mail'),
    path('user-account/',user_views.user_account,name='user-account'),
    path('password-reset/',user_views.send_password_reset_mail,name='password-reset'),
    path('verify-otp/',user_views.verify_otp,name='verify-otp'),
    path('chat/',include(('chat.urls','chat'),namespace='chat')),
    path('order/',include(('order.urls','order'),namespace='order')),
    path('accounts/', include('allauth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# ,name='password_reset_done'
# ,name='password_reset_confirm'
#,name='password_reset_complete'
