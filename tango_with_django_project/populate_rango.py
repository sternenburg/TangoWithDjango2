import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'tango_with_django_project.settings')

import django
django.setup()
from rango.models import Category, Page

def populate():
    python_pages = [
        {'title': 'Official Python Tutorial',
         'url': 'http://docs.python.org/3/tutorial/'},
        {'title': 'How to Think like a Computer Scientist',
         'url': 'http://www.greeteapress.com/thinkpython'},
        {'title': 'Baidu',
         'url': 'http://www.baidu.com'},
    ]
    
    movie_pages = [
        {'title': '腾讯视频',
         'url': 'http://v.qq.com/'},
        {'title': '爱奇艺',
         'url': 'http://www.greeteapress.com/thinkpython'},
        {'title': 'Baidu',
         'url': 'http://www.baidu.com'},
    ]

    other_pages = [
        {'title': '百度',
         'url': 'http://www.baidu.com/'},
        {'title': 'Bing',
         'url': 'http://www.bing.com'},
    ]
    cats = {'Python': {'pages': python_pages},
            'Movie': {'pages': movie_pages},
            'Other Frameworks': {'pages': other_pages}}
    
    # Goes through the cats dictionary, then adds each c
    # and then adds all the associated pages for that category
    for cat, cat_data in cats.items():
        c = add_cat(cat)
        for p in cat_data['pages']:
            add_page(c, p['title'], p['url'])
            
    # Print out the categories we have added.
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print('- {0} - {1}'.format(str(c), str(p)))
            
def add_page(cat, title, url, views = 0):
    # get_or_create() method returns a tuple of (object, created)
    # created is a boolean value
    p = Page.objects.get_or_create(category=cat, title=title)[0]
    p.url = url
    p.views = views
    p.save()
    return p

def add_cat(name):
    c = Category.objects.get_or_create(name=name)[0]
    c.save()
    return c

# Start execution here!
if __name__ == '__main__':
    print('Starting Rango population script...')
    populate()
            