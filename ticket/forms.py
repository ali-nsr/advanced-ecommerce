from django.forms import ModelForm
from .models import *


class TicketUserForm(ModelForm):
    class Meta:
        model = TicketUser
        fields = ['content', 'title']


class TicketUserChatForm(ModelForm):
    class Meta:
        model = TicketUser
        fields = ['content']
