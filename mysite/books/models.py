from django.db import models


class Publisher(models.Model):
    name = models.TextField()

    def __unicode__(self):
        return self.name


class Author(models.Model):
    first_name = models.TextField()
    last_name = models.TextField()

    def __unicode__(self):
        return u'%s %s' % (self.first_name, self.last_name)


class Book(models.Model):
    title = models.TextField()
    authors = models.ManyToManyField(Author)
    publisher = models.ForeignKey(Publisher, on_delete=models.PROTECT)
    publication_date = models.DateField()
    isbn = models.TextField()

    def __unicode__(self):
        return self.title
