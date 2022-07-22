from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from django.utils.http import is_safe_url


from .forms import LoginForm, RegisterForm, GuestForm
from .models import User, GuestEmail


# Create your views here.

class RegisterView(generic.CreateView):
    template_name = 'accounts/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('accounts:login')

class LoginView(generic.FormView):
    template_name = 'accounts/login.html'
    form_class = LoginForm
    success_url = '/'

    def form_valid(self, form):

        request = self.request
        next_ = request.GET.get('next')
        next_post = request.POST.get('next')
        redirect_path = next_ or next_post or None

        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect('/')

            return super(LoginView, self).form_invalid(form)

def guest_register_view(request):
    form = GuestForm(request.POST or None)
    context = {
        'form': form
    }
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
    if form.is_valid():
        email = form.cleaned_data.get('email')
        guest_email_obj = GuestEmail.objects.create(email=email)
        request.session['guest_email_id'] = guest_email_obj.id
        if is_safe_url(redirect_path, request.get_host()):
            return redirect(redirect_path)
        else:
            return redirect('/')

    return redirect('/register/')
