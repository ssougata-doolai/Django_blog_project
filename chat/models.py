from django.db import models
from django.utils import timezone
from django.urls import reverse

class Chat(models.Model):
    sender = models.ForeignKey('auth.User', on_delete = models.CASCADE, related_name='sender')
    receiver = models.ForeignKey('auth.User', on_delete = models.CASCADE, related_name='receiver')
    message = models.CharField(max_length=250, null=False, blank=False)
    time = models.TimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('chat:send-msg', kwargs={'receiver':self.receiver.username})

    def __str__(self):
        return self.message
