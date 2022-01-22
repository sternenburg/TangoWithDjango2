from django.db import models
from django.template.defaultfilters import slugify

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    
    # in order to make readable URLs, so called "percent-encoded"
    # eg. change "how are you" to "how-are-you"
    slug = models.SlugField(unique=True) # unique参数保证唯一性
    
    # overidde the save() function
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Page(models.Model):
    # the ForeignKey field type allows to create a one-to-many relationship
    # CASCADE instructs Django to delete the pages associated
    # with category when the category is deleted.
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)
    # Another commonly used field type is DateField
    # which stores a Python datetime.date object.

    def __str__(self):
        return self.title

