# from curses.ascii import HT
from unicodedata import category
from webbrowser import get
from django.shortcuts import render
from django.http import HttpResponse

# import the Category model
from rango.models import Category
from rango.models import Page

from rango.forms import CategoryForm, PageForm
from django.shortcuts import redirect
from django.urls import reverse

from rango.forms import UserForm, UserProfileForm

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required

from datetime import datetime

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

    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']
    response = render(request, 'rango/index.html', context=context_dict)

    
    # # Obtain our Response object early so we can add cookie information.
    # response = render(request, 'rango/index.html', context=context_dict)
    # # Call the helper function to handle the cookies
    # visitor_cookie_handler(request, response)

    # Render the response and send it back!
    return response
        
        
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

@login_required
def add_category(request):
    form = CategoryForm()
    
    # A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        
        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)
            # Now that the category is saved, we could confirm this.
            # For now, just redirect the user back to the index view.
            return redirect('/rango/')
        else:
            # The supplied form contained errors -
            # just print them to the terminal
            print(form.errors)
            
    # Will handle the bad form, new form, or no form supplied cases.
    # Render the form with error messages (if any).
    return render(request, 'rango/add_category.html', {'form': form})

@login_required     
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None
    
    if category is None:
        return redirect('/rango/')
    
    form = PageForm()
    
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                return redirect(reverse('rango:show_category',
                                        kwargs = {'category_name_slug':
                                            category_name_slug}))
        else:
            print(form.errors)
            
    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context=context_dict)
'''
def register(request):
    # A boolean value for telling the tempalte whether the registration was successful.
    # Set to False initially. code changes value to True when registration succeeds.
    registered = False

    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            # Hash the password with the set_password method.
            # Once hashed, update the user object.
            user.set_password(user.password)
            user.save()

            # information from the UserProfileForm form is passed onto a new instance of the UserProfile
            # model. The UserProfile contains a foreign key reference to the standard Django
            # User model – but the UserProfile does not provide this information! Attempting
            # to save the new instance in an incomplete state would raise a referential integrity
            # error. The link between the two models is required.
            # To counter this problem, we instruct the UserProfileForm to not save straight away,
            # This then allows us to add the User reference in with the
            # line profile.user=user. After this is done, we can then call
            # the profile.save() method to manually save the new instance to the
            # database. This time, referential integrity is guaranteed, and everything works as
            # it should.
            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()

            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        # Not a HTTP POST, so render the form using two ModelForm instaces,
        # These forms will be blank, ready for user input.
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render(request,
                  'rango/register.html',
                  context = {'user_form': user_form,
                             'profile_form': profile_form,
                             'registered': registered})
'''

'''
def user_login(request):
    # if the request is a HTTP POST, try to pull out the relevant information
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None, no user with matching credentials was found.
        if user:
            # Is the account is active? It could have been disabled.
            if user.is_active:
                login(request, user)
                return redirect(reverse('rango:index'))
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            # Bad login details were provided, so we can't log the user in
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")

    else:
        # No context variables to pass to the template system, hence the 
        # blank dictionary object...
        return render(request, 'rango/login.html')
'''

@login_required
def restricted(request):
    return render(request, 'rango/restricted.html')

'''
@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('rango:index'))
'''

# def visitor_cookie_handler(request, response):
#     # Get the number of visits to the site.
#     # Use the COOKIES.get() to obtain the 'visits' cookie.
#     # If the cookie exists, the value returned is casted to an integer.
#     # If the cookie doesn't exist, then the default value of 1 is used.
#     visits = int(request.COOKIES.get('visits', '1'))

#     last_visit_cookie = request.COOKIES.get('last_visit', str(datetime.now()))
#     last_visit_time = datetime.strptime(last_visit_cookie[:-7],
#                                         '%Y-%m-%d %H:%M:%S')

#     # If it's been more than a day since the last visit...
#     if (datetime.now() - last_visit_time).days > 0:
#         visits = visits + 1
#         response.set_cookie('last_visit', str(datetime.now()))
#     else:
#         visits = 1
#         # Set the last visit cookie
#         response.set_cookie('last_visit', last_visit_cookie)

#     response.set_cookie('visits', visits)

# A helper method
def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val

# Updated the function definition
def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request, 'visits', '1'))
    last_visit_cookie = get_server_side_cookie(request,
                                               'last_visits',
                                               str(datetime.now()))

    last_visit_time = datetime.strptime(last_visit_cookie[:-7],
                                        '%Y-%m-%d %H:%M:%S')

    # If it's been more that a day since the last visit...
    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        # Update the last visit cookie now that we have updated the count
        request.session['last_visit'] = str(datetime.now())
    else:
        # Set the last visit cookie
        request.session['last_visit'] = last_visit_cookie

    # update/set the visits cookie
    request.session['visits'] = visits
