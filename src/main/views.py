from importlib import reload
from django.shortcuts import redirect, render,get_object_or_404
from django.http import  JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail




from .filters import ListingFilter
from .models import LikedListing, Listing
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
    user_liked_listings = LikedListing.objects.filter(profile=request.user.profile).values_list('listing')
    liked_listings_id = [ l[0] for l in user_liked_listings]
   
    context = {
        
        'listing_filter': listing_filter,
        'liked_listings_id':liked_listings_id,
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
            listing_form = ListingForm(request.POST,request.FILES, instance=listing)
            location_form = LocationForm(request.POST,instance=listing.location)
            if listing_form.is_valid and location_form.is_valid:
                listing_form.save()
                location_form.save() 
                messages.info(request, f'Listing {id} updated successfully!')
                return redirect('home')
            else :
                messages.error(request,
                               f'An error occured while trying to edit the listing.')
                return reload()
        else:
          listing_form = ListingForm(instance=listing)
          location_form = LocationForm(instance=listing.location)
        context = {
            'location_form':location_form,
            'listing_form': listing_form
        }  
        return render (request, 'page_views/edit.html', context)
    except Exception as e:
        messages.error(
            request, f"An error occured while trying to access the edit page ")
        return redirect('home')
    
    
@login_required  
def like_listing_view(request, id):
  
    listing = get_object_or_404(Listing, id=id )
    
    liked_listing,created = LikedListing.objects.get_or_create(
        profile=request.user.profile, listing=listing)
    if not created :
        liked_listing.delete()
        
    else:
        liked_listing.save()   
        
    return JsonResponse({
        'is_liked_by_user':created,
    })
    
    

@login_required
def inquire_listing_using_email(request, id):
    listing = get_object_or_404(Listing, id=id)
    try:
        emailSubject = f'{request.user.username} is interested {listing.model}' #this is going to be the header of our email
        emailMessage = f'Hi {listing.seller.user.username}, {request.user.username} is interested in your {listing.model} listing on Greencode'
        send_mail(emailSubject, emailMessage, 'noreply@greencode.com', [listing.seller.user.email], fail_silently=True)
        return JsonResponse({
             'success': True,
           
        })
    except Exception as e:
        print(e)   
        return JsonResponse({
            'success': False,
            'info': e,
        }) 
        
       
   


