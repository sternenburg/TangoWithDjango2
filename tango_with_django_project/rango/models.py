from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)

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

