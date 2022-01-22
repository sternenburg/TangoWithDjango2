from django.urls import path
from rango import views



app_name = 'rango'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    
    # <slug:category_name_slug> indicates to django that we want to match a string which is a slug,
    # and to assign it to variable category_name_slug, which is what we pass through to the view
    # show_category()
    # Instead of slugs, we can extract out other variables like strings and integers
    path('category/<slug:category_name_slug>/', 
         views.show_category, name='show_category')
]