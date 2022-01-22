import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'tango_with_django_project.settings')

import django
django.setup()
from rango.models import Category, Page

def populate():
    python_pages = [
        {'title': 'Official Python Tutorial',
         'url': 'http://docs.python.org/3/tutorial/',
         'views': 10},
        {'title': 'How to Think like a Computer Scientist',
         'url': 'http://www.greeteapress.com/thinkpython',
         'views': 13},
        {'title': 'w3school',
         'url': 'http://www.w3school.com.cn',
         'views':14},
    ]
    
    movie_pages = [
        {'title': '腾讯视频',
         'url': 'http://v.qq.com/',
         'views': 20},
        {'title': '爱奇艺',
         'url': 'http://www.greeteapress.com/thinkpython',
         'views':38},
        {'title': '芒果TV',
         'url': 'http://www.mgtv.com',
         'views': 19},
    ]

    other_pages = [
        {'title': '百度',
         'url': 'http://www.baidu.com/',
         'views': 1},
        {'title': 'Bing',
         'url': 'http://www.bing.com',
         'views': 6},
    ]

    cats = {'Python': {'pages': python_pages,
                       'views': 128,
                       'likes':64},
            'Movie': {'pages': movie_pages,
                      'views':64,
                      'likes':32},
            'Other Frameworks': {'pages': other_pages,
                                 'views': 32,
                                 'likes':16}
    }

    
    # Goes through the cats dictionary, then adds each c
    # and then adds all the associated pages for that category
    for cat, cat_data in cats.items():
        c = add_cat(cat, cat_data['views'], cat_data['likes'])
        for p in cat_data['pages']:
            add_page(c, p['title'], p['url'], p['views'])
            
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

<<<<<<< HEAD
def add_cat(name, views=0, likes=0):
=======
def add_cat(name, views, likes):
>>>>>>> 4be9a6724290d30d609c089a6328ee9dd3eebb34
    c = Category.objects.get_or_create(name=name)[0]
    c.views = views
    c.likes = likes
    c.save()
    return c

# Start execution here!
if __name__ == '__main__':
    print('Starting Rango population script...')
    populate()
            