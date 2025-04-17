from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import CollegeUserCreationForm , LoginForm
from django.contrib.auth import login,authenticate, logout
from .forms import LostFoundItemForm
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.contrib import messages
from . models import LostFoundItem


# Create your views here.



def home(request):
    
    return render(request, 'home.html')
def signup_view(request):
    if request.method == 'POST':
        form = CollegeUserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                messages.success(request, "Registration successful.")
                return redirect('home')
            except IntegrityError:
                messages.error(request, "User ID or Email already exists.")
    else:
        form = CollegeUserCreationForm()
    return render(request, 'signup.html', {'form': form})

# Login View
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username').upper()
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

# Logout View
def logout_view(request):
    logout(request)
    return redirect('signup')

def find_item(request):
    return render(request, 'find_item.html')
def post_item(request):
    return render(request, 'post_item.html')
def about_us(request):
    return render(request, 'about_us.html')


@login_required
def post_item_view(request):
    if request.method == 'POST':
        form = LostFoundItemForm(request.POST, request.FILES)
        if form.is_valid():
            lost_found_item = form.save(commit=False)
            lost_found_item.posted_by = request.user
            lost_found_item.save()  
            
            return redirect('find_item')  
    else:
        form = LostFoundItemForm()
    return render(request, 'post_item.html', {'form': form})
def find_item(request):
    items = LostFoundItem.objects.all()  
    return render(request, 'find_item.html', {'items': items})
def item_detail(request, item_id):
    try:
        item = LostFoundItem.objects.get(id=item_id)
    except LostFoundItem.DoesNotExist:
        return redirect('find_item')  

    return render(request, 'item_detail.html', {'item': item})
@login_required
def my_posts(request):
    items = LostFoundItem.objects.filter(posted_by=request.user)
    return render(request, 'my_posts.html', {'items': items})
@login_required
def delete_item(request, item_id):
   
        item = LostFoundItem.objects.get(id=item_id, posted_by=request.user)
        item.delete()
        return redirect('my_posts')
