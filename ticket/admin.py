from django.contrib import admin
from .models import Ticket, TicketUser


class TicketUserInline(admin.StackedInline):
    model = TicketUser
    fields = ('content', 'reply', 'reply_created_date', 'ticketUserStatus',)
    extra = 0
    readonly_fields = ('content',)


class TicketAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'status', 'jalali_created_date')
    list_editable = ('status',)
    list_filter = ('status',)
    readonly_fields = ('title', 'user')
    inlines = [TicketUserInline]


class TicketUserAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'ticketUserStatus', 'jalali_created_date')
    readonly_fields = ('title', 'ticket', 'content', 'ticketUserStatus')


admin.site.register(Ticket, TicketAdmin)
admin.site.register(TicketUser, TicketUserAdmin)
