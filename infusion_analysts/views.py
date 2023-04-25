from django.shortcuts import render,redirect
from django.contrib.auth.models import User 
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.template.response import TemplateResponse
from django.http import HttpResponse
import requests


# Create your views here.

def register_1(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        re_password = request.POST['re_password']
        if password == re_password:
            if User.objects.filter(username = username).exists():
                messages.error(request,'Username already exist')
                return render(request,'account/register.html')
            elif User.objects.filter(email = email).exists():
                messages.error(request,'email already exist')
                return render(request,'account/register.html')
            else:
                user=User.objects.create_user(first_name = first_name,last_name = last_name,username = username,email=email,password = password)
                user.save()
                return redirect('login1')
        else:
            messages.error(request,'password does not match')
            return render(request,'account/register.html')
    else:
        return render(request,'account/register.html')
    
def login_1(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username = username,password = password)
        if user is not None:
            print(request)
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'Invalid credencials')
            return render(request,'account/login1.html')
    else:
        return render(request,'account/login1.html')

def logout_1(request):
    logout(request)                                                                                                                          
    return redirect('home')

def home(request):
    if request.method == "GET":
        auth_code = request.GET.get('code')
        if auth_code:
            # Generate the code verifier and code challenge
            code_verifier = b'T1RCR1VscFlSa2sxTUZsWlNWYzNWRWsyVGtOQlJqRTBVRmMxUXpnNFZWRktRMVJaV0ZFNVFrcERRVE5VVFU5Rk5FdzFNRTVEUkZVNU0wOVNOVXBhT0RCRlQxaERSRlpIVURoVw=='
            # code_verifier = base64.urlsafe_b64encode(code_verifier.encode('utf-8'))
            print(code_verifier)
            data = {
                'grant_type': 'authorization_code',
                'code': auth_code,
                'redirect_uri': 'http://localhost:8000/home/',
                'code_verifier': code_verifier,
            }
            # response = requests.post('http://localhost:7000/o/token/', data=data, auth=('client_id', 'client_secret'))
            response = requests.post('http://localhost:7000/o/token/', data=data, auth=('RO1tlvKqigM7OEAi4igEfn7rp6FrK3zDSfwPC70j', 'HiuUAAuaobpMB46U3jE0fk3XIbweqfdQfsU5oiujPNYJF1VDPuv2kEJEeXspfkywsPzLNi3KhgpCezhuLJyJJwjfZqqrY1fjLkwp3cBIKrD8nnqm1T0qeqlJ84uaUdAN'))
            print(response.json())  # This line will print out the JSON response
            access_token = response.json()['access_token']
            # print(access_token)
            if response.status_code == 200:
                access_token = response.json()['access_token']
                # Get user data using access token
                headers = {'Authorization': f'Bearer {access_token}'}
                response = requests.get('http://localhost:7000/users/', headers=headers)
                if response.status_code == 200:
                    user_data = response.json()
                    # print(user_data)
                    return HttpResponse(f"Welcome {user_data['username']}, your email is {user_data['email']}")
                else:
                    return HttpResponse("Failed to fetch user data")
            else:
                return HttpResponse("Failed to obtain access token")
        else:
            return HttpResponse("Authorization code not found")
    else:
        return HttpResponse("Invalid request method")





