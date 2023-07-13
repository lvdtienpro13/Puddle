from django.shortcuts import render, redirect
from item.models import Category, Item
from .forms import SignupForm, SettingProfileForm, ChangePasswordForm
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib.auth.models import User, auth
from django.contrib.auth import update_session_auth_hash
from django.core.paginator import Paginator

# Create your views here.

def index(request):
    item_list = Item.objects.filter(is_sold=False).order_by('-id')
    paginator = Paginator(item_list, 16)  # Chia các mục thành các trang chứa tối đa 8 mục.

    page = request.GET.get('page')  # Lấy số trang từ tham số truy vấn.
    items = paginator.get_page(page)  # Lấy các mục cho trang hiện tại.

    categories = Category.objects.all()

    numbers = [0.5,1.5,2.5,3.5,4.5]

    return render(request, 'core/index.html', {
        'categories': categories,
        'items': items,
        'numbers': numbers,
    })

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()

            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user_login = auth.authenticate(username=username, password=password)
            auth.login(request, user_login)

            user_model = User.objects.get(username=username)
            new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
            new_profile.save()

            return redirect('/settings/')
 
        
    else:
        form = SignupForm()

    return render(request, 'core/signup.html',{
        'form' : form
    })

@login_required
def settings(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        form = SettingProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('core:profile', pk=request.user.username)
    else:
        form = SettingProfileForm(instance=profile, initial={
            'firstname': request.user.first_name,
            'lastname': request.user.last_name,
        })
    return render(request, 'core/setting.html', {'form': form})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request,user)
            return redirect('core:index')
    else:
        form = ChangePasswordForm(request.user)
    return render(request,'core/changepassword.html',{
        'form':form 
    })

@login_required
def profile(request, pk):
    user_object= User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_profile.calculate_avg_rating()
    user_items = Item.objects.filter(created_by=user_object)
    user_items_length = len(user_items)

    numbers = [0.5,1.5,2.5,3.5,4.5]
    
    context = {
        'user_object' : user_object,
        'user_profile' : user_profile,
        'user_items': user_items,
        'user_items_length' :user_items_length,
        'numbers':numbers,
    }
    return render(request, 'core/profile.html', context)

    