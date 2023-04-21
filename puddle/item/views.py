from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from .models import Item, Category, OrderItem, Order
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from django.utils import timezone
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist

from .forms import NewItemForm, EditItemForm
# Create your views here.

def items(request):
    items = Item.objects.filter(is_sold = False)
    query = request.GET.get('query', '')
    category_id = request.GET.get('category', 0)
    categories = Category.objects.all()

    if category_id:
        items = items.filter(category_id=category_id)
    
    if query:
        items = items.filter(Q(name__icontains=query) | Q(description__icontains=query))

    return render(request, 'item/items.html', {
        'items' : items[0:8],
        'query' : query,
        'categories': categories,
        'category_id': int(category_id)
    })


def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    related_items = Item.objects.filter(category=item.category, is_sold=False).exclude(pk=pk)[0:3]
    
    return render(request, 'item/detail.html',{
        'item' : item,
        'related_items' : related_items
    })

@login_required
def new(request):
    if request.method == "POST":
        form = NewItemForm(request.POST, request.FILES)

        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()

            return redirect('item:detail', pk=item.id)
    else:
        form = NewItemForm()

    return render(request, 'item/form.html', {
        'form' : form,
        'title' : 'New Item',
    })

@login_required
def delete(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)
    item.delete()

    return redirect('dashboard:index')

@login_required
def edit(request, pk):
    item =get_object_or_404(Item, pk=pk, created_by=request.user)

    if request.method== 'POST':
        form = EditItemForm(request.POST, request.FILES, instance=item)
        
        if form.is_valid():
            form.save()
            return redirect('item:detail', pk=item.id)
    else:
        form = EditItemForm(instance=item)
    return render(request, 'item/form.html',{
        'form': form,
        'title' : 'Edit Form'
    })

@login_required
def add_to_cart(request, pk):
    item = get_object_or_404(Item, pk=pk)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__pk=item.pk).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("item:order-summary")
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("item:order-summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("item:order-summary")


@login_required
def remove_from_cart(request, pk):
    item = get_object_or_404(Item, pk=pk)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__pk=item.pk).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "This item was removed from your cart.")
            return redirect("item:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("item:order-summary")
    else:
        messages.info(request, "You do not have an active order")
        return redirect("item:order-summary")


@login_required
def remove_single_item_from_cart(request, pk):
    item = get_object_or_404(Item, pk=pk)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__pk=item.pk).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was updated.")
            return redirect("item:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("item:detail", pk=pk)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("item:detail", pk=pk)

# class OrderSummaryView(View):
#     def get(self,*args, **kwargs ):
#         return render(self.request, 'item/order_summary.html')
class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'item/order_summary.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("/")