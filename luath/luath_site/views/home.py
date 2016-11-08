from django.views.decorators.http import require_http_methods
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.shortcuts import render
from django.contrib import messages
import json, requests, os

with open('./luath_site/data/homepage.json', 'r') as f:
    homepage_data = f.read()
    homepage_json = json.loads(homepage_data)

@require_http_methods(["GET", "POST"])
def index(request):
    if request.method == 'GET':
        return render_home(request, homepage_json)
    elif request.method == 'POST':
        email = request.POST['email']
        if not validateEmail(email):
            return error(request, 'Please sign up with a valid email')
        if user_exists(email):
            return error(request, 'That email is already in use. If you can\'t \
            remember your API key, please get in touch \
            <a href="https://www.twitter.com/kerrmarin">@kerrmarin</a>')
        user = User.objects.create_user(email)
        if not user:
            return error(request, 'An error occurred creating your API key, \
            please try again')

        r = send_email(email, user)
        if r.status_code == requests.codes.ok:
            messages.success(request, 'API key successfully requested. You\'ll \
            receive an email with your API key shortly. Thanks for using Luath :)')
            return render_home(request, homepage_json)
        else:
            return error(request, 'There was an error requesting your API key, \
            please try again.')

def validateEmail(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False

def user_exists(email):
    return User.objects.filter(username=email).exists()

def error(request, error):
    messages.error(request, error, extra_tags='safe error')
    return render_home(request, homepage_json)

def email_data(email, token):
    return {
        'from': 'Luath API <kerr@kerrmarin.com>',
        'to': email,
        'subject': 'Luath API key for ' + email,
        'text': ('Here is your API key: ' + token + "."
            " Include it in the Authorization header preceded by 'Token'."
            " For example: 'Authorization: Token " + token + "'.")
    }

def render_home(request, data):
    return render(request, 'luath_site/index.html', data)

def send_email(user_email, user):
    token = Token.objects.create(user=user)
    data = email_data(user_email, token.key)
    url = os.environ['mailgun_url']
    return requests.post(url, data=data)
