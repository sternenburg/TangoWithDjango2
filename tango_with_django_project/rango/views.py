from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage matches to {{ boldmessage }} in the template!
    context_dict = {'boldmessage': 'Crunchy, creamy, cookie, candy, cupcakes!'}

    # Return a rendered response to send the client.
    # Note that the first parmeter is the template we wish to use.
    
    # return HttpResponse("Rango says hey there partner!")
    return render(request, 'rango/index.html', context=context_dict)
    
def about(request):
    return HttpResponse('This is the about page.')