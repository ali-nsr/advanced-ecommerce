from django.urls import path
from . import views

app_name = 'ticket'
urlpatterns = [
    path('tickets', views.TicketListView.as_view(), name='ticket_list'),
    path('new-ticket', views.NewTicketView.as_view(), name='new_ticket'),
    path('ticket/<ticket_pk>', views.TickerChatView.as_view(), name='ticket_chat'),
    path('send-ticket', views.SendTicketView.as_view(), name='send_ticket'),
    path('ticket-reply/<ticket_pk>', views.SendReplyView.as_view(), name='ticket_reply'),
]
