from django.urls import path
from . views import SendMessageView

urlpatterns = [
    path('<receiver>/', SendMessageView.as_view(), name='send-msg'),
    ]
