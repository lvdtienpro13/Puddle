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
    item_list = Item.objects.filter(is_sold=False)
    paginator = Paginator(item_list, 8)  # Chia các mục thành các trang chứa tối đa 16 mục.

    page = request.GET.get('page')  # Lấy số trang từ tham số truy vấn.
    items = paginator.get_page(page)  # Lấy các mục cho trang hiện tại.

    categories = Category.objects.all()

    return render(request, 'core/index.html', {
        'categories': categories,
        'items': items,
    })

# def index(request):
#     items = Item.objects.filter(is_sold=False)[0:16]
#     categories = Category.objects.all()

#     return render(request, 'core/index.html', {
#         'categories': categories,
#         'items': items,
#     })

def contact(request):
    return render(request, 'core/contact.html')

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

# @login_required
# def settings(request):
#     user_profile = Profile.objects.get(user=request.user)
#     if request.method == 'POST':
        
#         if request.FILES.get('image') == None:
#             image = user_profile.profileimg
#             bio = request.POST['bio']
#             location = request.POST['location']

#             user_profile.profileimg = image
#             user_profile.bio = bio
#             user_profile.location = location
#             user_profile.save()
#         if request.FILES.get('image') != None:
#             image = request.FILES.get('image')
#             bio = request.POST['bio']
#             location = request.POST['location']

#             user_profile.profileimg = image
#             user_profile.bio = bio
#             user_profile.location = location
#             user_profile.save()
        
#         return redirect('/settings/')
#     form = SettingProfileForm(instance=user_profile)
#     return render(request, 'core/setting.html', {
#         'form': form})
@login_required
def settings(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        form = SettingProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('core:settings')
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
    user_items = Item.objects.filter(created_by=user_object)
    user_items_length = len(user_items)
    
    context = {
        'user_object' : user_object,
        'user_profile' : user_profile,
        'user_items': user_items,
        'user_items_length' :user_items_length,
    }
    return render(request, 'core/profile.html', context)

    