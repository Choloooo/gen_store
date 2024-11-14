# inventory/views.py

from django.shortcuts import render, get_object_or_404, redirect
from .models import Item, Transaction
from .forms import ItemForm, TransactionForm, BarcodeScanForm
from django.contrib.auth.decorators import login_required

from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Item



from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def item_list(request):
    items = Item.objects.all()
    return render(request, 'inventory/item_list.html', {'items': items})

@login_required
def add_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('item_list')
    else:
        form = ItemForm()
    return render(request, 'inventory/add_item.html', {'form': form})

@login_required
def scan_barcode(request):
    if request.method == 'POST':
        form = BarcodeScanForm(request.POST)
        if form.is_valid():
            barcode = form.cleaned_data['barcode']
            item = get_object_or_404(Item, barcode=barcode)
            return redirect('add_transaction', item_id=item.id)
    else:
        form = BarcodeScanForm()
    return render(request, 'inventory/scan_barcode.html', {'form': form})

@login_required
def add_transaction(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.item = item
            transaction.save()
            # Update item quantity
            if transaction.transaction_type == 'IN':
                item.quantity += transaction.quantity
            elif transaction.transaction_type == 'OUT':
                item.quantity -= transaction.quantity
            item.save()
            return redirect('item_list')
    else:
        form = TransactionForm()
    return render(request, 'inventory/add_transaction.html', {'form': form, 'item': item})



# inventory/views.py


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})



# inventory/views.py


@login_required
def dashboard(request):
    items = Item.objects.all()
    return render(request, 'dashboard.html', {'items': items})




# inventory/views.py



@login_required
def add_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ItemForm()
    return render(request, 'dashboard.html', {'form': form, 'items': Item.objects.all()})

@login_required
def edit_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ItemForm(instance=item)
    return render(request, 'dashboard.html', {'form': form, 'items': Item.objects.all()})

@login_required
def delete_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    item.delete()
    return redirect('dashboard')


@login_required
def item_list(request):
    items = Item.objects.all()
    return render(request, 'inventory/item_list.html', {'items': items})


def qr_scanner(request):
    return render(request, 'qr_scanner.html')



# views.py



