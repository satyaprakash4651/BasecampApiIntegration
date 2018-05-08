from allauth.account.views import LoginView
from allauth.socialaccount.models import SocialAccount, SocialToken
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

from todoapp.forms import TodoForm
from todoapp.basecamp import BasecampConnection


class CustomLoginView(LoginView):
    template_name = 'login.html'


@require_http_methods(['GET', 'POST'])
def index(request):
    return redirect('/accounts/login')


@require_http_methods(['GET', 'POST'])
def todoadd(request):
    template_name = 'todoapp/add.html'

    if request.method == 'GET':
        return render(request, template_name, {
            'form': TodoForm(),
        })
    else:
        form = TodoForm(request.POST, request.FILES)
        if form.is_valid():
            account = SocialAccount.objects.filter(user=request.user, provider='basecamp')
            if account:
                cd = form.cleaned_data
                access_token = SocialToken.objects.filter(account=account).first().token
                bc = BasecampConnection(access_token)
                bc.create_todo_with_attachment(cd['title'], cd['audio_file'])
                success = True
            else:
                success = False

            return render(request, template_name, {
                'form': TodoForm(),
                'success': success,
            })
        return render(request, template_name, {
            'form': form,
        })
