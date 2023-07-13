from pyexpat.errors import messages
from django.http import Http404
from django.shortcuts import render
from  .models import Rating
from .forms import RatingForm
from item.models import Item, OrderItem
from .models import Rating
from core.models import Profile
from django.shortcuts import render,redirect, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
# def rating(request):
#     return render(request, 'rating/rating.html')
@login_required
def index(request):
    rated_type = request.GET.get('rated_type', 0)
    if int(rated_type)==0:
        items = OrderItem.objects.filter(user=request.user,ordered=True, rated=False).order_by('-id')
    else:
        items = OrderItem.objects.filter(user=request.user,ordered=True, rated=True).order_by('-id')
    items_with_rating = []
    for item in items:
        rating = Rating.objects.filter(order_item=item).first()
        items_with_rating.append({
            'item': item,
            'rating': rating if rating else None,
        })

    return render(request, 'rating/index.html', {
        'items_with_rating':items_with_rating,
        'rated_type':rated_type,
    })

@login_required
def rating(request, order_item_id):
    order_item = get_object_or_404(OrderItem, id = order_item_id)
    item = order_item.item
    if order_item.rated==False:
        user = request.user
        profile = Profile.objects.get(user=user)
        if request.method == 'POST':
            form = RatingForm(request.POST)
            if form.is_valid():
                rating = form.save(commit=False)
                rating.item = item
                rating.user = user
                rating.order_item = order_item
                rating.save()
                order_item.rated=True
                order_item.save()
                # update the average rating of the item, user
                item.calculate_avg_rating()
                profile.calculate_avg_rating()

                url = reverse('rating:index')
                url_with_params = url + '?rated_type=0'
                return redirect(url_with_params)
        else:
            form = RatingForm()

        numbers = [0.5,1.5,2.5,3.5,4.5]
        return render(request, 'rating/rating.html', {
            'form': form,
            'order_item' : order_item,
            'numbers':numbers,
            })
    else:
         return redirect('item:detail', pk=item.pk)