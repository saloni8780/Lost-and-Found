from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse
from .forms import CollegeUserCreationForm , LoginForm
from django.contrib.auth import login,authenticate, logout
from .forms import LostFoundItemForm,ClaimDetailForm
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.contrib import messages
from . models import LostFoundItem,ClaimDetail


# Create your views here.



def home(request):
    
    return render(request, 'home.html')
def Guidelines(request):
    
    return render(request, 'Guidelines.html')
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
    claimed_items = ClaimDetail.objects.values_list('item_id', flat=True)
    items = LostFoundItem.objects.exclude(id__in=claimed_items)
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
def claim_item(request, item_id):
    item = get_object_or_404(LostFoundItem, id=item_id)

    if request.method == 'POST':
        form = ClaimDetailForm(request.POST)
        if form.is_valid():
            claim = form.save(commit=False)
            claim.item = item
            claim.save()
            item.item_type = 'Found'  
            item.save()
            return redirect('my_posts')  
    else:
        form = ClaimDetailForm()
    
    return render(request, 'claim_item.html', {'form': form, 'item': item})
@login_required
def view_all_claims(request):
    claims = ClaimDetail.objects.select_related('item__posted_by').all()
    return render(request, 'view_all_claims.html', {'claims': claims})
