from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from .models import ReportedItem
from .forms import ReportForm
from django.contrib.auth.forms import UserCreationForm

def index(request):
    recent_items = ReportedItem.objects.order_by('-created_at')[:6]
    return render(request, 'index.html', {'recent_items': recent_items})


def report(request):
    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            report_item = form.save()

            if report_item.type.lower() == 'lost':
                matches = ReportedItem.objects.filter(
                    type__iexact='found',
                    name__icontains=report_item.name
                )

                if matches.exists():
                    message = "Hello! We found these items matching your lost item:\n\n"
                    for item in matches:
                        message += f"- {item.name} found at {item.location}, contact: {item.contact}\n"

                    send_mail(
                        'Match Found for Your Lost Item',
                        message,
                        settings.EMAIL_HOST_USER,
                        [report_item.contact],
                        fail_silently=False,
                    )

            return redirect('thank_you')
    else:
        form = ReportForm()
    return render(request, 'report.html', {'form': form})

def thank_you(request):
    return render(request, 'thank_you.html')

def items_list(request):
    query = request.GET.get('q', '')
    if query:
        items = ReportedItem.objects.filter(name__icontains=query)
    else:
        items = ReportedItem.objects.all()
    return render(request, 'items.html', {'items': items, 'query': query})

def item_detail(request, item_id):
    item = get_object_or_404(ReportedItem, id=item_id)
    return render(request, 'item_details.html', {'item': item})


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login after signup
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
