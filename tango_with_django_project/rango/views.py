from django.shortcuts import render
from django.http import HttpResponse

# import the Category model
from rango.models import Category
from rango.models import Page

def index(request):
    # # Construct a dictionary to pass to the template engine as its context.
    # # Note the key boldmessage matches to {{ boldmessage }} in the template!
    # context_dict = {'boldmessage': 'Crunchy, creamy, cookie, candy, cupcakes!'}

    # # Return a rendered response to send the client.
    # # Note that the first parmeter is the template we wish to use.
    
    # # return HttpResponse("Rango says hey there partner!")
    # return render(request, 'rango/index.html', context=context_dict)
    
    # Query the database for a list of All categories currently stored.
    # Order the categories by the number of likes in descending order.
    # Retrieve the top 5 only -- or all if less than 5
    # Place the list in our context_dict dictionary (with our boldmessage!)
    # that will be passed to the template engine.
    category_list = Category.objects.order_by('-likes')[:5]
    
    page_list = Page.objects.order_by('-views')[:5]
    
    
    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list
    
    context_dict['pages'] = page_list
    
    # Render the response and send it back!
    return render(request, 'rango/index.html', context = context_dict)
        
        
def about(request):
    context_dict = {'your_name': 'Lei'}
    return render(request, 'rango/about.html', context=context_dict)

def show_category(request, category_name_slug):
    # Create a context dict which we can pass to the template rendering engine.
    context_dict = {}
    
    try:
        # If we can't find a category name slug with the given one,
        # the .get() method raises a DoesNotExist exception.
        # If we can, the .get() method returns one model instance.
        category = Category.objects.get(slug=category_name_slug)
        
        # Retrieve all of the associated pages.
        # the filter() will return a list of page objects or an empty list
        pages = Page.objects.filter(category=category)
        
        # Add the results list to the template context under name pages.
        context_dict['pages'] = pages
        
        # We also add the category object from the database to the context dict.
        # We will use this in the template to verify that the category exists.
        context_dict['category'] = category
        
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pages'] = None
        
    # Go render the response and return it to the client.
    return render(request, 'rango/category.html', context=context_dict)

