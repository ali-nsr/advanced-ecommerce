from django.urls import path
from . import views
from .forms import ResetPasswordEmailValidation

app_name = 'accounts'
urlpatterns = [
    # authenticate
    path('register', views.RegisterView.as_view(), name='register_page'),
    path('register-verify', views.verify_register, name='verify_register'),
    path('resend-sms', views.resent_sms, name='resent_sms'),
    path('login', views.LoginView.as_view(), name='login_page'),
    path('logout', views.LogoutView.as_view(), name='logout_page'),

    # reset password phone
    path('forgot-password', views.forgot_password, name='forgot_password'),
    path('reset-password/<user_temp_code>', views.reset_password, name='reset_password'),

    # change password
    path('change-password', views.ChangePasswordView.as_view(), name='change_password'),

    # reset password email
    path('reset', views.ResetPasswordView.as_view(form_class=ResetPasswordEmailValidation),
         name='reset_password_email'),
    path('reset/done', views.ResetPasswordDoneView.as_view(), name='reset_password_done_email'),
    path('confirm/<uidb64>/<token>/', views.ResetPasswordConfirmView.as_view(), name='reset_password_confirm_email'),
    path('confirm/done', views.ResetPasswordCompleteView.as_view(), name='reset_password_complete_email'),

    # profile
    path('dashboard', views.DashboardView.as_view(), name='dashboard'),
    path('orders', views.OrderListView.as_view(), name='order_list'),
    path('favourite', views.FavouriteListView.as_view(), name='favourite'),
    path('comments', views.CommentsListView.as_view(), name='comments'),
    path('comments/<commentId>', views.comment_delete, name='comment_delete'),
    path('profile-info', views.ProfileInfoView.as_view(), name='profile_info'),
    # path('order-detail', views.OrderDetailView.as_view(), name='order_detail'),

    # delete order by user
    path('order-delete/<orderId>', views.order_delete, name='order_delete'),
    path('order-update/<orderId>', views.order_update, name='order_update'),
]
