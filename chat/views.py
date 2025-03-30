from django.shortcuts import render, get_object_or_404
from . forms import messageForm
from . models import Chat
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User

class SendMessageView(LoginRequiredMixin, CreateView):
    model = Chat
    fields = ['message']

    def form_valid(self, form):
        form.instance.sender = self.request.user
        form.instance.receiver = get_object_or_404(User, username=self.kwargs.get('receiver'))
        super().form_valid(form)
        message = form.instance
        message.save()
        return super().form_valid(form)
