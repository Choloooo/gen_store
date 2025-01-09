# inventory/views.py

from django.shortcuts import render, get_object_or_404, redirect
from .models import Item, Transaction
from .forms import ItemForm, TransactionForm, BarcodeScanForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Item
import csv
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas



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
    # Get the search query from the GET parameters, default to an empty string
    query = request.GET.get('q', '') 
    
    if query:
        # Filter items based on the query
        items = Item.objects.filter(name__icontains=query)
    else:
        # If no query, show all items
        items = Item.objects.all()

    # Paginate the queryset
    paginator = Paginator(items, 10)  # Show 10 items per page
    
    # Get the current page number from the URL
    page_number = request.GET.get('page')
    
    # Get the items for the current page
    page_obj = paginator.get_page(page_number)

    # Pass the page_obj and query to the template
    return render(request, 'dashboard.html', {'page_obj': page_obj, 'query': query})



def reports(request):
    # Get all items from the database
    items = Item.objects.all()

    # Calculate the total number of items
    total_items = items.count()

    # Calculate the total quantity of all items
    total_quantity = sum(item.quantity for item in items)

    # Pass these values to the template
    return render(request, 'reports.html', {
        'total_items': total_items,
        'total_quantity': total_quantity,
        'items': items
    })


def export_csv(request):
    items = Item.objects.all()
    total_items = items.count()
    total_quantity = sum(item.quantity for item in items)

    # Create the response object for CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="inventory_report.csv"'

    # Create the CSV writer
    writer = csv.writer(response)

    # Write the header row
    writer.writerow(['Item Name', 'Quantity'])
    for item in items:
        writer.writerow([item.name, item.quantity])

    # You can also add the summary information at the bottom
    writer.writerow([])
    writer.writerow(['Total Number of Items', total_items])
    writer.writerow(['Total Quantity', total_quantity])

    return response

def export_pdf(request):
    items = Item.objects.all()
    total_items = items.count()
    total_quantity = sum(item.quantity for item in items)

    # Create the response object for PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="inventory_report.pdf"'

    # Create the PDF object and set up the canvas
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    # Title
    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, height - 40, "Inventory Report")

    # Add the summary
    p.setFont("Helvetica", 12)
    p.drawString(30, height - 80, f"Total Number of Items: {total_items}")
    p.drawString(30, height - 100, f"Total Quantity of Items: {total_quantity}")

    # Add a table with item names and quantities
    p.setFont("Helvetica-Bold", 12)
    p.drawString(30, height - 140, "Item Name")
    p.drawString(300, height - 140, "Quantity")

    # Write item data into the PDF
    y_position = height - 160
    p.setFont("Helvetica", 12)
    for item in items:
        p.drawString(30, y_position, item.name)
        p.drawString(300, y_position, str(item.quantity))
        y_position -= 20  # Move down for the next item

    # Save the PDF
    p.showPage()
    p.save()

    return response





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



