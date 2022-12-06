from django.shortcuts import render, redirect, HttpResponseRedirect
from django.views import View
from .forms import RegisterForm, LoginForm, VerifyRegistrationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import UpdateView
from django.contrib import messages
from random import randint
from ippanel import Client
from core.settings import SMS_API_KEY
from .models import User
from .forms import ForgotPasswordForm, VerifyResetPassword, ChangePasswordForm
from django.utils.crypto import get_random_string
from django.contrib.auth.decorators import login_required
# email auth imports
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
# orders imports
from order.models import Order
from store.models import Comment

api_key = SMS_API_KEY
sms = Client(api_key)


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        context = {
            'form': register_form
        }
        if request.user.is_authenticated:
            return redirect('store:home_page')
        return render(request, 'accounts/register_page.html', context)

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            data = register_form.cleaned_data
            user = User(first_name=data['first_name_form'],
                        last_name=data['last_name_form'],
                        email=data['email_form'], phone=data['phone_number_form'],
                        password=data['confirm_password_form'])
            user.set_password(data['confirm_password_form'])
            user.save()
            login(request, user)
            verify_code = randint(1111, 9999)
            request.session['verify_auth'] = verify_code
            pattern_values = {
                "code": f"{verify_code}",
            }
            sms.send_pattern(
                "your pattern code",
                f"your number",
                f"{user.phone}",
                pattern_values,
            )
            print(request.session['verify_auth'])
            messages.success(request,
                             f'ثبت نام شما با موفقیت انجام شد. لطفا برای فعالسازی کد تایید برای شماره {user.phone} را وارد کنید.')
            return redirect('accounts:verify_register')


def verify_register(request):
    if request.method == 'POST':
        form = VerifyRegistrationForm(request.POST)
        if form.is_valid():
            verify_code = form.cleaned_data['code']
            verify_session = request.session['verify_auth']
            if verify_code == verify_session:
                user = request.user
                if not user.is_verify:
                    user.is_verify = True
                    user.save()
                    del verify_session
                    messages.success(request, 'ثبت نام شما با موفقیت انجام شد.')
                    return render(request, 'accounts/register_done.html')
                else:
                    messages.info(request, 'شما کاربر تایید شده هستید.')
                    return redirect('accounts:verify_register')
            else:
                messages.warning(request, 'کد تایید صحیح نمیباشد.')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        form = VerifyRegistrationForm()
        return render(request, 'accounts/verify_code_auth.html', {'form': form})


def resent_sms(request):
    if not request.user.is_verify:
        verify_code = randint(1111, 9999)
        request.session['verify_auth'] = verify_code
        pattern_values = {
            "code": f"{request.session['verify_auth']}",
        }
        sms.send_pattern(
            "5drzq2t5yg5akmh",
            f"3000505",
            f"{request.user.phone}",
            pattern_values,
        )
        messages.success(request, f'کد فعالسازی دوباره برای {request.user.phone} ارسال شد.')
        return redirect('accounts:verify_register')
    else:
        messages.info(request, 'کاربر گرامی شما تایید شده اید. میتوانید از خدمات همتا گیم استفاده نمایید.')
        return redirect('accounts:verify_register')


def forgot_password(request):
    form = ForgotPasswordForm()
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            user_phone_number = form.cleaned_data['phone_number_form']
            user = User.objects.filter(phone__iexact=user_phone_number).first()
            if user is not None:
                reset_password_code = randint(111111, 999999)
                request.session['reset_password_session'] = reset_password_code
                user.temp_code = get_random_string(250)
                user.save()
                # send verify reset password sms here
                print(reset_password_code)
                messages.success(request, f'کد بازیابی رمز عبور برای شماره {user.phone} ارسال شد.')
                return redirect('accounts:reset_password', user.temp_code)
    return render(request, 'accounts/forgot_password_phone_page.html', {'form': form})


def reset_password(request, user_temp_code):
    the_user = User.objects.get(temp_code__iexact=user_temp_code)
    temp_code = the_user.temp_code
    form = VerifyResetPassword()
    if request.method == 'POST':
        form = VerifyResetPassword(request.POST)
        if form.is_valid():
            reset_password_code = form.cleaned_data['reset_password_code']
            confirm_reset_password_form = form.cleaned_data['confirm_reset_password_form']
            verify_reset_password = request.session['reset_password_session']
            if verify_reset_password == reset_password_code:
                the_user.set_password(confirm_reset_password_form)
                the_user.temp_code = None
                the_user.save()
                del request.session['reset_password_session']
                messages.success(request, f'رمز عبور شما تغییر یافت.')
                return redirect('accounts:login_page')
            else:
                messages.warning(request, 'کد تایید اشتباه است.')
                return redirect(request.META.get('HTTP_REFERER'))
    return render(request, 'accounts/reset_password_phone_page.html', {'form': form, 'temp_code': temp_code})


class ResetPasswordView(auth_views.PasswordResetView):
    template_name = 'accounts/reset_password_page.html'
    success_url = reverse_lazy('accounts:reset_password_done_email')
    email_template_name = 'accounts/link.html'


