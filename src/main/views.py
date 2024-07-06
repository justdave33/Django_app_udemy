from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages



from .filters import ListingFilter
from .models import Listing
from .forms import ListingForm
from users.forms import LocationForm

# Create your views here.
    #first we define a function

def main_view(request):
    return render(request,"page_views/main.html", {"name": "GreenCode"})

@login_required
def home_view(request):
    listings = Listing.objects.all()
    listing_filter = ListingFilter(request.GET, queryset=listings)
    context = {
        
        'listing_filter': listing_filter,
    }
    return render(request, 'page_views/home.html', context)

@login_required
def list_view(request):
    if request.method == 'POST':
        try:
             listing_form = ListingForm(request.POST, request.FILES)
             location_form = LocationForm(request.POST)
             if listing_form.is_valid() and location_form.is_valid():
                 listing = listing_form.save(commit=False)
                 listing_location = location_form.save()
                 listing.seller = request.user.profile
                 listing.location = listing_location
                 listing.save()
                 messages.info(
                     request, f'{listing.model} Listing posted successfully')
                 return redirect('home')
             else:
                 raise Exception()

        except Exception as e:
            messages.error(request,'An error occured while posting the list')
    elif request.method == 'GET':
       listing_form = ListingForm()
       location_form = LocationForm()
    return render (request, 'page_views/list.html', {'listing_form': listing_form, 'location_form':location_form})


@login_required
def listing_view(request, id):
    try:
        listing = Listing.objects.get(id=id)
        if listing is None:
            raise Exception
        return render(request, 'page_views/listing.html', {'listing': listing, })
    except Exception as e:
        messages.error(request, f'Invalid UID {id} was provided for listing.')
        return redirect('home')
    
    
@login_required
def edit_view(request, id):
    try:
        listing = Listing.objects.get(id=id)
        if listing is None:
            raise Exception
        if request.method == 'POST':
            pass
        else:
          print(id)
        return render (request, 'page_views/edit.html', {})
    except Exception as e:
        messages.error(
            request, f"An error occured while trying to edit the listing ")
        return redirect('home')
       
   

