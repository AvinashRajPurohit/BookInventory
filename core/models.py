from django.db import models

# Create your models here.


class Books(models.Model):
    title = models.CharField(max_length=300)
    description = models.TextField()
    image = models.URLField()
    preview_link = models.URLField()
    info_link = models.URLField()
    book_id = models.SlugField()
    number_of_copies = models.PositiveIntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title