class ResetPasswordDoneView(auth_views.PasswordResetDoneView):
    template_name = 'accounts/reset_password_done_page.html'


class ResetPasswordConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'accounts/reset_password_confirm_page.html'
    success_url = reverse_lazy('accounts:reset_password_complete_email')


class ResetPasswordCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'accounts/reset_password_complete_page.html'


class LoginView(View):
    def get(self, request):
        login_form = LoginForm()
        context = {
            'login_form': login_form,
        }
        if request.user.is_authenticated:
            return redirect('store:home_page')
        return render(request, 'accounts/login_page.html', context)

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            data = login_form.cleaned_data
            user = authenticate(phone=data['phone_number_form'], password=data['password_form'])
            if user is not None:
                login(request, user)
                messages.success(request, 'با موفقیت به حساب خود وارد شدید.')
                return redirect('store:home_page')
        else:
            print('error')
        context = {
            'login_form': login_form,
        }
        return render(request, 'accounts/login_page.html', context)


class LogoutView(View):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
            messages.success(request, 'با موفقیت از حساب خود خارج شدید.')
            return redirect('accounts:login_page')


class DashboardView(View):
    def get(self, request):
        user = request.user
        if user.is_verify:
            context = {
                'user': user,
                'favorite_products': request.user.favourites_user.all(),
            }
            return render(request, 'accounts/profile/dashboard.html', context)
        messages.warning(request, 'کاربر گرامی لطفا شماره تلفن خود را تایید کنید.')
        return redirect('store:home_page')


class OrderListView(View):
    def get(self, request):
        user_id = request.user.id
        paid_orders = Order.objects.filter(user_id=user_id, status='P').order_by('-id')
        sending_orders = Order.objects.filter(user_id=user_id, status='S').order_by('-id')
        received_orders = Order.objects.filter(user_id=user_id, status='R').order_by('-id')
        canceled_orders = Order.objects.filter(user_id=user_id, is_paid=False).order_by('-id')
        context = {
            'paid_orders': paid_orders,
            'sending_orders': sending_orders,
            'received_orders': received_orders,
            'canceled_orders': canceled_orders,
        }
        if request.user.is_authenticated:
            return render(request, 'accounts/profile/profile_orders_page.html', context)
        return redirect('home:home_page')


class FavouriteListView(View):
    def get(self, request):
        if request.user.is_authenticated and request.user.is_verify:
            products = request.user.favourites_user.all()
            count = products.count()
            print(count)
            return render(request, 'accounts/profile/favourite.html', {'products': products})
        else:
            return redirect('accounts:login_page')

class CommentsListView(View):
    def get(self, request):
        comments = Comment.objects.filter(user_id=request.user.id)
        return render(request, 'accounts/profile/profile_comments.html', {'comments': comments})


@login_required
def comment_delete(request, commentId):
    if request.method == 'POST':
        Comment.objects.get(user_id=request.user.id, id=commentId).delete()
        messages.success(request, 'کامنت شما حذف شد.')
        return redirect(request.META.get('HTTP_REFERER'))


class ProfileInfoView(SuccessMessageMixin, UpdateView):
    from django.urls import reverse_lazy
    from .forms import ProfileForm
    form_class = ProfileForm
    model = User
    success_url = reverse_lazy('accounts:profile_info')
    success_message = 'بروز رسانی با موفقیت انجام شد'
    template_name = 'accounts/profile/profile_info.html'

    def get_object(self, queryset=None):
        return User.objects.get(pk=self.request.user.pk)


class ChangePasswordView(View):
    def get(self, request):
        context = {
            'form': ChangePasswordForm()
        }
        return render(request, 'accounts/profile/profile_change_password.html', context)

    def post(self, request):
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            user = User.objects.filter(id=request.user.id).first()
            current_password = form.cleaned_data.get('current_password')
            confirm_new_password = form.cleaned_data.get('confirm_new_password')
            if user.check_password(current_password):
                user.set_password(confirm_new_password)
                user.save()
                logout(request)
                messages.success(request,
                                 'رمز عبور جدید شما با موفقیت ثبت شد. اکنون با رمز عبور جدید به حساب خود وارد شوید.')
                return redirect('accounts:login_page')
            else:
                form.add_error('current_password', 'رمز عبور اشتباه است.')
        context = {
            'form': form
        }
        return render(request, 'accounts/profile/profile_change_password.html', context)


@login_required
def order_delete(request, orderId):
    Order.objects.get(id=orderId, user_id=request.user.id, is_paid=False).delete()
    messages.success(request, 'سفارش شما حذف شد.')
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def order_update(request, orderId):
    order = Order.objects.get(id=orderId, user_id=request.user.id, is_paid=False)
    if request.method == 'POST':
        for item in order.item_orders.all():
            item.price = item.variant.total_price
            item.unit_price = item.variant.unit_price
            item.discount = item.variant.discount_variant
            item.save()
            order.save()
        return redirect(request.META.get('HTTP_REFERER'))
