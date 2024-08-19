from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm

from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # User should be inactive until activated
            user.save()

            # Generate activation token and UID
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            domain = get_current_site(request).domain

            # Generate activation link
            activation_link = f"http://{domain}/users/activate/{uid}/{token}/"
            message = render_to_string('users/activation_email.html', {
                'user': user,
                'domain': domain,
                'uid': uid,
                'token': token,
                'activation_link': activation_link,
            })

            # Send activation email
            email = EmailMessage(
                subject='Activate Your Account',
                body=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[user.email],
            )
            email.content_subtype = "html"  # This tells Django to treat the email content as HTML
            email.send()

            # Send email to admin
            admin_email = settings.ADMIN_EMAIL  # Ensure this is set in settings.py
            admin_message = render_to_string('users/admin_notification_email.html', {
                'user': user,
            })
            admin_email = EmailMessage(
                subject='New User Registration',
                body=admin_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[admin_email],
            )
            admin_email.content_subtype = "html"  # This tells Django to treat the email content as HTML
            admin_email.send()

            return redirect('users/registration_pending')  # Inform user to check their email
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

def activate(request, uidb64, token):
    uid = force_str(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=uid)
    if default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)  # Automatically log in the user after activation
        return redirect('users/registration_successful')  # Redirect to the registration successful page
    else:
        return redirect('users/registration_failed')  # Redirect to a failure page if the token is invalid


from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required

from django.shortcuts import redirect
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.is_superuser:
                return redirect('admin:index')  # Redirect to Django admin for superuser
            elif user.groups.filter(name='warehouse_managers').exists():
                return redirect('warehouse_manager_dashboard') 
            elif user.groups.filter(name='warehouse_staff').exists():
                return redirect('warehouse_staff_dashboard') # Redirect to warehouse manager dashboard
            else:
                return redirect('unauthorized')  # Redirect to a default page for other users
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


def registration_successful(request):
    return render(request, 'users/registration_successful.html')

def registration_pending(request):
    return render(request, 'users/registration_pending.html')  # A new page to inform users to check their email

def registration_failed(request):
    return render(request, 'users/registration_failed.html')  # A new page to inform users of activation failure

def admin_login(request):
    return redirect(reverse('admin:index'))

from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test

# Check if the user is a warehouse manager
#def is_warehouse_manager(user):
#    return user.groups.filter(name='warehouse_managers').exists()

#@login_required
#@user_passes_test(is_warehouse_manager)
#def warehouse_manager_dashboard(request):
#   return render(request, 'users/warehouse_manager_dashboard.html')

from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test

@login_required
@user_passes_test(lambda u: u.groups.filter(name='warehouse_managers').exists())
def warehouse_manager_dashboard(request):
    return render(request, 'users/warehouse_manager_dashboard.html')

from django.contrib.auth import logout
from django.shortcuts import redirect

def custom_logout(request):
    logout(request)
    return redirect('login')  # Redirect to the login page

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

def is_warehouse_staff(user):
    return user.groups.filter(name='warehouse_staff').exists()

@login_required
@user_passes_test(is_warehouse_staff)
def warehouse_staff_dashboard(request):
    return render(request, 'users/warehouse_staff_dashboard.html', {'username': request.user.username})

def unauthorized_access(request):
    return render(request, 'users/unauthorized.html')

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.contrib.auth.tokens import default_token_generator as token_generator

def password_reset_request(request):
    if request.method == "POST":
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            # Generate a one-time use token and URL
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = token_generator.make_token(user)
            current_site = get_current_site(request)
            reset_url = reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
            reset_link = f'http://{current_site.domain}{reset_url}'

            # Email the user with the reset link
            subject = "Password Reset Requested"
            html_message = render_to_string('users/password_reset_email.html', {
                'user': user,
                'reset_link': reset_link,
            })
            plain_message = f"Hi {user.username},\n\nClick the link below to reset your password:\n{reset_link}\n\nIf you didn't request a password reset, please ignore this email."

            send_mail(
                subject,
                plain_message,  # Fallback plain text message
                'admin@example.com',
                [user.email],
                html_message=html_message,  # The actual HTML content
                fail_silently=False,
            )

            return redirect('password_request_sent')
        except User.DoesNotExist:
            return render(request, 'users/password_reset_request.html', {
                'error': 'No account found with that email address.'
            })
    return render(request, 'users/password_reset_request.html')

from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.contrib.auth.models import User

def password_reset_confirm(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and token_generator.check_token(user, token):
        if request.method == 'POST':
            password = request.POST.get('password')
            password_confirm = request.POST.get('password_confirm')
            if password == password_confirm:
                user.set_password(password)
                user.save()
                return redirect('password_reset_complete')
            else:
                return render(request, 'users/password_reset_confirm.html', {
                    'error': 'Passwords do not match.',
                })
        return render(request, 'users/password_reset_confirm.html')
    else:
        return render(request, 'users/password_reset_confirm.html', {
            'error': 'The reset link is invalid or has expired.',
        })

from django.shortcuts import render

def password_reset_complete(request):
    return render(request, 'users/password_reset_complete.html')

def password_request_sent(request):
    return render(request, 'users/password_request_sent.html')

from django.contrib.auth import logout
from django.shortcuts import redirect

def custom_logout(request):
    logout(request)
    return redirect('login')  # Replace 'login' with the name of your login URL






