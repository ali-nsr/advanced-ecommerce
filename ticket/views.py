from django.shortcuts import render, redirect, get_object_or_404, Http404
from .models import *
from .forms import TicketUserForm, TicketUserChatForm
from django.contrib import messages
from django.views import View


class TicketListView(View):
    def get(self, request):
        tickets = Ticket.objects.filter(user_id=request.user.id)
        context = {
            'tickets': tickets,
        }
        if request.user.is_authenticated:
            return render(request, 'accounts/profile/ticket_list.html', context)
        return redirect('home:home_page')


class TickerChatView(View):
    def get(self, request, ticket_pk):
        form = TicketUserChatForm(request.POST or None)
        ticket = get_object_or_404(Ticket, id=ticket_pk)
        tickets = TicketUser.objects.filter(ticket_id=ticket.id)
        if request.user.id == ticket.user.id:
            return render(request, 'accounts/profile/ticket_chat.html',
                          {'ticket': ticket, 'tickets': tickets, 'form': form, })
        else:
            return redirect('home:home_page')


class NewTicketView(View):
    def get(self, request):
        form = TicketUserForm(request.POST or None)
        context = {
            'form': form,
        }
        if request.user.is_authenticated:
            return render(request, 'accounts/profile/ticket_detail.html', context)
        return redirect('home:home_page')


class SendTicketView(View):
    def post(self, request):
        form = TicketUserForm(request.POST)
        if form.is_valid():
            ticket = Ticket.objects.create(user_id=request.user.id, title=form.cleaned_data['title'], status='open')
            TicketUser.objects.create(ticket_id=ticket.id, title=form.cleaned_data['title'],
                                      content=form.cleaned_data['content'])
            messages.success(request, 'تیکت شما با موفقیت ارسال شد')
            return redirect(request.META.get('HTTP_REFERER'))


class SendReplyView(View):
    def post(self, request, ticket_pk):
        ticket = get_object_or_404(Ticket, id=ticket_pk)
        if request.method == 'POST':
            ticket_form = TicketUserForm(request.POST or None)
            if ticket_form.is_valid():
                TicketUser.objects.create(ticket_id=ticket.id, content=ticket_form.cleaned_data['content'])
                messages.success(request, 'تیکت شما با موفقیت ارسال شد')
                return redirect(request.META.get('HTTP_REFERER'))

# def ticket_chat(request, ticket_pk):
#     form = TicketUserChatForm(request.POST or None)
#     ticket = get_object_or_404(Ticket, id=ticket_pk)
#     tickets = TicketUser.objects.filter(ticket_id=ticket.id)
#     if request.user.id == ticket.user.id:
#         return render(request, 'account/ticket_chat.html',
#                       {'ticket': ticket, 'tickets': tickets, 'form': form, })
#     else:
#         return redirect('home:home_page')


# def new_ticket(request):
#     form = TicketUserForm(request.POST or None)
#     context = {
#         'form': form,
#     }
#     return render(request, 'account/ticket_detail.html', context)

# def send_ticket(request):
#     if request.method == 'POST':
#         form = TicketUserForm(request.POST)
#         if form.is_valid():
#             ticket = Ticket.objects.create(user_id=request.user.id, title=form.cleaned_data['title'], status='open')
#             TicketUser.objects.create(ticket_id=ticket.id, title=form.cleaned_data['title'],
#                                       content=form.cleaned_data['content'])
#             messages.success(request, 'تیکت شما با موفقیت ارسال شد')
#             return redirect(request.META.get('HTTP_REFERER'))

# def ticket_reply(request, ticket_pk):
#     ticket = get_object_or_404(Ticket, id=ticket_pk)
#     if request.method == 'POST':
#         ticket_form = TicketUserForm(request.POST or None)
#         if ticket_form.is_valid():
#             TicketUser.objects.create(ticket_id=ticket.id, content=ticket_form.cleaned_data['content'])
#             messages.success(request, 'تیکت شما با موفقیت ارسال شد')
#             return redirect(request.META.get('HTTP_REFERER'))
